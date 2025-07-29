import pytest
from datetime import datetime
from pathlib import Path
from file_uploader.metadata.db_interface import DbUtils
from file_uploader.exceptions import DatabaseError

@pytest.fixture
def db_utils(tmp_path):
    """Create a DbUtils instance with a temporary database."""
    # Override the database path for testing
    db = DbUtils()
    db.db_path = tmp_path / "test.db"
    db._initialize_db()
    return db

class TestDbUtils:
    """Test database utility functions."""

    def test_create_job(self, db_utils):
        """Test creating a new job."""
        job_id = "test-job-1"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test1.txt", "test2.txt"]
        
        # Create job
        result = db_utils.create_job(job_id, created_date, files)
        assert result == job_id
        
        # Verify job was created
        jobs = db_utils.fetch_job(job_id)
        assert len(jobs) == 2  # Two files
        assert all(job["JOB_ID"] == job_id for job in jobs)
        assert all(job["STATUS"] == "STARTED" for job in jobs)

    def test_update_job(self, db_utils):
        """Test updating job status."""
        # Create a job first
        job_id = "test-job-2"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test.txt"]
        db_utils.create_job(job_id, created_date, files)
        
        # Update job
        db_utils.update_job(job_id, "COMPLETED")
        
        # Verify update
        jobs = db_utils.fetch_job(job_id)
        assert len(jobs) == 1
        assert jobs[0]["STATUS"] == "COMPLETED"
        assert jobs[0]["END_TIME"] is not None
        assert jobs[0]["PROCESSING_TIME"] is not None

    def test_update_job_with_error(self, db_utils):
        """Test updating job with error information."""
        # Create a job first
        job_id = "test-job-3"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test.txt"]
        db_utils.create_job(job_id, created_date, files)
        
        # Update job with error
        error_code = "ERR001"
        error_desc = "Test error occurred"
        db_utils.update_job(job_id, "ERROR", error_code, error_desc)
        
        # Verify error information
        jobs = db_utils.fetch_job(job_id)
        assert len(jobs) == 1
        assert jobs[0]["STATUS"] == "ERROR"
        assert jobs[0]["ERROR_CODE"] == error_code
        assert jobs[0]["ERROR_DESC"] == error_desc

    def test_log_error(self, db_utils):
        """Test error logging."""
        job_id = "test-job-4"
        error_details = {
            "module_name": "test_module",
            "script_name": "test_script.py",
            "line_no": 42,
            "error_desc": "Test error",
            "error_stack_trace": "Test stack trace"
        }
        
        # Log error
        db_utils.log_error(
            job_id=job_id,
            module_name=error_details["module_name"],
            script_name=error_details["script_name"],
            line_no=error_details["line_no"],
            error_desc=error_details["error_desc"],
            error_stack_trace=error_details["error_stack_trace"]
        )
        
        # Verify error log
        logs = db_utils.fetch_error_logs(job_id)
        assert len(logs) == 1
        log = logs[0]
        assert log["JOB_ID"] == job_id
        assert log["MODULE_NAME"] == error_details["module_name"]
        assert log["LINE_NO"] == error_details["line_no"]
        assert log["ERROR_DESC"] == error_details["error_desc"]

    def test_invalid_job_update(self, db_utils):
        """Test updating non-existent job."""
        with pytest.raises(DatabaseError, match="Database error while updating job"):
            db_utils.update_job("non-existent-job", "COMPLETED")
