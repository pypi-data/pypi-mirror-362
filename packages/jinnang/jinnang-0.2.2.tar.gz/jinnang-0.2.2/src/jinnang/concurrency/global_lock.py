"""Global Lock Manager for Resource Synchronization

This module provides a professional, unified lock system that ensures
exclusive access to shared resources across both synchronous and asynchronous contexts.

Key features:
- Unified lock interface for sync and async operations
- Thread-safe and async-safe operations
- Lightweight and efficient design
- Context manager support
- Clean decorator interface for easy adoption
- Optional key-based resource isolation
"""

import asyncio
import threading
import weakref
from typing import Callable, TypeVar, Optional, Dict, Any, Union, ContextManager, AsyncContextManager, List
from functools import wraps
from contextlib import contextmanager, asynccontextmanager

T = TypeVar('T')


class UnifiedLock:
    """
    A unified lock that handles both sync and async operations efficiently.
    
    This class provides a single lock interface that works seamlessly in both
    synchronous and asynchronous contexts without the overhead of complex metrics.
    """
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or "unnamed"
        self._thread_lock = threading.RLock()
        self._async_lock = None  # Created lazily when needed
    
    def __enter__(self):
        self._thread_lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._thread_lock.release()

    async def __aenter__(self):
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        await self._async_lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._async_lock.release()
    
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """Acquire the lock in synchronous context."""
        if timeout is not None:
            return self._thread_lock.acquire(blocking=blocking, timeout=timeout)
        return self._thread_lock.acquire(blocking=blocking)
    
    def release(self):
        """Release the lock in synchronous context."""
        self._thread_lock.release()
    
    async def acquire_async(self) -> None:
        """Acquire the lock in asynchronous context."""
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        await self._async_lock.acquire()
    
    def release_async(self):
        """Release the lock in asynchronous context."""
        if self._async_lock is not None:
            self._async_lock.release()


class GlobalLockManager:
    """
    A professional global lock manager with key-based resource isolation.
    
    This manager maintains separate locks for different resource keys, allowing
    fine-grained control over resource access while preventing unnecessary blocking
    between unrelated operations.
    
    Features:
    - Key-based lock isolation
    - Thread-safe and async-safe operations
    - Multiple Pythonic interfaces (decorators, context managers)
    - Lightweight and efficient design
    """
    
    def __init__(self):
        self._locks: Dict[str, UnifiedLock] = {}
        self._locks_lock = threading.Lock()  # Protects the _locks dict itself
    
    def _get_or_create_lock(self, key: str) -> UnifiedLock:
        """Thread-safely get or create a lock for the given key."""
        with self._locks_lock:
            if key not in self._locks:
                self._locks[key] = UnifiedLock(name=key)
            return self._locks[key]
    
    @contextmanager
    def lock(self, key: str, timeout: Optional[float] = None):
        """
        Context manager for synchronous lock acquisition.
        
        Args:
            key: Unique identifier for the resource being protected
            timeout: Lock acquisition timeout in seconds (None for no timeout)
            
        Yields:
            The lock object
            
        Raises:
            TimeoutError: If lock acquisition times out
        """
        resource_lock = self._get_or_create_lock(key)
        acquired = resource_lock.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError(f"Failed to acquire lock for key '{key}' within {timeout}s")
        try:
            yield resource_lock
        finally:
            resource_lock.release()
    
    @asynccontextmanager
    async def alock(self, key: str, timeout: Optional[float] = None):
        """
        Async context manager for asynchronous lock acquisition.
        
        Args:
            key: Unique identifier for the resource being protected
            timeout: Lock acquisition timeout in seconds (None for no timeout)
            
        Yields:
            The lock object
            
        Raises:
            asyncio.TimeoutError: If lock acquisition times out
        """
        resource_lock = self._get_or_create_lock(key)
        if timeout is not None:
            async with asyncio.timeout(timeout):
                async with resource_lock:
                    yield resource_lock
        else:
            async with resource_lock:
                yield resource_lock
    
    def execute_sync(
        self,
        lock_key: str,
        func: Callable[..., T],
        func_args: tuple = (),
        func_kwargs: Optional[dict] = None,
        lock_timeout: Optional[float] = None,
    ) -> T:
        """
        Execute a synchronous function with lock protection.
        
        Args:
            lock_key: Unique identifier for the resource being protected
            func: The function to execute
            func_args: Positional arguments for the function
            func_kwargs: Keyword arguments for the function
            lock_timeout: Lock acquisition timeout in seconds
            
        Returns:
            The result of the function
        """
        if func_kwargs is None:
            func_kwargs = {}
        with self.lock(lock_key, timeout=lock_timeout):
            return func(*func_args, **func_kwargs)
    
    async def execute_async(
        self,
        lock_key: str,
        func: Callable[..., T],
        func_args: tuple = (),
        func_kwargs: Optional[dict] = None,
        lock_timeout: Optional[float] = None,
    ) -> T:
        """
        Execute an asynchronous function with lock protection.
        
        Args:
            lock_key: Unique identifier for the resource being protected
            func: The async function to execute
            func_args: Positional arguments for the function
            func_kwargs: Keyword arguments for the function
            lock_timeout: Lock acquisition timeout in seconds
            
        Returns:
            The result of the function
        """
        if func_kwargs is None:
            func_kwargs = {}
        async with self.alock(lock_key, timeout=lock_timeout):
            return await func(*func_args, **func_kwargs)

    def get_lock(self, key: str) -> UnifiedLock:
        """Get the lock object for a specific key (for advanced usage)."""
        return self._get_or_create_lock(key)
    
    def list_keys(self) -> List[str]:
        """List all currently registered lock keys."""
        with self._locks_lock:
            return list(self._locks.keys())
    
    def cleanup_unused_locks(self):
        """Remove locks that are not currently held (for memory management)."""
        with self._locks_lock:
            # Use weak references to detect unused locks
            keys_to_remove = []
            for key, lock in self._locks.items():
                # Check if lock is not currently held
                async_locked = lock._async_lock.locked() if lock._async_lock is not None else False
                if (not hasattr(lock._thread_lock, '_owner') or lock._thread_lock._owner is None) and \
                   (not async_locked):
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self._locks[key]


