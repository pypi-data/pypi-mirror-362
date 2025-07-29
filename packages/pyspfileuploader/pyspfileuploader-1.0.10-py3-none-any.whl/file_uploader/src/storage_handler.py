from datetime import datetime
from file_uploader.constants import BASE_PATH
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict
from file_uploader.src.file_upload import (
    LocalStorageHandler,
    S3StorageHandler,
    ADLSStorageHandler,
    BlobStorageHandler,
)

load_dotenv()

def build_folder_path(**kwargs: Dict) -> str:
    """Build the folder path for file storage.
    
    The structure will be:
    job_id/created_date
    
    Example:
    20250713143022_a1b2c/13-07-2025
    """
    job_id = kwargs['job_id']  # This should always be provided
    created_date = kwargs.get('created_date', datetime.now().strftime("%d-%m-%Y"))
    return f"{job_id}/{created_date}"


def get_storage_handler(config_dict: Dict, **kwargs: Dict):
    """Get storage handler basis on the storage type."""
    job_id = kwargs["job_id"]  # This will be set by __main__.py
    created_date = kwargs.get("created_date", datetime.now().strftime("%d-%m-%Y"))
    storage_type = kwargs.get("storage_type", "local")
    folder_path = build_folder_path(
        job_id=job_id,
        created_date=created_date,
    )
        
    if storage_type == "adls":
        print(f"//Using {storage_type} for file upload.")
        return ADLSStorageHandler(
            folder_path=folder_path,
            adls_account_name=config_dict.get("ADLS_ACCOUNT_NAME"),
            adls_file_system_name=config_dict.get("ADLS_FILE_SYSTEM_NAME"),
            adls_credential=config_dict.get("ADLS_CREDENTIAL"),
        )
    elif storage_type == "local":
        print(f"//Using {storage_type} for file upload.")
        return LocalStorageHandler(
            base_path=Path(BASE_PATH),
            folder_path=folder_path,
        )
    elif storage_type == "s3":
        print(f"//Using {storage_type} for file upload.")
        return S3StorageHandler(
            folder_path=folder_path,
            aws_bucket_name=config_dict.get("AWS_BUCKET_NAME"),
            aws_access_key_id=config_dict.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config_dict.get("AWS_SECRET_ACCESS_KEY"),
            region_name=config_dict.get("REGION_NAME", "us-east-1"),
        )
    
    elif storage_type == "blob":
        print(f"//Using {storage_type} for file upload.")
        return BlobStorageHandler(
            folder_path=folder_path,
            blob_connection_string=config_dict.get("BLOB_CONNECTION_STRING"),
            blob_container_name=config_dict.get("BLOB_CONTAINER_NAME"),
        )
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")