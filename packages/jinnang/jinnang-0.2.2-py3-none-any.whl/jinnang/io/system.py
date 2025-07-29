import os
import sys
import shutil
import contextlib
import threading
from io import StringIO
from typing import Optional, Union
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

from jinnang.concurrency.global_lock import global_lock

PathType = Union[str, Path]

# Global thread-local storage for suppress_c_stdout_stderr
_suppress_thread_local = threading.local()

@contextlib.contextmanager
def suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    """
    A robust context manager that redirects C-level stdout and/or stderr to /dev/null.
    
    This implementation is thread-safe and handles async/recursive scenarios properly
    by ensuring file descriptors are always restored even in exceptional cases.
    
    Args:
        suppress_stdout: Whether to suppress stdout (default: True)
        suppress_stderr: Whether to suppress stderr (default: False)
    
    Raises:
        OSError: If file descriptor operations fail
    """
    # Use global lock to prevent race conditions in multi-threaded scenarios
    with global_lock("suppress_c_stdout_stderr"):
        # Initialize thread-local storage if needed
        if not hasattr(_suppress_thread_local, 'nesting_level'):
            _suppress_thread_local.nesting_level = 0
            _suppress_thread_local.active_suppressions = []
        
        _suppress_thread_local.nesting_level += 1
        current_level = _suppress_thread_local.nesting_level
        
        # Only redirect at the first level to avoid conflicts
        if current_level > 1:
            try:
                yield
            finally:
                _suppress_thread_local.nesting_level -= 1
            return
        
        # Flush Python-level buffers before redirecting
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except (OSError, ValueError):
            # Handle cases where stdout/stderr might be closed or invalid
            pass
        
        # Store original file descriptors
        redirected_fds = {}
        null_fd = None
        
        try:
            # Open /dev/null once and reuse
            null_fd = os.open(os.devnull, os.O_WRONLY)
            
            # Redirect stdout if requested
            if suppress_stdout:
                try:
                    stdout_fd = sys.stdout.fileno()
                    # Duplicate the original file descriptor before redirecting
                    original_stdout = os.dup(stdout_fd)
                    redirected_fds['stdout'] = {
                        'original': original_stdout,
                        'target': stdout_fd
                    }
                    # Redirect to /dev/null
                    os.dup2(null_fd, stdout_fd)
                except (OSError, ValueError, AttributeError) as e:
                    # Clean up partial state on error
                    if 'stdout' in redirected_fds:
                        try:
                            os.close(redirected_fds['stdout']['original'])
                        except OSError:
                            pass
                        del redirected_fds['stdout']
            
            # Redirect stderr if requested
            if suppress_stderr:
                try:
                    stderr_fd = sys.stderr.fileno()
                    # Duplicate the original file descriptor before redirecting
                    original_stderr = os.dup(stderr_fd)
                    redirected_fds['stderr'] = {
                        'original': original_stderr,
                        'target': stderr_fd
                    }
                    # Redirect to /dev/null
                    os.dup2(null_fd, stderr_fd)
                except (OSError, ValueError, AttributeError) as e:
                    # Clean up partial state on error
                    if 'stderr' in redirected_fds:
                        try:
                            os.close(redirected_fds['stderr']['original'])
                        except OSError:
                            pass
                        del redirected_fds['stderr']
            
            # Execute the wrapped code
            yield
            
        except Exception as e:
            # Handle any setup errors
            # Restore file descriptors if any were redirected
            restoration_errors = []
            
            # Restore stderr first, then stdout (reverse order)
            for stream_name in ['stderr', 'stdout']:
                if stream_name in redirected_fds:
                    fd_info = redirected_fds[stream_name]
                    try:
                        # Restore the original file descriptor
                        os.dup2(fd_info['original'], fd_info['target'])
                    except OSError as restore_e:
                        restoration_errors.append(f"Failed to restore {stream_name}: {restore_e}")
                    
                    try:
                        # Close the duplicated file descriptor
                        os.close(fd_info['original'])
                    except OSError as close_e:
                        restoration_errors.append(f"Failed to close {stream_name} backup fd: {close_e}")
            
            # Close /dev/null file descriptor
            if null_fd is not None:
                try:
                    os.close(null_fd)
                except OSError as null_e:
                    restoration_errors.append(f"Failed to close /dev/null fd: {null_e}")
            
            # Reset nesting level
            _suppress_thread_local.nesting_level -= 1
            
            # Log any restoration errors
            if restoration_errors:
                print(f"Warning: File descriptor restoration errors during exception: {'; '.join(restoration_errors)}")
            
            # Re-raise the original exception
            raise
        
        finally:
            # Restore file descriptors in reverse order with robust error handling
            restoration_errors = []
            
            # Restore stderr first, then stdout (reverse order)
            for stream_name in ['stderr', 'stdout']:
                if stream_name in redirected_fds:
                    fd_info = redirected_fds[stream_name]
                    try:
                        # Restore the original file descriptor
                        os.dup2(fd_info['original'], fd_info['target'])
                    except OSError as e:
                        restoration_errors.append(f"Failed to restore {stream_name}: {e}")
                    
                    try:
                        # Close the duplicated file descriptor
                        os.close(fd_info['original'])
                    except OSError as e:
                        restoration_errors.append(f"Failed to close {stream_name} backup fd: {e}")
            
            # Close /dev/null file descriptor
            if null_fd is not None:
                try:
                    os.close(null_fd)
                except OSError as e:
                    restoration_errors.append(f"Failed to close /dev/null fd: {e}")
            
            # Reset nesting level
            _suppress_thread_local.nesting_level -= 1
            
            # Log any restoration errors (but don't raise to avoid masking original exceptions)
            if restoration_errors:
                # Use print instead of logger to avoid potential circular dependencies
                print(f"Warning: File descriptor restoration errors: {'; '.join(restoration_errors)}")
            
            # Flush again to ensure any buffered output is written
            try:
                sys.stdout.flush()
                sys.stderr.flush()
            except (OSError, ValueError):
                pass

