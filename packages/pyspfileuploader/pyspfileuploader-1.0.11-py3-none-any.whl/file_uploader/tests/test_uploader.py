import os
import pytest
from pathlib import Path
import zipfile
from io import BytesIO
from file_uploader.src.file_upload import (
    LocalStorageHandler,
    S3StorageHandler,
    ADLSStorageHandler,
    BlobStorageHandler,
    StorageError
)

# Test data
TEST_CONTENT = b"test content"
TEST_TEXT_CONTENT = "test content"
ZIP_FILES = {
    "test1.txt": b"test content 1",
    "test2.txt": b"test content 2",
    "subfolder/test3.txt": b"test content 3"
}

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def local_handler(temp_dir):
    """Create a LocalStorageHandler instance."""
    return LocalStorageHandler(base_path=temp_dir, folder_path="test_folder")

@pytest.fixture
def test_zip_file():
    """Create a test zip file in memory."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, content in ZIP_FILES.items():
            zip_file.writestr(file_name, content)
    return zip_buffer.getvalue()

class TestLocalStorageHandler:
    """Test LocalStorageHandler functionality."""

    def test_save_single_file(self, local_handler):
        """Test saving a single file."""
        result = local_handler.upload_files("test.txt", TEST_CONTENT)
        assert result == ["test.txt"]
        
        # Verify file exists and content is correct
        file_path = local_handler.file_path / "upload" / "test_folder" / "test.txt"
        assert file_path.exists()
        assert file_path.read_bytes() == TEST_CONTENT

    def test_save_zip_file(self, local_handler, test_zip_file):
        """Test saving a zip file."""
        result = local_handler.upload_files("test.zip", test_zip_file)
        
        # Verify all files were extracted and saved
        expected_files = [name for name in ZIP_FILES.keys() if not '/' in name]
        assert sorted(result) == sorted(expected_files)
        
        # Verify content of extracted files
        for file_name in expected_files:
            file_path = local_handler.file_path / "upload" / "test_folder" / file_name
            assert file_path.exists()
            assert file_path.read_bytes() == ZIP_FILES[file_name]

    def test_file_size_limit(self, local_handler):
        """Test file size limit validation."""
        large_content = b"x" * (101 * 1024 * 1024)  # 101MB
        with pytest.raises(StorageError, match="exceeds maximum allowed size"):
            local_handler.upload_files("large.txt", large_content)

    def test_invalid_zip_file(self, local_handler):
        """Test handling of invalid zip files."""
        invalid_zip = b"not a zip file"
        with pytest.raises(StorageError, match="Invalid or corrupted zip file"):
            local_handler.upload_files("invalid.zip", invalid_zip)

    def test_read_files(self, local_handler):
        """Test reading files with specific extensions."""
        # Setup test files
        local_handler.upload_files("test1.txt", b"content1")
        local_handler.upload_files("test2.csv", b"content2")
        local_handler.upload_files("test3.txt", b"content3")
        
        # Test reading .txt files
        result = local_handler.read_files(
            local_handler.file_path / "upload" / "test_folder",
            extensions=[".txt"]
        )
        assert len(result) == 2
        assert "test1.txt" in result
        assert "test3.txt" in result
        assert result["test1.txt"] == "content1"

    def test_file_extension_validation(self, local_handler):
        """Test file extension validation."""
        with pytest.raises(StorageError, match="File extension.*not allowed"):
            local_handler.upload_files(
                "test.exe",
                TEST_CONTENT,
                allowed_extensions=['.txt', '.csv']
            )

# Mock classes for testing cloud storage handlers
class MockS3Client:
    def put_object(self, *args, **kwargs):
        pass

class MockBlobClient:
    def upload_blob(self, *args, **kwargs):
        pass

class TestCloudStorageHandlers:
    """Test cloud storage handlers with mocks."""
    
    @pytest.fixture
    def s3_handler(self, monkeypatch):
        """Create a mocked S3StorageHandler."""
        def mock_boto3_client(*args, **kwargs):
            return MockS3Client()
        monkeypatch.setattr("boto3.client", mock_boto3_client)
        return S3StorageHandler(
            "test-bucket",
            "test-key",
            "test-secret",
            "us-east-1",
            "test_folder"
        )

    @pytest.fixture
    def blob_handler(self, monkeypatch):
        """Create a mocked BlobStorageHandler."""
        def mock_blob_service(*args, **kwargs):
            return MockBlobClient()
        monkeypatch.setattr(
            "azure.storage.blob.BlobServiceClient.from_connection_string",
            mock_blob_service
        )
        return BlobStorageHandler(
            "connection-string",
            "container-name",
            "test_folder"
        )

    def test_s3_upload(self, s3_handler):
        """Test S3 upload functionality."""
        result = s3_handler.upload_files("test.txt", TEST_CONTENT)
        assert result == ["test.txt"]

    def test_blob_upload(self, blob_handler):
        """Test Blob storage upload functionality."""
        result = blob_handler.upload_files("test.txt", TEST_CONTENT)
        assert result == ["test.txt"]