# Global singleton instance
global_lock_manager = GlobalLockManager()


def with_global_lock(
    key: str,
    *,
    timeout: Optional[float] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for automatic global lock management with key-based isolation.
    
    This decorator provides a clean, professional interface for protecting
    functions with global locks. Each key represents an independent resource,
    allowing fine-grained concurrency control.
    
    Args:
        key: Unique identifier for the resource being protected
        timeout: Lock acquisition timeout in seconds (None for no timeout)
    
    Returns:
        Decorated function with lock protection
    
    Example:
        @with_global_lock("transformer_model")
        def load_model():
            return load_transformer_model()
        
        @with_global_lock("database", timeout=30.0)
        async def update_records():
            await database.update()
        
        @with_global_lock("file_processor")
        def process_files(files):
            return [process_file(f) for f in files]
    """
    def decorator(target_func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(target_func):
            @wraps(target_func)
            async def async_wrapper(*args, **kwargs) -> T:
                return await global_lock_manager.execute_async(
                    lock_key=key,
                    func=target_func,
                    func_args=args,
                    func_kwargs=kwargs,
                    lock_timeout=timeout
                )
            return async_wrapper
        else:
            @wraps(target_func)
            def sync_wrapper(*args, **kwargs) -> T:
                return global_lock_manager.execute_sync(
                    lock_key=key,
                    func=target_func,
                    func_args=args,
                    func_kwargs=kwargs,
                    lock_timeout=timeout
                )
            return sync_wrapper
    
    return decorator


# Convenience functions for direct usage
def global_lock(key: str, timeout: Optional[float] = None):
    """
    Get a synchronous context manager for global lock.
    
    Args:
        key: Unique identifier for the resource being protected
        timeout: Lock acquisition timeout in seconds
    
    Returns:
        Context manager for the lock
    
    Example:
        with global_lock("shared_resource"):
            # Critical section
            modify_shared_resource()
    """
    return global_lock_manager.lock(key, timeout=timeout)


def global_alock(key: str, timeout: Optional[float] = None):
    """
    Get an asynchronous context manager for global lock.
    
    Args:
        key: Unique identifier for the resource being protected
        timeout: Lock acquisition timeout in seconds
    
    Returns:
        Async context manager for the lock
    
    Example:
        async with global_alock("shared_resource"):
            # Critical section
            await modify_shared_resource_async()
    """
    return global_lock_manager.alock(key, timeout=timeout)


# Alias for backward compatibility and convenience
lock = global_lock
alock = global_alock