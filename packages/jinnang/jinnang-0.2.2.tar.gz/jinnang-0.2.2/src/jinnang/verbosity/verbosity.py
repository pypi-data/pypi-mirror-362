"""Module for controlling output verbosity levels."""

from enum import IntEnum

class Verbosity(IntEnum):
    """Enumeration for controlling output verbosity levels.
    
    This enum provides standardized verbosity levels that can be used
    throughout the application to control the amount of information displayed
    to users or logged to files.
    
    Levels:
        SILENT (0): No output
        ONCE (1): Show only once or minimal information
        DETAIL (2): Show detailed information
        FULL (3): Show all available information
        TMP (4): Temporary/debug level (not for production use)
    """
    SILENT = 0
    ONCE = 1
    DETAIL = 2
    FULL = 3
    TMP = 4