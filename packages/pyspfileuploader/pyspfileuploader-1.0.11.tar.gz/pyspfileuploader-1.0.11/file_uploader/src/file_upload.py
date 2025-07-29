import zipfile
import boto3
from abc import ABC, abstractmethod
from pathlib import Path
from io import BytesIO
from typing import Dict, List, Union
from azure.core.exceptions import ResourceExistsError
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.blob import BlobServiceClient
from file_uploader.exceptions import StorageError

class FileStorageHandler(ABC):
    """File storage handler as an abstract implementation."""
    def __init__(self):
        """Initialize the handler."""
        self.extracted_files = []
        
    def validate_file_size(self, content: bytes, max_size_mb: int = 100) -> None:
        """Validate file size is within limits."""
        size_mb = len(content) / (1024 * 1024)  # Convert to MB
        if size_mb > max_size_mb:
            raise StorageError(f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)")

    @abstractmethod
    def save_files(self, file_name: str, content: bytes, is_source_upload: bool = True) -> List[str]:
        """Save files to storage."""
        pass

    @abstractmethod
    def read_files(self, file_path: Union[Path, str], extensions: List[str]) -> Dict[str, str]:
        """Read files from storage."""
        pass

    def _extract_and_save_zip_file(self, zip_content: bytes, is_source_upload: bool) -> List[str]:
        """Extract files from a zip archive and save individually."""
        try:
            # First validate the zip file size
            self.validate_file_size(zip_content)
            
            with zipfile.ZipFile(BytesIO(zip_content)) as zip_archive:
                # Validate zip file integrity
                if zip_archive.testzip() is not None:
                    raise StorageError("Zip file is corrupted")
                
                # Calculate total uncompressed size
                total_size = sum(info.file_size for info in zip_archive.filelist)
                if total_size > 200 * 1024 * 1024:  # 200MB limit for extracted files
                    raise StorageError("Total uncompressed size exceeds 200MB limit")
                
                extracted_files = []
                for member in zip_archive.infolist():
                    if member.is_dir():
                        continue
                        
                    # Skip hidden files and potentially dangerous files
                    filename = Path(member.filename).name
                    if filename.startswith('.') or filename.startswith('__'):
                        continue
                        
                    # Read and validate individual file
                    extracted_data = zip_archive.read(member.filename)
                    self.validate_file_size(extracted_data)
                    
                    # Save the file and track it
                    self.save_files(filename, extracted_data, is_source_upload)
                    extracted_files.append(filename)

                return extracted_files
            
        except zipfile.BadZipFile as e:
            raise StorageError(f"Invalid or corrupted zip file: {str(e)}")
        except Exception as e:
            raise StorageError(f"Error processing zip file: {str(e)}")

    def upload_files(self, file_name: str, content: bytes, 
                    is_source_upload: bool = True, 
                    allowed_extensions: List[str] = None) -> List[str]:
        """Upload files to the storage handler."""
        try:
            # Validate file extension if restrictions are provided
            if allowed_extensions:
                ext = Path(file_name).suffix.lower()
                if ext not in allowed_extensions:
                    raise StorageError(
                        f"File extension '{ext}' not allowed. "
                        f"Allowed extensions: {', '.join(allowed_extensions)}"
                    )
            
            # Validate individual file size for non-zip files
            if not file_name.endswith('.zip'):
                self.validate_file_size(content)

            # Process based on file type
            if file_name.endswith('.zip'):
                return self._extract_and_save_zip_file(content, is_source_upload)
            else:
                result = self.save_files(file_name, content, is_source_upload)
                return result if isinstance(result, list) else [result]
                
        except StorageError:
            raise  # Re-raise StorageError as is
        except Exception as e:
            raise StorageError(f"Error uploading file(s): {str(e)}")
        

class LocalStorageHandler(FileStorageHandler):
    """Real world implementation of local storage handler."""
    def __init__(self, base_path: Path, folder_path: str = ""):
        """Initializing."""
        self.file_path = base_path
        self.folder_path = folder_path
        self.file_path.mkdir(parents=True, exist_ok=True)

    def save_files(self, file_name: str, content: bytes, is_source_upload: bool = True):
        """Save files to local storage."""
        try:
            if is_source_upload:
                # upload/job_id/created_date/file1.txt
                upload_path = self.file_path.joinpath("upload", self.folder_path, file_name)
            else:
                # converted/job_id/created_date/file1.txt for converted files
                upload_path = self.file_path.joinpath("converted", self.folder_path, file_name)
            upload_path.parent.mkdir(parents=True, exist_ok=True)
            if not is_source_upload:
                if not isinstance(content, str):
                    raise ValueError("Content must be a string for local storage.")
                with open(upload_path, 'w', encoding="utf-8") as f:
                    f.write(content)
            else:
                with open(upload_path, 'wb') as f:
                    f.write(content)
            
            return [file_name]
        except Exception as e:
            raise StorageError(f"An error occurred:::{str(e)}")

    def read_files(self, file_path: Path, extensions: List[str]) -> Dict[str, str]:
        """Read files from local storage."""
        try:
            all_files = {}
            for extension in extensions:
                for file in file_path.rglob(f"*{extension}"):
                    try:
                        all_files[file.name] = file.read_text(encoding='utf-8')
                    except UnicodeDecodeError:
                        all_files[file.name] = file.read_text(encoding='utf-8', errors='ignore')
            
            return all_files
        except Exception as e:
            raise StorageError(f"An error occurred:::{str(e)}")


