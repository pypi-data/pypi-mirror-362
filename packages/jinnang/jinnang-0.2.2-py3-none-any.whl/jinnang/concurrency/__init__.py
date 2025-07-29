"""
Concurrency utilities for AI Album.

This module provides thread-safe and async-safe utilities for managing
concurrent operations across the application.
"""

# For explicit imports, use:
# from jinnang.concurrency.global_lock import global_lock, global_alock, with_global_lock
# from jinnang.concurrency.global_lock import GlobalLockManager, global_lock_manager

from .global_lock import (
    global_lock,
    global_alock,
    with_global_lock
)

__all__ = [
    'global_lock',
    'global_alock', 
    'with_global_lock'
]