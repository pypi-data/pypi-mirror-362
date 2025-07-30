import pathlib
import json
from typing import Optional, Any
import papermill as pm
import functools as ft
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TimeElapsedColumn



def execute_run(
    notebook_dir_or_file: pathlib.Path | str,
    bulk_params: list | dict,
    output_dir: Optional[pathlib.Path | str] = None,
    output_prepend_components: Optional[list[str]] = None,
    output_append_components: Optional[list[str]] = None,
    recursive: bool = False,
    exclude_glob_pattern: Optional[str] = None,
    include_glob_pattern: Optional[str] = None,
    use_multiprocessing: bool = False,
    **kwargs,
) -> list[pathlib.Path] | None:
    """
    Executes the notebooks contained in the notebook_dir_or_file using the parameters in
    'bulk_params'.

    'notebook_dir_or_file': If a directory, then will execute all of the notebooks
        within the directory
    'bulk_params': 
        Either a dict in the following format:
        
        {
            "key1": ["list", "of", "values"], # All lists of values must be same length
            "key2": ["list", "of", "values"],
            "key3": ["list", "of", "values"],
            ...
        }, 
        
        -or- 

        A list in the following format:

        [
            {"key1": "value", "key2": "value"}, # All keys
            {"key1": "value", "key2": "value"},
            {"key1": "value", "key2": "value"},
            ...
        ]
    'output_dir': The directory for all output files. If None,
        files will be output in the same directory as the source file.
    'output_prepend_components': A list of str representing the keys used
        in 'bulk_params'. These keys will be used to retrieve the value
        for the key in each iteration of 'bulk_params' and they will
        be used to name the output file be prepending them to the 
        original filename. If a key is not found then the key will
        be interpreted as a str literal and will be added asis.
    'output_append_components': Same as the prepend components but
        these components will be used at the end of the original filename.
    'recursive': If True, and if 'notebook_dir_or_file' is a directory,
        then will execute notebooks within all sub-directories.
    'exclude_glob_pattern': A glob-style pattern of files to exclude.
        If None, then all files willbe included.
    'include_glob_pattern': A glob-style pattern of files to include. If
        None then all files will be included.
    '**kwargs': Passed on to papermill.execute_notebook
    """
    notebook_dir_or_file = pathlib.Path(notebook_dir_or_file)
    output_dir = pathlib.Path(output_dir)
    if isinstance(bulk_params, dict):
        unequal_lengths = check_unequal_value_lengths(bulk_params)
        if unequal_lengths:
            raise ValueError(
                f"All lists in the bulk_params dict must be of equal length.\n"
                f"The following keys have unequal length: {unequal_lengths}"
            )
        bulk_params_list = convert_bulk_params_to_list(bulk_params)
    else:
        bulk_params_list = bulk_params
    
    notebook_dir = None
    notebook_filename = None
    if notebook_dir_or_file.is_dir():
        notebook_dir = notebook_dir_or_file
    else:
        notebook_dir = notebook_dir_or_file.parent.resolve()
        notebook_filename = notebook_dir_or_file.name

    if output_dir is None:
        output_dir = notebook_dir
    if not output_dir.exists():
        output_dir.mkdir(exist_ok=True, parents=True)
    if notebook_filename is not None:
        execute_notebooks(
            notebook_dir / notebook_filename,
            bulk_params_list,
            output_prepend_components,
            output_append_components,
            output_dir,
            use_multiprocessing,
            **kwargs
        )
    else:
        glob_method = notebook_dir.glob
        if recursive:
            glob_method = notebook_dir.rglob

        excluded_paths = set()
        if exclude_glob_pattern is not None:
            excluded_paths = set(glob_method(exclude_glob_pattern))

        glob_pattern = include_glob_pattern
        if include_glob_pattern is None:
            glob_pattern = "*.ipynb"
        included_paths = set(glob_method(glob_pattern))

        notebook_paths = sorted(included_paths - excluded_paths)
        for notebook_path in notebook_paths:

            execute_notebooks(
                notebook_path,
                bulk_params_list,
                output_prepend_components,
                output_append_components,
                output_dir,
                use_multiprocessing,
                **kwargs
            )            



