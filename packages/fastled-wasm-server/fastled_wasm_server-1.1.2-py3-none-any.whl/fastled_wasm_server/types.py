from dataclasses import dataclass
from enum import Enum


@dataclass
class CompilerStats:
    compile_count: int = 0
    compile_failures: int = 0
    compile_successes: int = 0


class BuildMode(Enum):
    """Build mode enum that handles both uppercase and lowercase values for API compatibility."""

    DEBUG = "debug"
    QUICK = "quick"
    RELEASE = "release"

    @classmethod
    def from_string(cls, mode_str: str) -> "BuildMode":
        """Convert string to BuildMode enum, handling both uppercase and lowercase."""
        try:
            # Try to match by value first (case-insensitive)
            mode_str_lower = mode_str.lower()
            for build_mode in cls:
                if build_mode.value == mode_str_lower:
                    return build_mode
            # If no value match, try by name (case-insensitive)
            return cls[mode_str.upper()]
        except (KeyError, AttributeError):
            valid_modes = [bm.value for bm in cls]
            raise ValueError(f"Build mode must be one of {valid_modes}, got {mode_str}")
