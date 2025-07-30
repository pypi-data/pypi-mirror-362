"""
Hex Address System

A reversible system for converting GPS coordinates to memorable syllable-based
addresses using Uber's H3 spatial indexing system.

Features:
- Sub-meter precision (~0.5m) using H3 Level 15
- Memorable syllable addresses (e.g., "dinenunukiwufeme")
- Perfect reversible mapping for all real coordinates
- Multiple language-specific configurations
- Address validation (some combinations don't exist, like street addresses)
- International pronunciation optimization

Example:
    >>> from hex_address import H3SyllableSystem, is_valid_address
    >>>
    >>> # Initialize system (uses ascii-dnqqwn by default)
    >>> system = H3SyllableSystem()
    >>>
    >>> # Convert coordinate to syllable address
    >>> address = system.coordinate_to_address(48.8566, 2.3522)
    >>> print(address)  # 8-syllable address
    >>>
    >>> # Convert back to coordinates
    >>> lat, lon = system.address_to_coordinate(address)
    >>> print(f"{lat:.6f}, {lon:.6f}")  # 48.856602, 2.352198
    >>>
    >>> # Validate addresses (some combinations don't exist)
    >>> is_valid = system.is_valid_address(address)
    >>> print(is_valid)  # True
"""

from .config_loader import (
    SyllableConfig,
    get_all_configs,
    get_config,
    list_configs,
)
from .h3_syllable_system import (
    AddressAnalysis,
    ConversionError,
    GeographicBounds,
    H3SyllableError,
    H3SyllableSystem,
    PartialLocationEstimate,
    PhoneticAlternative,
    PhoneticChange,
    SystemInfo,
    analyze_address,
    coordinate_to_address,
    estimate_location_from_partial,
    get_config_info,
    is_valid_address,
    list_available_configs,
    address_to_coordinate,
)
from .utilities import (
    calculate_distance,
    find_nearby_addresses,
    get_address_bounds,
    cluster_addresses,
    haversine_distance,
)

__version__ = "1.3.1"
__author__ = "Álvaro Silva"
__license__ = "MIT"
__description__ = "Convert GPS coordinates to memorable hex addresses"

# Public API
__all__ = [
    # Main classes
    "H3SyllableSystem",
    "SyllableConfig",
    "SystemInfo",
    "GeographicBounds",
    "PartialLocationEstimate",
    # Address analysis classes
    "AddressAnalysis",
    "PhoneticAlternative",
    "PhoneticChange",
    # Exceptions
    "H3SyllableError",
    "ConversionError",
    # Convenience functions
    "coordinate_to_address",
    "address_to_coordinate",
    "is_valid_address",
    "estimate_location_from_partial",
    "analyze_address",
    # Configuration functions
    "get_config",
    "get_all_configs",
    "list_configs",
    "list_available_configs",
    "get_config_info",
    # Utility functions
    "calculate_distance",
    "find_nearby_addresses",
    "get_address_bounds",
    "cluster_addresses",
    "haversine_distance",
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
    "__description__",
]
