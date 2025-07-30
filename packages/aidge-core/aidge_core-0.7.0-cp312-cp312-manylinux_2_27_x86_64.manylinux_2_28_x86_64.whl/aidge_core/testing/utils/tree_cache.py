"""

Provide tree_update_from_cache(path) method which
minimize changes in a generated tree when files are
re-generated but identical.

It takes as argument a generated tree, and optionally a cache path.
Then it will update both the generated tree and the cache tree
to take the cache version of the files when identical, or the newly
generated one otherwise.

This is in particular useful for speeding up iterative compilation
when generating a source/build system tree.

For instance:
- first time, one generates a tree of files:
  - generated: path/{t1,t2,t3}
- then call tree_update_from_cache("path")
  - will generate: __cache_path/{t1,t2,t3}
  - and untouch: path/{t1,t2,t3}
- second time, re-generate a tree of file:
  - say generated files are identical: path/{t1,t2,t3}
- then call tree_update_from_cache("path")
  - will untouch in cache: __cache_path/{t1,t2,t3}
  - and reset to previous timestamps files: path/{t1,t2,t3}
- third time, re-generate again with some changes:
  - say t1 is identical, t2 content has changed and no t3: path/{t1,t2'}
- then call tree_update_from_cache("path")
  - will update t2' and remove t3 in cache: __cache_path/{t1,t2'}
  - and reset to previous timestamp t1: path/{t1,t2'}

Note that by default the `dir`/__cache_`name` cache path is used
for a given path `dir`/`name`.
Though it is also possible to have the cache path inside the generated tree,
in this case use for instance:

    tree_update_from_cache(path, Path(path) / "__cache_src")

For more evolved scenarii, specialize the provided FileTreeCache class.

"""


from pathlib import Path
import shutil
import sys
import filecmp
from typing import Optional, Union, List

from .tree_utils import tree_move, tree_remove


__all__ = [
    "FileTreeCache",
    "tree_update_from_cache",
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


class FileTreeCache():
    """
    Class for implementation of the file tree cache.
    Can be derived to changes for instance default cache name/tmp name prefixes
    or to specialize for other contexts.
    """
    default_cache_prefix = "__cache_"
    default_tmp_cache_prefix = "__tmp_cache_"
    default_tmp_prefix = "__tmp_"

    def __init__(self,
                 src_path: Union[str, Path],
                 cache_path: Optional[Union[str, Path]] = None
                 ) -> None:
        self.src_path = Path(src_path).absolute()
        self.cache_path = (
            Path(cache_path).absolute()
            if cache_path is not None else
            (self.src_path.parent /
             f"{self.default_cache_prefix}{self.src_path.name}")
        )
        ctx_msg = f"tree_cache: {src_path = }, {cache_path = }"
        assert self.src_path != self.cache_path, f"src_path and cache_path must differ on {ctx_msg}"
        assert not is_relative_to(self.src_path, self.cache_path), f"src_path must not be relative to cache_path on {ctx_msg}"
        self._tmp_path = (
            self.src_path.parent /
            f"{self.default_tmp_prefix}{self.src_path.name}")
        self._tmp_cache_path = (
            self.src_path.parent /
            f"{self.default_tmp_cache_prefix}{self.src_path.name}")

    @classmethod
    def _copytree_or_cache(cls, src_dir: Path, dst_dir: Path, cache_dir: Path, dst_cache_dir: Path) -> None:
        assert not dst_dir.exists()
        assert not dst_cache_dir.exists()
        assert src_dir.is_dir()
        assert not cache_dir.exists() or cache_dir.is_dir()
        assert not is_relative_to(cache_dir, src_dir)

        def copy_or_cache(src, dst):
            base_src = Path(src).relative_to(src_dir)
            cache_src = cache_dir / base_src
            base_dst = Path(dst).relative_to(dst_dir)
            cache_dst = dst_cache_dir / base_dst
            cache_dst.parent.mkdir(parents=True, exist_ok=True)
            if cache_src.exists() and filecmp.cmp(str(src), str(cache_src), shallow=False):
                shutil.copy2(str(cache_src), str(cache_dst))
                shutil.copy2(str(cache_src), dst)
            else:
                shutil.copy2(src, str(cache_dst))
                shutil.copy2(src, dst)
        shutil.copytree(str(src_dir), str(dst_dir), copy_function=copy_or_cache)

    def update_from_cache(self) -> None:
        assert self.src_path.exists(), f"src path must exist before swapping with cache"

        # Move cache path apart first as it may be relative to source path
        tree_move(self.cache_path, self._tmp_cache_path, ignore_missing=True, exist_ok=True)
        # Move source path apart before recreating merged source tree
        tree_move(self.src_path, self._tmp_path, exist_ok=True)

        # Manage the source/cache merge to the dst/dst_cahe with a variant of
        # copytree.
        self._copytree_or_cache(
            src_dir=self._tmp_path,
            dst_dir=self.src_path,
            cache_dir=self._tmp_cache_path,
            dst_cache_dir=self.cache_path,
        )

        # Remove tmp source path
        tree_remove(self._tmp_path)
        # Note that the tmp cache path may not exist
        tree_remove(self._tmp_cache_path, ignore_missing=True)


def tree_update_from_cache(
        src_path: Union[str, Path],
        cache_path: Optional[Union[str, Path]] = None) -> None:
    """
    Update from cache the current generation of a tree from the
    older generations, preserving file stamps when files contents are identical.

    :param src_path: str or Path object to the generated tree
    :param cache_path: optional str or Path object to the cache path,
    or defaults to: `cache_path = src_path.parent / f"__cache_{src_path.name}"`
    """
    FileTreeCache(src_path, cache_path).update_from_cache()
