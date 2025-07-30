import json
from typing import Optional, Any
from typing_extensions import Annotated
import pathlib

import typer
from .millrun import execute_run


def _parse_json(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        return json.load(file)

APP_INTRO = typer.style(
"""
AISC sections database W-section selection tool (2023-05-28)
""",
    fg=typer.colors.BRIGHT_YELLOW,
    bold=True,
)

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help=APP_INTRO,
    # pretty_exceptions_enable=False,
    pretty_exceptions_show_locals=False
)

@app.command(
    name='run',
    help="Executes a notebook or directory of notebooks using the provided bulk parameters JSON file",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def run(
    notebook_dir_or_file: Annotated[str, typer.Argument(
        help="Path to a notebook file or a directory containing notebooks.")
    ],
    params: Annotated[str, typer.Argument(
        help=("JSON file that contains parameters for notebook execution. "
              "Can either be a 'list of dict' or 'dict of list'."),
        callback=lambda value: _parse_json(value),
        )
    ],
    output_dir: Annotated[Optional[str], typer.Option(
        help=("Directory to place output files into. If not provided"
              " the file directory will be used."),
        )
    ] = None,
    prepend: Annotated[Optional[str], typer.Option(
        help=("Prepend components to use on output filename."
              "Can use dict keys from 'params' which will be evaluated."
              "(Comma-separated values)."),
        callback=lambda x: x.split(",") if x else None
        )
    ] = None,
    append: Annotated[Optional[str], typer.Option(
        help=("Append components to use on output filename."
              "Can use dict keys from 'params' which will be evaluated."
              "(Comma-separated values)."),
        callback=lambda x: x.split(",") if x else None
        )
    ] = None,
    recursive: bool = False,
    exclude_glob_pattern: Optional[str] = None,
    include_glob_pattern: Optional[str] = None,
):
    if output_dir is not None:
        output_dir = pathlib.Path(output_dir)
    else:
        output_dir = pathlib.Path.cwd()
    execute_run(
        notebook_dir_or_file,
        params,
        output_dir,
        prepend,
        append,
        recursive,
        exclude_glob_pattern,
        include_glob_pattern,
        use_multiprocessing=True
        # **kwargs
    )


if __name__ == "__main__":
    app()