class S3StorageHandler(FileStorageHandler):
    """Real world implementation of s3 storage handler."""
    def __init__(self, aws_bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, folder_path: str):
        """Initializing."""
        self.bucket = aws_bucket_name
        self.folder_path = folder_path
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def save_files(self, file_name: str, content: bytes, is_source_upload: bool=True):
        """Save files to s3 bucket."""
        try:
            upload_path = f"upload/{self.folder_path}/{file_name}" if is_source_upload else f"converted/{self.folder_path}/{file_name}"
            self.s3.put_object(Bucket=self.bucket, Key=upload_path, Body=content)

            return [file_name]
        except Exception as e:
            raise StorageError(f"An error occurred:::{str(e)}")

    def read_files(self, file_path: str, extensions: List[str]) -> Dict[str, str]:
        """Read files from s3 bucket."""
        try:
            all_files = {}
            read_file_path = f"data/upload/{file_path}"
            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket, Prefix=read_file_path)
            for page in pages:
                for obj in page.get('Contents', []):
                    key = obj['Key']
                    if any(key.endswith(extension) for extension in extensions):
                        content = self.s3.get_object(Bucket=self.bucket, Key=key)['Body'].read()
                        try:
                            all_files[Path(key).name] = content.decode('utf-8')
                        except UnicodeDecodeError:
                            all_files[Path(key).name] = content.decode('utf-8', errors='ignore')

            return all_files
        except Exception as e:
            raise StorageError(f"An error occurred:::{str(e)}")


class ADLSStorageHandler(FileStorageHandler):
    """Real world implementation of adls storage handler."""
    def __init__(self, adls_account_name: str, adls_file_system_name: str, adls_credential: str, folder_path: str ):
        """Initializing."""
        self.folder_path = folder_path
        self.service = DataLakeServiceClient(
            account_url=f"https://{adls_account_name}.dfs.core.windows.net",
            credential=adls_credential,
        )
        self.file_system_client = self.service.get_file_system_client(adls_file_system_name)

    def save_files(self, file_name: str, content: bytes, is_source_upload: bool = True):
        """Save files to adls.""" 
        try:
            upload_path = f"upload/{self.folder_path}/{file_name}" if is_source_upload else f"converted/{self.folder_path}/{file_name}"
            file_client = self.file_system_client.get_file_client(upload_path)
            file_client.upload_data(content, overwrite=True)

            return [file_name]
        except Exception as e:
            raise StorageError(f"Failed to save files: {str(e)}")

    def read_files(self, file_path: str, extensions: List[str]) -> Dict[str, str]:
        """Read files from ADLS."""
        try:
            all_files = {}
            read_file_path = f"data/upload/{file_path}"
            paths = self.file_system_client.get_paths(path=read_file_path, recursive=True)
            for path in paths:
                if not path.is_directory and any(path.name.endswith(ext) for ext in extensions):
                    file_client = self.file_system_client.get_file_client(path.name)
                    content = file_client.download_file().readall()
                    try:
                        all_files[Path(path.name).name] = content.decode('utf-8')
                    except UnicodeDecodeError:
                        all_files[Path(path.name).name] = content.decode('utf-8', errors='ignore')

            return all_files 
        except Exception as e:
            raise StorageError(f"Failed to read files: {str(e)}")



class BlobStorageHandler(FileStorageHandler):
    """Real world implementation of blob storage handler."""
    def __init__(self, blob_connection_string: str, blob_container_name: str, folder_path: str):
        """Initializing."""
        self.folder_path = folder_path
        self.blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        self.container_client = self.blob_service_client.get_container_client(blob_container_name)
        try:
            self.container_client.create_container()
        except ResourceExistsError:
            pass

    def save_files(self, file_name: str, content: bytes, is_source_upload: bool = True):
        """Save files to blob storage."""
        try:
            upload_path = f"upload/{self.folder_path}/{file_name}" if is_source_upload else f"converted/{self.folder_path}/{file_name}"
            blob_client = self.container_client.get_blob_client(upload_path)
            blob_client.upload_blob(content, overwrite=True)

            return [file_name]
        except Exception as e:
            raise StorageError(f"Failed to save files: {str(e)}")

    def read_files(self, file_path: str, extensions: List[str]) -> Dict[str, str]:
        """Read files from blob storage."""
        try:
            all_files = {}
            read_file_path = f"data/upload/{file_path}"
            blobs = self.container_client.list_blobs(name_starts_with=read_file_path)
            for blob in blobs:
                if any(blob.name.endswith(ext) for ext in extensions):
                    blob_client = self.container_client.get_blob_client(blob.name)
                    content = blob_client.download_blob().readall()
                    try:
                        all_files[Path(blob.name).name] = content.decode('utf-8')
                    except UnicodeDecodeError:
                        all_files[Path(blob.name).name] = content.decode('utf-8', errors='ignore')
            
            return all_files
        except Exception as e:
            raise StorageError(f"Failed to read files: {str(e)}")