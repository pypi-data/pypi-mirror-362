"""Design pattern implementations for reuse across the jinnang package.

This module provides implementations of common design patterns such as Singleton,
Factory, and other structural patterns that can be reused throughout the application.
"""

import os
import logging
from typing import TypeVar, Type, Dict, Any, Optional, List, ClassVar

from jinnang.verbosity.verbosity import Verbosity

# Type variable for generic class methods
T = TypeVar('T')

class Singleton:
    """
    Base singleton class compatible with Python 3.8+.
    
    This class implements the Singleton pattern, ensuring only one instance 
    of a class exists and providing a standardized way to access it.
    
    Example:
        ```python
        class MyManager(Singleton):
            def __init__(self, config=None):
                if not hasattr(self, '_initialized'):
                    self.config = config or {}
                    self._initialized = True
                
        # Get the singleton instance
        manager = MyManager(config={'setting': 'value'})
        # Second call returns the same instance
        same_manager = MyManager.get_instance()
        assert manager is same_manager  # True
        ```
    """
    
    # Class variable to store singleton instances
    _instances: ClassVar[Dict[Type['Singleton'], 'Singleton']] = {}

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, *args: Any, **kwargs: Any):
        # This __init__ is to check for re-initialization with different params.
        if getattr(self, '_initialized_with_params', False):
            if args or kwargs:
                raise TypeError(
                    "Singleton already initialized with parameters. To prevent accidental reconfiguration, "
                    "re-initialization with new parameters is not allowed.\n"
                    "Example:\n"
                    "  s1 = MySingleton(value='foo')  # OK\n"
                    "  s2 = MySingleton(value='bar')  # Raises TypeError\n"
                    "Use MySingleton.get_instance() to retrieve the existing instance."
                )
            return

        # Mark as initialized with params if any are provided.
        if args or kwargs:
            self._initialized_with_params = True

    @classmethod
    def get_instance(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """Get the singleton instance. Parameters are not allowed.

        Raises:
            TypeError: If any arguments are passed.
        """
        if args or kwargs:
            raise TypeError(
                "get_instance() does not accept any arguments. Use the constructor for initial configuration.\n"
                "Example of incorrect usage:\n"
                "  s1 = MySingleton.get_instance(value='foo')  # Raises TypeError\n"
                "Correct usage:\n"
                "  s1 = MySingleton(value='foo')             # OK\n"
                "  s2 = MySingleton.get_instance()          # OK"
            )
        if cls not in cls._instances:
            return cls()
        return cls._instances[cls]
