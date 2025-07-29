# numba-lock-cache

A Python package that monkey-patches Numba's caching mechanism to safely coordinate concurrent cache access using file locks.

## Why?

Numba’s function-level caching (`@jit(cache=True)`) is not concurrency-safe by default. This can lead to:

- Crashes when multiple processes load/write to the same cache
- Especially problematic on shared filesystems (e.g., NFS)

## Locking Mechanism

- Uses [`flufl.lock`](https://pypi.org/project/flufl.lock/) for file-based locking.
- Lock file is created next to the cache index file:
  `/path/to/cache/func.nbi.lock`
- Lock behavior:
  - Timeout to acquire: 60 minutes (configurable)
  - Lifetime: `None` (lock persists until released)
  - NFS-safe: relies on atomic file creation

## Installation

```bash
pip install numba-lock-cache
```

## How to use it

Just import the patch Numba in your application:

```python
import numba_cache_lock

numba_cache_lock.patch_numba_cache()

from numba import jit

@jit(cache=True)
def my_func(x):
    return x * 2
```

By default, `patch_numba_cache` will hold a lock for 1 hour in the worst case.
One can change this value by assigning the `lifetime=` keyword argument to a
`timedelta` object.
