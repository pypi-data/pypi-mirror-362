import pytest
from datetime import datetime
from file_uploader.jobs.db_manager import JobManager
from file_uploader.exceptions import DatabaseError

class TestJobManager:
    """Test job management functionality."""

    def test_create_job(self):
        """Test job creation."""
        job_id = "test-job-1"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test1.txt", "test2.txt"]
        
        result = JobManager.create_job(job_id, created_date, files)
        assert result == job_id

    def test_update_job(self):
        """Test job status update."""
        # First create a job
        job_id = "test-job-2"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test.txt"]
        JobManager.create_job(job_id, created_date, files)
        
        # Update the job
        JobManager.update_job(job_id, "COMPLETED")
        
        # Verify update
        jobs = JobManager.fetch_job(job_id)
        assert len(jobs) == 1
        assert jobs[0]["STATUS"] == "COMPLETED"

    def test_update_job_with_error(self):
        """Test job update with error information."""
        # First create a job
        job_id = "test-job-3"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test.txt"]
        JobManager.create_job(job_id, created_date, files)
        
        # Update with error
        error_code = "ERR001"
        error_desc = "Test error occurred"
        JobManager.update_job(job_id, "ERROR", error_code, error_desc)
        
        # Verify error was recorded
        jobs = JobManager.fetch_job(job_id)
        assert len(jobs) == 1
        assert jobs[0]["STATUS"] == "ERROR"
        assert jobs[0]["ERROR_CODE"] == error_code
        assert jobs[0]["ERROR_DESC"] == error_desc

    def test_log_error(self):
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
        JobManager.log_error(job_id, error_details)
        
        # Verify error was logged
        logs = JobManager.fetch_error_logs(job_id)
        assert len(logs) == 1
        log = logs[0]
        assert log["JOB_ID"] == job_id
        assert log["MODULE_NAME"] == error_details["module_name"]
        assert log["LINE_NO"] == error_details["line_no"]
        assert log["ERROR_DESC"] == error_details["error_desc"]

    def test_fetch_job(self):
        """Test fetching job details."""
        # Create a job
        job_id = "test-job-5"
        created_date = datetime.now().strftime("%Y-%m-%d")
        files = ["test.txt"]
        JobManager.create_job(job_id, created_date, files)
        
        # Fetch and verify
        jobs = JobManager.fetch_job(job_id)
        assert len(jobs) == 1
        assert jobs[0]["JOB_ID"] == job_id
        assert jobs[0]["FILE_NAME"] == "test.txt"
        assert jobs[0]["STATUS"] == "STARTED"

    def test_error_handling(self):
        """Test error handling for non-existent job."""
        with pytest.raises(DatabaseError, match="Failed to fetch job"):
            JobManager.fetch_job("non-existent-job")
