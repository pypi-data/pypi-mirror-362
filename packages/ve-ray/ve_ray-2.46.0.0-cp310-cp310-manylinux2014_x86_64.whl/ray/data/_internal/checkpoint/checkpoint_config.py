from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# --- Configuration Classes ---
class CheckpointStorageConfig:
    """Parsed configuration for a specific checkpoint storage backend."""
    def __init__(self, storage_config: Dict[str, Any]):
        self.remote_args: Dict[str, Any] = storage_config.get("remote_args", {})
        self.type: str = storage_config.get("type", "fs")
        self.check_ready_timeout: float = storage_config.get(
            "check_ready_timeout", 500)
        if self.type != "fs":
            raise ValueError("Checkpoint storage type must be 'fs'.")
        options_key = f"{self.type}_options"
        if not storage_config.get(options_key):
            raise ValueError(f"{self.type} checkpoint storage requires '{options_key}' options.")
        # fs specific parsed options
        self.options = storage_config.get(options_key, {})
        self.path = self.options.get("path", None)
        if self.path is None:
            raise ValueError(
                f"{self.type} checkpoint storage requires 'path' option.")

class CheckpointConfig:
    """
    The main checkpoint configuration class.

    This class is responsible for parsing and validating the checkpoint configuration
    from the DataContext. It ensures that the configuration is in the correct format
    and contains all the necessary information for checkpoint.

    Attributes:
        enabled (bool): Whether checkpoint is enabled.
        key_columns (Optional[List[str]]): The list of key columns for checkpoint.
        num_buckets (int): The number of buckets for checkpoint.
    """
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        if config_dict is None:
            config_dict = {}

        self.enabled: bool = config_dict.get("enabled", False)
        self.key_columns: Optional[List[str]] = None
        self.num_buckets: int = 1
        self.storage_config: Optional[CheckpointStorageConfig] = None

        if self.enabled:
            key_columns = config_dict.get("key_columns", None)
            if isinstance(key_columns, str):
                key_columns = [key_columns]
            if key_columns is None or len(key_columns) != 1:
                raise ValueError(
                    "Checkpoint 'key_columns' must include one column when enabled."
                )
            self.key_columns = key_columns
            self.num_buckets: int = config_dict.get("num_buckets", 1)
            if self.num_buckets <= 0:
                raise ValueError("Checkpoint 'num_buckets' must be greater than 0.")

            storage_settings = config_dict.get("storage")
            if not isinstance(storage_settings, dict):
                # If enabled, storage config is expected to be a dict.
                # If not a dict (e.g. None or wrong type), default to a disabled-like state
                # or raise error. For now, let's assume it implies issues,
                # so CheckpointStorageConfig might raise error if critical parts are missing.
                logger.warning(
                    "Checkpoint is enabled but 'storage' config is missing or not a dictionary. "
                    "Defaults will be attempted."
                )
                storage_settings = {}

            self.storage_config = CheckpointStorageConfig(storage_settings)

    @property
    def is_enabled(self) -> bool:
        return self.enabled

