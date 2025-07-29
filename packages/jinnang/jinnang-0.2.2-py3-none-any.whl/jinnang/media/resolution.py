"""Module for handling video resolution presets."""

from enum import Enum, unique
from functools import total_ordering

@unique
@total_ordering
class ResolutionPreset(Enum):
    """Standard video resolution presets with exact dimensions.
    
    This enumeration defines common video resolution presets with their exact
    width and height dimensions in pixels. It supports comparison operations
    to determine relative sizes between resolutions.
    
    Each preset is represented as a tuple of (width, height) in pixels.
    The ORIGINAL preset is a special case that represents the native resolution
    of the source material (represented as None, None).
    
    Example:
        ```python
        # Compare resolutions
        if ResolutionPreset.RES_720P > ResolutionPreset.RES_480P:
            print("720p is higher resolution than 480p")
            
        # Get dimensions
        width, height = ResolutionPreset.RES_1080P.value
        ```
    """
    ORIGINAL = (None, None)

    RES_4K = (3840, 2160)
    RES_2K = (2560, 1440)
    RES_1080P = (1920, 1080)
    RES_720P = (1280, 720)
    RES_540P = (960, 540)
    RES_480P = (854, 480)
    RES_360P = (640, 360)
    RES_240P = (426, 240)

    RES_144P = (256, 144)       # Common low-quality streaming
    RES_120P = (160, 120)       # Old webcam/QQVGA standard
    RES_96P = (128, 96)         # Very low-res, sometimes for thumbnails
    RES_80P = (160, 80)         # Ultra-low bandwidth (e.g., IoT devices)
    RES_64P = (64, 64)          # Tiny (e.g., placeholder icons)
    RES_48P = (48, 48)          # Extremely small (practically unusable for video)
    RES_32P = (32, 32)          # Thumbnail/legacy icon size
    RES_16P = (16, 16)          # Smallest usable (favicon-sized)
    
    
    @classmethod
    def from_string(cls, value: str) -> 'Resolution':
        """Initialize from shorthand notation like '1080p' or '4k'"""
        value = value.upper().strip()
        
        # Handle "P" notation (720P, 1080P)
        if value.endswith('P'):
            height = int(value[:-1])
            return cls(f"RES_{height}P")
        
        # Handle "K" notation (2K, 4K)
        if value.endswith('K'):
            return cls(f"RES_{value}")
        
        # Handle raw numbers (16, 32)
        if value.isdigit():
            return cls(f"RES_{value}")
        
        raise ValueError(f"Unknown resolution format: {value}")

    @property
    def width(self) -> int:
        return self.value[0]
    
    @property
    def height(self) -> int:
        return self.value[1]
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.width}x{self.height})"

    def __eq__(self, other):
        if not isinstance(other, ResolutionPreset):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, ResolutionPreset):
            return NotImplemented
        if self.value == (None, None):
            return False  # ORIGINAL is always largest
        if other.value == (None, None):
            return True  # Any other resolution is less than ORIGINAL

        # Compare based on total pixel count (width * height)
        self_pixels = self.value[0] * self.value[1]
        other_pixels = other.value[0] * other.value[1]
        return self_pixels < other_pixels