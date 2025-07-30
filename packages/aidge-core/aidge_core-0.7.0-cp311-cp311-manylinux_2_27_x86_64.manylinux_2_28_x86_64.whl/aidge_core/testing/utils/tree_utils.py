"""

Provide utility function for file trees manipulations.

"""

import shutil
import sys
from pathlib import Path
from typing import Union


__all__ = [
    "tree_move",
    "tree_remove",
]


def is_relative_to(path: Path, other: Path) -> bool:
    """
    Dynamically choose implementation based on Python version
    """
    # Python 3.9+
    if sys.version_info >= (3, 9):
        return path.is_relative_to(other)

    # Python 3.8 and earlier
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def tree_remove(
        path: Union[str, Path],
        ignore_missing: bool = False,
) -> None:
    """
    Remove the full tree at path.
    Optionally ignore if the path does not exist when ignore_missing is True.

    :param path: str or Path object to the directory path
    :param ignore_missing: if True will return early is path does not exists
    """
    path = Path(path)
    ctx_msg = f"tree_remove: : {path = }"
    assert ignore_missing or path.exists(), f"path must exists when ignore_missing is False on {ctx_msg}"
    if ignore_missing and not path.exists():
        return
    shutil.rmtree(path)


def tree_move(
        src_path: Union[str, Path],
        dst_path: Union[str, Path],
        ignore_missing: bool = False,
        exist_ok: bool = False,
) -> None:
    """
    Move the whole src_path file tree to dst_path.
    Optionally does nothing if the src path does not exists and ignore_missing is True.
    Optionally the full dst_path will be removed first when exists_ok is True.

    :param src_path: str or Path object to the source directory path
    :param dst_path: str or Path object to the new path name for the source directory
    :param ignore_missing: if True will return early is src_path does not exists
    :param exist_ok: if True will first erase the new path name if it exists
    """
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    ctx_msg = f"tree_move: : {src_path = }, {dst_path = }"
    assert ignore_missing or src_path.exists(), f"src_path must exists when ignore_missing is False on {ctx_msg}"
    assert exist_ok or not dst_path.exists(), f"dst_path must not exists when exist_ok is False on {ctx_msg}"
    assert src_path != dst_path, f"paths must not be identical on {ctx_msg}"
    assert not is_relative_to(dst_path, src_path), f"dst_path must not be relative to src_path on {ctx_msg}"
    assert not is_relative_to(src_path, dst_path), f"src_path must not be relative to dst_path on {ctx_msg}"
    if ignore_missing and not src_path.exists():
        return
    if exist_ok and dst_path.exists():
        shutil.rmtree(dst_path)
    shutil.move(src_path, dst_path)
