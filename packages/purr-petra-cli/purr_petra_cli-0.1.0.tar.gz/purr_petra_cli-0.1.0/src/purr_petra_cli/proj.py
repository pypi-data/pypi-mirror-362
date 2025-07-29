from pathlib import Path
from typing import Optional
import typer
from purr_petra_cli.epsg import get_epsg_info


def is_valid_dir(fs_path: str) -> Optional[str]:
    """Validates and returns path as string if it exists

    Args:
        fs_path (str): A string path that may exist

    Returns:
        Optional[str]: Return Path string if it exists or None if not
    """
    path = Path(fs_path).resolve()
    if path.is_dir():
        return str(path)
    else:
        return None


def looks_like_petra_project(directory: str) -> bool:
    """Check if a directory looks like a Petra project

    Args:
        directory (str): The directory path to check.

    Returns:
        bool: True if the directory appears to be a Petra project.
    """
    dir_path = Path(directory)

    petra_db = dir_path / "DB"
    petra_parms = dir_path / "PARMS"
    petra_welldat = dir_path / "DB" / "WELL.DAT"

    return all(
        [
            petra_db.is_dir(),
            petra_parms.is_dir(),
            petra_welldat.is_file(),
        ]
    )


def validate_proj_dir(proj: str) -> Optional[str]:
    if not is_valid_dir(proj):
        raise typer.BadParameter(f"Not a valid directory: {proj}")

    if not looks_like_petra_project(proj):
        raise typer.BadParameter(f"Does not look like a Petra project: {proj}")

    return proj


def get_storage_epsg(proj: str):
    return get_epsg_info(proj)
