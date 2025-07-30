"""
Configuration module using Dynaconf for OC Image Segmentation.
"""

import os
from pathlib import Path
from typing import List, Optional, Union

from dynaconf import Dynaconf

# Global settings instance - will be initialized explicitly
_settings: Optional[Dynaconf] = None


def _get_default_settings_files() -> List[Union[str, Path]]:
    """Get default settings files list."""
    return [
        "settings.yaml",
        ".secrets.yaml",  # Optional secrets file
    ]


def _resolve_settings_files(
    settings_files: Optional[List[Union[str, Path]]] = None,
    root_path: Optional[Union[str, Path]] = None,
) -> List[Path]:
    """
    Resolve settings files with environment variables and root path.

    Args:
        settings_files: List of settings files. If None, uses environment or defaults
        root_path: Root path for relative files. If None, uses environment or current dir

    Returns:
        List of resolved Path objects
    """
    # Determine settings files
    if settings_files is None:
        custom_settings_files = os.environ.get("OC_SEGMENT_SETTINGS_FILES")
        if custom_settings_files:
            settings_files = [f.strip() for f in custom_settings_files.split(",")]
        else:
            settings_files = _get_default_settings_files()

    # Convert to Path objects
    settings_paths = [Path(f) for f in settings_files]

    # Determine root path
    if root_path is None:
        custom_root_path = os.environ.get("OC_SEGMENT_ROOT_PATH")
        if custom_root_path:
            root_path = Path(custom_root_path)
        else:
            # Default to project root (parent of this file's parent)
            root_path = Path(__file__).parent.parent
    else:
        root_path = Path(root_path)

    # Resolve relative paths against root_path
    resolved_paths = []
    for settings_path in settings_paths:
        if settings_path.is_absolute():
            resolved_paths.append(settings_path)
        else:
            resolved_paths.append(root_path / settings_path)

    return resolved_paths


def initialize_settings(
    settings_files: Optional[List[Union[str, Path]]] = None,
    root_path: Optional[Union[str, Path]] = None,
    environment: Optional[str] = None,
    force_reload: bool = False,
) -> Dynaconf:
    """
    Initialize the settings configuration explicitly.

    Args:
        settings_files: List of configuration files to load
        root_path: Root directory for relative paths
        environment: Environment to use (overrides OC_SEGMENT_ENV)
        force_reload: Force reinitialization even if already loaded

    Returns:
        Dynaconf settings instance

    Raises:
        FileNotFoundError: If required settings files don't exist
        ValueError: If configuration is invalid
    """
    global _settings

    if _settings is not None and not force_reload:
        return _settings

    # Resolve settings files
    resolved_files = _resolve_settings_files(settings_files, root_path)

    # Check if at least one primary settings file exists
    primary_files = [f for f in resolved_files if not f.name.startswith(".")]
    existing_primary = [f for f in primary_files if f.exists()]

    if not existing_primary:
        raise FileNotFoundError(
            f"No primary settings file found. Looked for: {primary_files}"
        )

    # Determine environment
    if environment is None:
        environment = os.environ.get("OC_SEGMENT_ENV", "default")

    # Initialize Dynaconf
    _settings = Dynaconf(
        # Configuration files to load
        settings_files=[str(f) for f in resolved_files],
        # Environment variables prefix
        envvar_prefix="OC_SEGMENT",
        # Enable environment switching
        environments=True,
        # Set environment
        env=environment,
        # Load environment from ENV variable
        env_switcher="OC_SEGMENT_ENV",
        # Enable .env file loading
        load_dotenv=True,
    )

    return _settings


def get_settings() -> Dynaconf:
    """
    Get the current settings instance.

    Returns:
        Dynaconf settings instance

    Raises:
        RuntimeError: If settings haven't been initialized
    """
    global _settings

    if _settings is None:
        # Auto-initialize with defaults for backward compatibility
        _settings = initialize_settings()

    return _settings


def reset_settings():
    """Reset settings to force reinitialization on next access."""
    global _settings
    _settings = None


def reset_settings_with_files(
    settings_files: Optional[List[Union[str, Path]]] = None,
    root_path: Optional[Union[str, Path]] = None,
    environment: Optional[str] = None,
) -> Dynaconf:
    """
    Reset and reinitialize settings with specific configuration files.

    This function is useful for dynamically switching between different
    configuration files (e.g., switching between trainId and categoryId modes).

    Args:
        settings_files: List of configuration files to load
        root_path: Root directory for relative paths
        environment: Environment to use (overrides OC_SEGMENT_ENV)

    Returns:
        Dynaconf settings instance

    Raises:
        FileNotFoundError: If required settings files don't exist
        ValueError: If configuration is invalid
    """
    # Reset current settings
    reset_settings()

    # Initialize with new files
    return initialize_settings(
        settings_files=settings_files,
        root_path=root_path,
        environment=environment,
        force_reload=True,
    )


class _SettingsProxy:
    """Proxy class for backward compatibility."""

    def __getattr__(self, name):
        return getattr(get_settings(), name)

    def __setattr__(self, name, value):
        setattr(get_settings(), name, value)

    def __bool__(self):
        return True


# Create a proxy instance for backward compatibility
settings = _SettingsProxy()


# Validation function
def validate_model_config(model_name: str) -> bool:
    """
    Validate if a model configuration exists and is valid.

    Args:
        model_name: Name of the model to validate

    Returns:
        bool: True if model config is valid
    """
    settings = get_settings()

    if model_name not in settings.models:
        return False

    model_config = settings.models[model_name]

    required_fields = [
        "input_size",
    ]

    return all(field in model_config for field in required_fields)


def get_model_config(model_name: str) -> dict:
    """
    Get configuration for a specific model.

    Args:
        model_name: Name of the model

    Returns:
        dict: Model configuration

    Raises:
        ValueError: If model configuration is invalid
    """
    if not validate_model_config(model_name):
        raise ValueError(f"Invalid or missing configuration for model: {model_name}")

    settings = get_settings()
    return settings.models[model_name].to_dict()


def get_supported_formats() -> list:
    """Get list of supported image formats."""
    settings = get_settings()
    return settings.image.supported_formats


def get_logging_config() -> dict:
    """Get logging configuration."""
    settings = get_settings()
    return {
        "level": settings.logging.level,
        "format": settings.logging.format,
    }


# Export settings for direct access
__all__ = [
    "initialize_settings",
    "get_settings",
    "reset_settings",
    "reset_settings_with_files",
    "validate_model_config",
    "get_model_config",
    "get_supported_formats",
    "get_logging_config",
]
