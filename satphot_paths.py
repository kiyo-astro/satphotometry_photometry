"""
Path settings shared by the SatPhotometry notebooks.

Machine-specific locations are read from ``paths.json`` placed next to this
file (not committed to git) or from environment variables. Everything falls
back to directories inside the project folder.

paths.json example::

    {
        "images": "/path/to/observation/images",
        "input":  "input",
        "output": "output",
        "work":   "/path/to/large/scratch",
        "solve_field_dir": "~/astrometry/bin"
    }

Keys
----
images          Root of raw observation data (SER / FITS captures).
input           Small input files kept with the project (default: ./input).
output          Products: magzero, lightcurve, lightcurve_analysis ...
                (default: ./output).
work            Large intermediate files written by the GEO pipelines
                (fits_raw, fits_solved, ...). Default: same as output.
solve_field_dir Directory containing astrometry.net ``solve-field``. It is
                prepended to PATH so that a non-standard install is found.

Environment variables ``SATPHOT_IMAGES``, ``SATPHOT_INPUT``, ``SATPHOT_OUTPUT``,
``SATPHOT_WORK`` and ``SATPHOT_SOLVE_FIELD_DIR`` override paths.json.
Relative paths are resolved against the project folder.
"""

import json
import os
import sys
from pathlib import Path

PATH_project = Path(__file__).resolve().parent

_config_file = PATH_project / "paths.json"

if _config_file.is_file():
    with _config_file.open("r", encoding="utf-8") as _file:
        _config = json.load(_file)
else:
    _config = {}


def _resolve(key, default):
    value = os.environ.get(f"SATPHOT_{key.upper()}") or _config.get(key)

    if not value:
        return Path(default)

    path = Path(value).expanduser()

    if not path.is_absolute():
        path = PATH_project / path

    return path


PATH_images = _resolve("images", PATH_project / "images")
PATH_input = _resolve("input", PATH_project / "input")
PATH_output = _resolve("output", PATH_project / "output")
PATH_work = _resolve("work", PATH_output)

_solve_field_dir = (
    os.environ.get("SATPHOT_SOLVE_FIELD_DIR")
    or _config.get("solve_field_dir")
)


def _prepend_to_path(directory):
    directory = str(Path(directory).expanduser())
    entries = os.environ.get("PATH", "").split(os.pathsep)

    if directory not in entries:
        os.environ["PATH"] = directory + os.pathsep + os.environ.get("PATH", "")


if _solve_field_dir:
    _solve_field_dir = str(Path(_solve_field_dir).expanduser())
    _prepend_to_path(_solve_field_dir)

# Helper scripts started by solve-field (uniformize, removelines, ...) run
# ``python3`` from PATH. Put this kernel's interpreter first so they use the
# same environment (numpy, astrometry.util) as the notebook.
_prepend_to_path(Path(sys.executable).parent)


def show_paths():
    """Print the resolved paths."""
    print(f"PATH_project : {PATH_project}")
    print(f"PATH_images  : {PATH_images}")
    print(f"PATH_input   : {PATH_input}")
    print(f"PATH_output  : {PATH_output}")
    print(f"PATH_work    : {PATH_work}")
    print(f"solve-field  : {_solve_field_dir or '(PATH)'}")


__all__ = [
    "Path",
    "PATH_project",
    "PATH_images",
    "PATH_input",
    "PATH_output",
    "PATH_work",
    "show_paths",
]
