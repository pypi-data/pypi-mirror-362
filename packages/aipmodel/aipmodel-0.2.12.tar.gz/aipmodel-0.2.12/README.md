# AIPModel SDK

AIPModel is a Python SDK for managing machine learning model storage, versioning, and registration. It allows users to upload/download models from local, Hugging Face, or S3 sources and registers them in ClearML.

---

## Installation

Install from PyPI:

```bash
pip install aipmodel
```

---

## ClearML Credentials

To use this SDK, you must have valid ClearML credentials.

1. Visit: [http://213.233.184.112:30080](http://213.233.184.112:30080)
2. Go to the **Credentials** section
3. Copy your `access_key` and `secret_key`

You will need to provide these in your code (no config file is required).

---

## Usage

### Import

```python
from aipmodel.model_registry import MLOpsManager
```

### Initialization

```python
manager = MLOpsManager(
    clearml_access_key="YOUR_ACCESS_KEY",
    clearml_secret_key="YOUR_SECRET_KEY"
)
```

Replace `"YOUR_ACCESS_KEY"` and `"YOUR_SECRET_KEY"` with your own values.

---

## Features

### 1. Add Model

#### a) From Local Directory

```python
local_model_id = manager.add_model(
    source_type="local",
    source_path=r"/path/to/your/model",
    model_name="local_model"
)
```

#### b) From HuggingFace

```python
hf_model_id = manager.add_model(
    source_type="hf",
    hf_source="facebook/wav2vec2-base-960h",
    model_name="hf_model"
)
```

#### c) From Another S3 Bucket

```python
s3_model_id = manager.add_model(
    source_type="s3",
    endpoint_url="http://your-s3-endpoint.com",
    access_key="your-access-key",   # Get from your provider
    secret_key="your-secret-key",   # Get from your provider
    bucket_name="your-bucket-name",
    source_path="models/path/in/bucket/",
    model_name="s3_model"
)
```

---

### 2. Get/Download Model

```python
manager.get_model(model_id=hf_model_id, local_dest="./downloads")
```

Downloads the model files into `./downloads` directory.

---

### 3. List Models

```python
manager.list_models()
```

Prints all models registered under the project associated with your user.

---

### 4. Delete Model

```python
manager.delete_model(model_id=local_model_id)
```

Deletes model from ClearML and the underlying S3 storage.

---

## Development and Publishing (for Admins)

### Update Version

Update version inside `__init__.py`:

```python
__version__ = "0.2.12"  # ← Update this
```

### Build and Publish

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

Make sure to have `.pypirc` configured or use `--username`/`--password` with `twine`.

---

## Notes

- Ceph S3 credentials and endpoint are hardcoded for internal use.
- ClearML credentials **must** be provided by user at runtime.
- User-specific ClearML projects will be auto-created with prefix `project_{username}`.
