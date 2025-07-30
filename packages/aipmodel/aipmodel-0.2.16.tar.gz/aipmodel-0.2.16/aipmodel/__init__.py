from .test import create_model, download_model, get_model, list_models
from .model_registry import MLOpsManager
from .update_checker import check_latest_version

check_latest_version("aipmodel")

__all__ = [
    "create_model",
    "download_model",
    "get_model",
    "list_models",
    "MLOpsManager"
]

__version__ = "0.2.16"
__description__ = "SDK for model registration, versioning, and storage"
