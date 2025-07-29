from .test import create_model, download_model, get_model, list_models
from .model_registry import (
    upload_file, download_file, delete_folder, upload, download, 
    check_auth, check_connection, check_if_exists, check_clearml_auth, 
    check_clearml_service, check_internet, ensure_bucket_exists, 
    is_folder, delete_model, get_all, get_by_id, update, create, add_model, 
    list_models as list_models_internal, get_model as get_model_internal, _post
)
from .update_checker import check_latest_version

check_latest_version("aipmodel")

__all__ = [
    "_post",
    "add_model",
    "check_auth",
    "check_clearml_auth",
    "check_clearml_service",
    "check_connection",
    "check_if_exists",
    "check_internet",
    "create",
    "create_model",
    "delete",
    "delete_folder",
    "delete_model",
    "download",
    "download_file",
    "download_folder",
    "download_model",
    "ensure_bucket_exists",
    "get_all",
    "get_by_id",
    "get_model",
    "is_folder",
    "list_models",
    "update",
    "upload",
    "upload_file",
]

__version__ = "0.2.12"
__description__ = "SDK for model registration, versioning, and storage"
