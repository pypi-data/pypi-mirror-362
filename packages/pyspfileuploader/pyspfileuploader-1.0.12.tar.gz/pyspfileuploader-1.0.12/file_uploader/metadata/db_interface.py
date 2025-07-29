import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from file_uploader.utils.date_utils import format_date, format_datetime
from file_uploader.constants import (
    DB_JOB_CREATE_QUERY, 
    DB_JOB_INSERT_QUERY, 
    DB_JOB_UPDATE_QUERY,
    DB_JOB_FETCH_QUERY,
    DB_LOG_CREATE_QUERY,
    DB_LOG_INSERT_QUERY,
    DB_LOG_FETCH_QUERY,
)
from file_uploader.exceptions import DatabaseError


class DbUtils:
    """Real world implementation of a database utility class for managing 
    SQLite database connections and operations."""
    
    def __init__(self):
        """Initialize the database connection."""
        self.db_path = Path("data").joinpath("app_db", "file_tracker.db")
        self._initialize_db()

    def _get_db_connection(self):
        """Get a connection to the SQLite database."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_db(self):
        """Initialize the database by creating necessary tables."""
        conn = self._get_db_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(DB_JOB_CREATE_QUERY)
            cursor.execute(DB_LOG_CREATE_QUERY)

    def create_job(self, job_id: str, created_date: str, files: List[str]) -> str:
        """Create a new job entry in the database."""
        conn = self._get_db_connection()
        current_time = format_datetime(datetime.now())
        
        try:
            with conn:
                cursor = conn.cursor()
                for file_name in files:
                    cursor.execute(
                        DB_JOB_INSERT_QUERY,
                        (
                            job_id, 
                            file_name, 
                            'STARTED',
                            None,           # error_code 
                            None,           # error_desc
                            created_date,
                            datetime.now().strftime('%d-%m-%Y'),
                            current_time,
                            None,
                            None
                        )
                    )
            return job_id
        except sqlite3.Error as e:
            error_frame = traceback.extract_tb(e.__traceback__)[-1]  # Get the frame where error occurred
            self.log_error(
                job_id=job_id,
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno,
                error_desc=str(e),
                error_stack_trace=traceback.format_exc()
            )
            raise DatabaseError(
                message=f"Database error while creating job: {str(e)}",
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno
            )

    def update_job(self, job_id: str, status: str = 'COMPLETED', error_code: Optional[str] = None, error_desc: Optional[str] = None) -> None:
        """Update the job status in the database."""
        conn = self._get_db_connection()
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        try:
            with conn:
                cursor = conn.cursor()
                # Get the start time to calculate processing time
                cursor.execute("SELECT START_TIME FROM JOB_STATUS WHERE JOB_ID = ?", (job_id,))
                row = cursor.fetchone()
                start_time = datetime.strptime(row['START_TIME'], '%d-%m-%Y %H:%M:%S')
                processing_time = (datetime.now() - start_time).total_seconds()
                
                cursor.execute(
                    DB_JOB_UPDATE_QUERY,
                    (status, error_code, error_desc, current_time, processing_time, job_id)
                )
        except sqlite3.Error as e:
            error_frame = traceback.extract_tb(e.__traceback__)[-1]
            self.log_error(
                job_id=job_id,
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno,
                error_desc=str(e),
                error_stack_trace=traceback.format_exc()
            )
            raise DatabaseError(
                message=f"Database error while updating job: {str(e)}",
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno
            )
        except ValueError as e:
            error_frame = traceback.extract_tb(e.__traceback__)[-1]
            error_msg = f"Invalid datetime format in START_TIME for job {job_id}"
            self.log_error(
                job_id=job_id,
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno,
                error_desc=error_msg,
                error_stack_trace=traceback.format_exc()
            )
            raise DatabaseError(
                message=error_msg,
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno
            )

    def fetch_job(self, job_id: str) -> List[Dict]:
        """Fetch job details from the database."""
        conn = self._get_db_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(DB_JOB_FETCH_QUERY, (job_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            error_frame = traceback.extract_tb(e.__traceback__)[-1]
            self.log_error(
                job_id=job_id,
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno,
                error_desc=str(e),
                error_stack_trace=traceback.format_exc()
            )
            raise DatabaseError(
                message=f"Database error while fetching job: {str(e)}",
                module_name=self.__class__.__module__,
                script_name=error_frame.filename,
                line_no=error_frame.lineno
            )

    def log_error(self, job_id: str, module_name: str, script_name: str, 
                line_no: int, error_desc: str, error_stack_trace: Optional[str] = None) -> None:
        """Log error details to the database."""
        conn = self._get_db_connection()
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    DB_LOG_INSERT_QUERY,
                    (
                        job_id,
                        module_name,
                        script_name,
                        line_no,
                        error_desc,
                        error_stack_trace,
                        current_time
                    )
                )
        except sqlite3.Error as e:
            # If we can't log to the database, print to stderr and raise the error
            print(f"Failed to log error to database: {str(e)}", file=sys.stderr)
            raise DatabaseError(f"Failed to log error to database: {str(e)}")

    def fetch_error_logs(self, job_id: str) -> List[Dict]:
        """Fetch error logs for a specific job from the database."""
        conn = self._get_db_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(DB_LOG_FETCH_QUERY, (job_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            error_msg = f"Database error while fetching error logs: {str(e)}"
            print(f"Error fetching logs: {error_msg}", file=sys.stderr)
            raise DatabaseError(error_msg)

job_status_tracker = DbUtils()



