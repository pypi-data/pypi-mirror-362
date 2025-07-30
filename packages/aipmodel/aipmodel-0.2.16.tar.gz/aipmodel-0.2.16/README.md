
# AIP Model SDK

This SDK provides a simple interface for registering, uploading, downloading, listing, and deleting machine learning models using ClearML and S3 (Ceph) as storage.

---

## Installation

Install from PyPI:

```bash
pip install aipmodel
```

---

## Authentication

You must provide your own **ClearML Access Key** and **Secret Key**, which you can obtain from:

[http://213.233.184.112:30080/](http://213.233.184.112:30080/) → Credentials section

---

## Example Usage

This example shows how to:

- Upload a local model
- Upload a Hugging Face model
- Upload a model from another S3
- Download a model
- List models
- Delete a model

```python
from aipmodel.model_registry import MLOpsManager

# STEP 1: Initialize with your ClearML credentials
manager = MLOpsManager(
    clearml_access_key="your-clearml-access-key",
    clearml_secret_key="your-clearml-secret-key"
)

# STEP 2: Upload local model
local_model_id = manager.add_model(
    source_type="local",
    source_path="path/to/your/local/model/folder",
    model_name="your_local_model"
)

# STEP 3: Upload HuggingFace model
hf_model_id = manager.add_model(
    source_type="hf",
    hf_source="facebook/wav2vec2-base-960h",  # Or any other public HF model
    model_name="your_hf_model"
)

# STEP 4: Upload model from your own S3 (e.g., AWS S3, MinIO, or Ceph)
s3_model_id = manager.add_model(
    source_type="s3",
    endpoint_url="http://your-s3-endpoint.com",
    access_key="your-s3-access-key",
    secret_key="your-s3-secret-key",
    bucket_name="your-s3-bucket",
    source_path="path/in/your/bucket/",
    model_name="your_s3_model"
)

# STEP 5: Download a model locally
manager.get_model(
    model_id=hf_model_id,  # or any valid model ID
    local_dest="./downloaded_model"
)

# STEP 6: List all models in your ClearML project
manager.list_models()

# STEP 7: Delete a model
manager.delete_model(model_id=local_model_id)
```

---

## Functions Overview

| Function            | Description                                         |
| ------------------- | --------------------------------------------------- |
| `add_model(...)`    | Uploads a model from local, HF or external S3       |
| `get_model(...)`    | Downloads a model from S3 to local path             |
| `list_models()`     | Lists all registered models in your ClearML project |
| `delete_model(...)` | Deletes a model from ClearML and S3                 |

---

## Notes

- Ceph credentials (`s3.cloud-ai.ir`, access key, secret key) are hardcoded and used for final storage.
- Your own external S3 bucket is supported only during upload (optional).
- No config file is needed. You must pass ClearML keys manually in code.

---

## Full Example

```python
from aipmodel.model_registry import MLOpsManager

# Initialize with your ClearML credentials
manager = MLOpsManager(
    clearml_access_key="YOUR_ACCESS_KEY",  # ← Replace with your actual access key
    clearml_secret_key="YOUR_SECRET_KEY"   # ← Replace with your actual secret key
)

# 1. Add local model
local_model_id = manager.add_model(
    source_type="local",
    source_path=r"/path/to/local/model",   # ← Replace with path to your model folder
    model_name="my_local_model"
)

# 2. Add model from HuggingFace
hf_model_id = manager.add_model(
    source_type="hf",
    hf_source="facebook/wav2vec2-base-960h",  # ← Replace if needed
    model_name="my_hf_model"
)

# 3. Add model from another S3 bucket
s3_model_id = manager.add_model(
    source_type="s3",
    endpoint_url="http://your-s3-endpoint.com",  # ← Replace with source S3
    access_key="YOUR_S3_ACCESS_KEY",             # ← Get from your S3 provider
    secret_key="YOUR_S3_SECRET_KEY",             # ← Get from your S3 provider
    bucket_name="your-source-bucket",            # ← Replace accordingly
    source_path="models/path/in/bucket/",        # ← Path inside source bucket
    model_name="my_s3_model"
)

# 4. Download a model by ID
manager.get_model(model_id=hf_model_id, local_dest="./downloads")

# 5. List all models
manager.list_models()

# 6. Delete a model
manager.delete_model(model_id=local_model_id)
```

---

## Admin Instructions: Auto-Publishing to PyPI

This SDK uses a GitHub Actions workflow (`.github/workflows/publish.yaml`) for automatic versioning and PyPI publishing.

### Trigger Conditions

- Must push to the `main` branch
- Must include `pipy commit -push` in the commit message
- Must have `PUBLISH_TO_PYPI=true` in GitHub project variables

### Commit Message Format

The following patterns control the version bump:

| Description Contains         | Resulting Bump           |
|-----------------------------|--------------------------|
| `pipy commit -push major`   | Increments **major**     |
| `pipy commit -push minor`   | Increments **minor**     |
| `pipy commit -push patch`   | Increments **patch**     |
| `pipy commit -push`         | Increments **patch** (default) |

### What Happens Automatically

- Version is read from PyPI
- New version is calculated using `bump_version.py`
- Version in `__init__.py` and `setup.py` is updated
- Changes are committed and pushed to `main`
- Package is built and published to PyPI via Twine

No manual work is needed from the admin.
