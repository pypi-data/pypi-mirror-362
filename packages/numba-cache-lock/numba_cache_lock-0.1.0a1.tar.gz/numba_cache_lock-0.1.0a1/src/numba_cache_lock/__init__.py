import os
from datetime import timedelta
from typing import Final

from flufl.lock import Lock
from numba.core.caching import FunctionCache
from numba.core.target_extension import (
    dispatcher_registry,
    target_registry,
)

__all__ = [
    "monkey_patch_caching",
]


DEFAULT_LOCK_LIFETIME: Final = timedelta(hours=1)


class FileLockFunctionCache(FunctionCache):
    def __init__(self, py_func, lifetime=None):
        super().__init__(py_func)
        self._lifetime = lifetime

    def get_lock(self):
        path = self._cache_file._cache_path
        index_name = self._cache_file._index_name
        lock_name = f"{index_name}.lock"
        lock_path = os.path.join(path, lock_name)
        return Lock(lock_path, lifetime=self._lifetime)

    def load_overload(self, sig, target_context):
        global_compiler_file_lock = self.get_lock()
        with global_compiler_file_lock:
            return super().load_overload(sig, target_context)

    def save_overload(self, sig, data):
        global_compiler_file_lock = self.get_lock()
        with global_compiler_file_lock:
            return super().save_overload(sig, data)


def patch_numba_cache(lifetime: timedelta = DEFAULT_LOCK_LIFETIME):
    dispatcher = dispatcher_registry[target_registry["CPU"]]

    def enable_caching(self):
        self._cache = FileLockFunctionCache(self.py_func, lifetime=lifetime)

    dispatcher.enable_caching = enable_caching


try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]

__version__ = version("numba_cache_lock")
