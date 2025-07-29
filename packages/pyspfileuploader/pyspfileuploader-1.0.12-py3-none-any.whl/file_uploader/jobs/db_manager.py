from typing import Dict, List, Optional
from datetime import datetime
from file_uploader.metadata.db_interface import job_status_tracker
from file_uploader.exceptions import DatabaseError

class JobManager:
    """Manager class for handling job operations."""
    
    @staticmethod
    def create_job(job_id: str, created_date: str, files: List[str]) -> str:
        """Create a new job entry."""
        try:
            return job_status_tracker.create_job(
                job_id, 
                created_date, 
                files,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to create job: {str(e)}")

    @staticmethod
    def update_job(job_id: str, status: str = 'COMPLETED', error_code: Optional[str] = None, error_desc: Optional[str] = None) -> None:
        """Update job status with optional error information."""
        try:
            job_status_tracker.update_job(job_id, status, error_code, error_desc)
        except Exception as e:
            raise DatabaseError(f"Failed to update job: {str(e)}")

    @staticmethod
    def fetch_job(job_id: str) -> List[Dict]:
        """Fetch job details."""
        try:
            return job_status_tracker.fetch_job(job_id)
        except Exception as e:
            raise DatabaseError(f"Failed to fetch job: {str(e)}")

    @staticmethod
    def log_error(job_id: str, error_details: Dict) -> None:
        """Log error details.

        error_details: 
        --------------
        Dictionary containing error details with keys:
            - module_name: Name of the module where the error occurred
            - script_name: Name of the script where the error occurred
            - line_no: Line number where the error occurred
            - error_desc: Description of the error
            - error_stack_trace: Optional stack trace of the error
        """
        try:
            job_status_tracker.log_error(
                job_id=job_id,
                module_name=error_details.get('module_name'),
                script_name=error_details.get('script_name'),
                line_no=error_details.get('line_no'),
                error_desc=error_details.get('error_desc'),
                error_stack_trace=error_details.get('error_stack_trace')
            )
        except Exception as e:
            raise DatabaseError(f"Failed to log error: {str(e)}")

    @staticmethod
    def fetch_error_logs(job_id: str) -> List[Dict]:
        """Fetch error logs for a specific job."""
        try:
            return job_status_tracker.fetch_error_logs(job_id)
        except Exception as e:
            raise DatabaseError(f"Failed to fetch error logs: {str(e)}")
