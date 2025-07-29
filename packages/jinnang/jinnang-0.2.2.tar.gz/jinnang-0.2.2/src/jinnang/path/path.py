import functools
import platform
import time
import pytz
import os
import logging
from datetime import datetime
from typing import TypeVar

from jinnang.common.hash import partial_file_hash
from jinnang.verbosity.verbosity import Verbosity
from typing import TypeVar, Type, Dict, Any, Optional, List, ClassVar

T = TypeVar('T')

# a decorator
def ensure_unique_path(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        original_path = func(*args, **kwargs)
        if not original_path:
            return None

        # Ensure the path is unique by appending a number if it already exists
        base, extension = os.path.splitext(original_path)
        counter = 1
        unique_path = original_path
        while os.path.exists(unique_path):
            unique_path = f"{base}-{counter}{extension}"
            counter += 1

        return unique_path
    return wrapper


class RelPathSeeker:
    """
    A utility class for resolving file paths relative to a calling module.

    This class provides methods to search for a given filename within a set of
    prioritized locations based on a provided caller module path.

    Example:
        ```python
        # Assuming 'my_script.py' is in /project/src/ and 'config.json' is in /project/conf/
        # and the current working directory is /project/

        # To find 'config.json' relative to 'my_script.py'
        config_seeker = RelPathSeeker(
            filename="conf/sample_config.yml",
            caller_module_path="/project/src/my_script.py"
        )
        print(config_seeker.filepath) # Expected: /project/conf/sample_config.yml

        # To find a file in the current working directory
        readme_seeker = RelPathSeeker(
            filename="README.md",
            caller_module_path=__file__ # Or None, if current working directory is sufficient
        )
        print(readme_seeker.filepath) # Expected: /project/README.md
        ```
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL,
        **kwargs: Any
    ):
        if not (filename or caller_module_path):
            raise ValueError(
                "At least one of 'filename' or 'caller_module_path' must be provided."
            )

        try:
            self.loaded_filepath = self.resolve_file_path(
                filename=filename,
                caller_module_path=caller_module_path,
                verbosity=verbosity
            )
        except FileNotFoundError:
            self.loaded_filepath = None
        
    @property
    def filepath(self):
        return self.loaded_filepath

    @staticmethod
    def _get_search_paths(
        filename: str = "",
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL
    ) -> List[str]:
        """Generates a list of potential file paths based on the caller's module path.

        This static method constructs a prioritized list of absolute file paths
        where a given filename might be located, relative to the calling module.

        Args:
            filename (str): The name of the file to search for.
            caller_module_path (Optional[str]): The `__file__` attribute of the
                calling module, used to determine a relative search path.
            verbosity (Verbosity): The verbosity level for logging.

        Returns:
            List[str]: A list of absolute paths where the file might exist,
            ordered by search priority.
        """
        module_path = caller_module_path or __file__
        locations = [
            os.path.dirname(module_path),
            os.path.join(os.path.dirname(module_path), '..'),
            os.path.join(os.path.dirname(module_path), '../..'),
            '.'
        ]
        potential_paths = [os.path.join(directory, filename) for directory in locations]
        if verbosity >= Verbosity.DETAIL:
            logging.debug(f"Potential search paths for '{filename}': {potential_paths}")
        return potential_paths

    @staticmethod
    def resolve_file_path(
        filename: str = "",
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL
    ) -> str:
        """Resolves the absolute path to a file based on the caller's module path.

        This static method attempts to find a file by searching through a series
        of prioritized locations relative to the calling module.

        Args:
            filename (str): The name of the file to resolve.
            caller_module_path (Optional[str]): The `__file__` attribute of the
                calling module, used to determine a relative search path.
            verbosity (Verbosity): The verbosity level for logging.

        Returns:
            str: The absolute path to the resolved file.

        Raises:
            FileNotFoundError: If the file cannot be found in any of the specified
                or default search locations.
        """
        if verbosity >= Verbosity.DETAIL:
            logging.debug(f"Searching for filename: {filename}")

        potential_paths = RelPathSeeker._get_search_paths(
            filename=filename,
            caller_module_path=caller_module_path,
            verbosity=verbosity
        )

        for potential_path in potential_paths:

            if os.path.exists(potential_path) and os.path.isfile(potential_path):
                if verbosity >= Verbosity.ONCE:
                    logging.info(f"Found file: {potential_path}")
                return potential_path

        error_message = f"Could not find {filename} in any of these locations: {potential_paths}"
        if verbosity >= Verbosity.ONCE:
            logging.error(error_message)
        raise FileNotFoundError(error_message)

class MyPath:

    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        """ Extracts the basename from a given file path. """
        return os.path.splitext(os.path.basename(self.path))[0]

    @property
    def extension(self):
        """ Extracts the extension from a given file path, without the dot. """
        return os.path.splitext(self.path)[1][1:]

    @property
    def abspath(self):
        return os.path.abspath(os.path.expanduser(self.path))

    @property
    def hash(self):
        return partial_file_hash(self.path)

    @property
    def timezone(self):
        return pytz.timezone('Asia/Shanghai')

    @property
    def timestamp(self):
        return get_file_timestamp(self.path)

    @property
    def timestr(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, self.timezone).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def date(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, self.timezone).strftime('%y%m%d')

    @property
    @functools.lru_cache(maxsize=8192)
    def time_of_a_day(self):
        """
        Return a human-readable time of day for a given timestamp.
        """
        if self.timestamp is None:
            return None

        local_dt = datetime.fromtimestamp(self.timestamp, self.timezone)
        hour = local_dt.hour

        # Define time periods with explicit start and end hours for clarity.
        time_periods = [
            (0, 5, 'Midnight'),
            (5, 12, 'Morning'),
            (12, 13, 'Noon'),      # Noon is a special case at exactly 12:00.
            (13, 17, 'Afternoon'),
            (17, 21, 'Evening'),
            (21, 24, 'Night')
        ]

        for start_hour, end_hour, period in time_periods:
            if start_hour <= hour < end_hour:
                return period

        return 'Night'  # Fallback, though all hours 0-23 should be covered.

@functools.lru_cache(maxsize=None)
def get_file_timestamp(path):
    timestamp = None
    try:
        stat_info = os.stat(path)
        if platform.system() == 'Windows':
            timestamp = stat_info.st_ctime
        else:
            try:
                timestamp = stat_info.st_birthtime  # macOS
            except AttributeError:
                try:
                    timestamp = stat_info.st_mtime  # Linux/Unix fallback
                except AttributeError:
                    timestamp = time.time()
    except (OSError, AttributeError):
        timestamp = time.time()
    return timestamp

def timestamp_to_date(timestamp, fstr='%y%m%d', timezone='Asia/Shanghai'):
    utc_dt = datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
    my_tz = pytz.timezone(timezone)
    my_dt = utc_dt.astimezone(my_tz)
    return my_dt.strftime(fstr)