@contextlib.contextmanager
def suppress_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    """A context manager that redirects Python-level stdout and/or stderr to StringIO"""
    old_stdout, old_stderr = sys.stdout, sys.stderr
    if suppress_stdout:
        sys.stdout = StringIO()
    if suppress_stderr:
        sys.stderr = StringIO()

    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr


def get_worker_num_for_io_bounded_task(user_defined: Optional[int] = None) -> int:
    """Calculate optimal number of workers for IO-bound tasks"""
    if user_defined is not None:
        return max(1, min(user_defined, 32))  # Enforce reasonable bounds
    try:
        cpu_count = os.cpu_count() or 4
        calculated = min(32, (cpu_count * 1))
        return max(4, calculated)
    except:
        return 8

def create_relative_symlink(target_path: str, link_folder: str):
    """
    Create a relative symbolic link inside 'link_folder' pointing to 'target_path'.
    The name of the symbolic link will be the same as the name of the target.
    Args:
    target_path (str): The path to the target file or directory.
    link_folder (str): The folder where the symbolic link will be created.
    """
    assert target_path and link_folder, \
            f'Both target_path, link_folder are a must. got target_path={target_path}; link_folder={link_folder}'
    target_path = os.path.abspath(target_path)
    link_folder = os.path.abspath(link_folder)
    os.makedirs(link_folder, exist_ok=True)
    link_name = os.path.basename(target_path)
    rel_path = os.path.relpath(target_path, link_folder)
    link_path = os.path.join(link_folder, link_name)
    try:
        os.symlink(rel_path, link_path)
    except Exception as e:
        print(f"Fail to build symlink at {str(rel_path)} for {str(target_path)}. Details: {e}")

def safe_delete(file_path):
    if not os.path.isfile(file_path):
        return
    try:
        os.remove(file_path)
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in safe_delete: {type(e).__name__} - {e}")

def safe_move(src: str, dst: str) -> bool:
    try:
        if not src or not dst:
            raise ValueError(f'Both src and dst are required. Got src={src}, dst={dst}')
        src_path = os.path.abspath(src)
        dst_path = os.path.abspath(dst)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f'Source file does not exist: {src_path}')
        if not os.path.isfile(src_path):
            raise ValueError(f'Source is not a file: {src_path}')
        if os.path.isdir(dst_path):
            dst_path = os.path.join(dst_path, os.path.basename(src_path))
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        try:
            os.rename(src_path, dst_path)
        except OSError:
            import shutil
            shutil.copy2(src_path, dst_path)
            os.remove(src_path)
        return True
    except Exception as e:
        print(f"Failed to move file: {e}")
        return False
    

def copy_with_meta(src: PathType, dst: PathType) -> bool:
    """
    Safely copy a file from src to dst while preserving metadata.
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Returns:
        bool: True if operation succeeded, False otherwise
    """
    try:
        # Validate inputs
        if not src or not dst:
            raise ValueError(f'Both src and dst are required. Got src={src}, dst={dst}')
            
        src_path = Path(src) if not isinstance(src, Path) else src
        dst_path = Path(dst) if not isinstance(dst, Path) else dst
        
        # Check if source exists
        if not src_path.exists():
            raise FileNotFoundError(f'Source file does not exist: {src_path}')
            
        # Check if source is a file
        if not src_path.is_file():
            raise ValueError(f'Source is not a file: {src_path}')
            
        # Create parent directory if needed
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(src_path, dst_path)
        
        # Handle metadata
        try:
            inplace_overwrite_meta(src_path, dst_path)
        except Exception as meta_error:
            logger.debug(f'Failed to copy metadata from {src_path} to {dst_path}: {meta_error}')
            # The file copy succeeded even if metadata failed, so we don't return False here
            
        return True
        
    except Exception as e:
        logger.debug(f'Failed to copy file from {src} to {dst}: {e}', exc_info=True)
        return False

def inplace_overwrite_meta(src: PathType, target: PathType):
    # Get timestamps from the source file
    stat_src = os.stat(src)
    atime = stat_src.st_atime  # Access time
    mtime = stat_src.st_mtime  # Modification time

    # Apply timestamps to the destination file
    os.utime(target, (atime, mtime))