def check_unequal_value_lengths(bulk_params: dict[str, list]) -> bool | dict:
    """
    Returns False if all list values are equal length. Returns a dict
    of value lengths otherwise.
    """
    acc = {}
    for k, v in bulk_params.items():
        try:
            acc.update({k: len(v)})
        except TypeError:
            raise ValueError(f"The values of the bulk_param keys must be lists, not: '{k: v}'")
    all_values = set(acc.values())
    if len(all_values) == 1:
        return False
    else:
        return acc
    

def convert_bulk_params_to_list(bulk_params: dict[str, list]):
    """
    Converts a dict of lists into a list of dicts.
    """
    iter_length = len(list(bulk_params.values())[0])
    bulk_params_list = []
    for idx in range(iter_length):
        inner_acc = {}
        for parameter_name, parameter_values in bulk_params.items():
            inner_acc.update({parameter_name: parameter_values[idx]})
        bulk_params_list.append(inner_acc)
    return bulk_params_list


def execute_notebooks(
    notebook_path: pathlib.Path,
    bulk_params_list: dict[str, Any],
    output_prepend_components: list[str],
    output_append_components: list[str],
    output_dir: pathlib.Path,
    use_multiprocessing: bool, 
    **kwargs
):
    total_variations = len(bulk_params_list)
    if not use_multiprocessing:
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            refresh_per_second=1,  # bit slower updates
        ) as progress:
            task_id = progress.add_task(notebook_path.name, total=total_variations)
            for idx, notebook_params in (list(enumerate(bulk_params_list))):
                execute_notebook(
                    notebook_filename=notebook_path,
                    notebook_params=notebook_params,
                    output_prepend_components=output_prepend_components,
                    output_append_components=output_append_components,
                    output_dir=output_dir,
                    **kwargs,
                )
                progress.update(task_id, completed=idx + 2)
    else:
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            refresh_per_second=1,  # bit slower updates
        ) as progress:
            # Multiprocessing approach inspired by 
            # https://www.deanmontgomery.com/2022/03/24/rich-progress-and-multiprocessing/
            futures = []  # keep track of the jobs
            with multiprocessing.Manager() as manager:
                _progress = manager.dict()
                overall_progress_task = progress.add_task(f"{notebook_path.name}", visible=True, total=total_variations)
                with ProcessPoolExecutor() as executor:
                    for idx, notebook_params in enumerate(bulk_params_list):
                        futures.append(
                            executor.submit(
                                execute_notebook, 
                                notebook_path,
                                notebook_params,
                                output_prepend_components,
                                output_append_components,
                                output_dir,
                                total_variations,
                                idx,
                                _progress,
                                overall_progress_task
                            )
                        )

                    # monitor the progress:
                    while (n_finished := sum([future.done() for future in futures])) < len(
                        futures
                    ):
                        progress.update(
                            overall_progress_task, completed=n_finished + 1
                        )


def execute_notebook(
    notebook_filename: pathlib.Path,
    notebook_params: dict,
    output_prepend_components: list[str],
    output_append_components: list[str],
    output_dir: pathlib.Path,
    total_variations: Optional[int] = None,
    current_iteration: Optional[int] = None,
    _progress: Optional[dict] = None,
    _task_id: Optional[str] = None,
    **kwargs,
):
    output_name = get_output_name(
        notebook_filename, 
        output_prepend_components, 
        output_append_components,
        notebook_params,
        current_iteration
    )
    pm.execute_notebook(
        notebook_filename,
        output_path=output_dir / output_name,
        parameters=notebook_params,
        progress_bar=False,
        cwd=str(notebook_filename.parent),
        **kwargs
    )
    if _progress is not None:
        _progress[_task_id] = {"progress": current_iteration, "total": total_variations}    


def get_output_name(
    notebook_filename: str,
    output_prepend_components: list[str] | None,
    output_append_components: list[str] | None,
    notebook_params: dict[str, Any],
    current_index: int
) -> str:
    """
    Returns the output name given the included components.
    """
    if output_prepend_components is None:
        output_prepend_components = [str(current_index)]
    if output_append_components is None:
        output_append_components = []
    prepends = [notebook_params.get(comp, comp) for comp in output_prepend_components]
    appends = [notebook_params.get(comp, comp) for comp in output_append_components]
    prepend_str = "-".join(prepends)
    append_str = "-".join(appends)
    notebook_filename = pathlib.Path(notebook_filename)
    output_name = "-".join([elem for elem in [prepend_str, notebook_filename.stem, append_str] if elem]) + notebook_filename.suffix
    return output_name