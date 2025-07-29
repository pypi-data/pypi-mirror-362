# print("This file uploader package is dedicated to lordship. Jay Shree Jagannatha Swami.")
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from dotenv import load_dotenv
import pandas as pd
from .jobs.db_manager import JobManager
from .src.storage_handler import get_storage_handler
from .exceptions import ConfigurationError, FileUploaderException
from .constants import BASE_PATH

load_dotenv()

def get_config() -> Dict[str, str]:
    """Get configuration from environment variables."""
    required_vars = {
        "s3": ["AWS_BUCKET_NAME", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "adls": ["ADLS_ACCOUNT_NAME", "ADLS_FILE_SYSTEM_NAME", "ADLS_CREDENTIAL"],
        "blob": ["BLOB_CONNECTION_STRING", "BLOB_CONTAINER_NAME"]
    }
    config_dict = {}
    storage_type = os.getenv("STORAGE_TYPE", "local")
    if storage_type not in ["local"] + list(required_vars.keys()):
        raise ConfigurationError(f"Unsupported storage type: {storage_type}")

    if storage_type == "local":
        config_dict["BASE_PATH"] = str(BASE_PATH)
    else:
        for var in required_vars[storage_type]:
            value = os.getenv(var)
            if not value:
                raise ConfigurationError(f"Missing required environment variable: {var}")
            config_dict[var] = value
    print(f"[DEBUG] Using config for {storage_type}: {json.dumps(config_dict, indent=2)}")
    
    return config_dict

def upload_file(file_path: str, job_id: Optional[str] = None, storage_type: Optional[str] = None, created_date: Optional[str] = None) -> str:
    """Upload a file to the configured storage."""
    try:
        # Get configuration
        config = get_config()
        
        # Generate job ID if not provided
        if not job_id:
            # Format: YYYYMMDDHHMMSS_XXXXX (timestamp + 5 random digits)
            now = datetime.now()
            job_id = f"{now.strftime('%d%m%Y%H%M%S')}_{os.urandom(3).hex()[:5]}"
        
        # Get file info
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get storage handler
        handler = get_storage_handler(
            config,
            job_id=job_id,
            created_date=created_date,
            storage_type=storage_type or os.getenv("STORAGE_TYPE", "local")
        )
        
        # Read and upload file
        with open(file_path, 'rb') as f:
            content = f.read()
            # Use upload_files which handles both regular files and zip files with validation
            uploaded_files = handler.upload_files(file_path.name, content, is_source_upload=True)
            print(f"Uploaded files: {uploaded_files}")
        
        # Create job entry
        JobManager.create_job(job_id, created_date, uploaded_files)
        
        # Update job status
        JobManager.update_job(job_id)
        
        return job_id
        
    except Exception as e:
        error_details = {
            'module_name': e.module_name if isinstance(e, FileUploaderException) else __name__,
            'script_name': e.script_name if isinstance(e, FileUploaderException) else __file__,
            'line_no': e.line_no if isinstance(e, FileUploaderException) else sys.exc_info()[2].tb_lineno,
            'error_desc': str(e)
        }
        
        if job_id:
            JobManager.log_error(job_id, error_details)
        
        raise

def format_job_details(job_details: List[Dict], error_logs: List[Dict]) -> Dict:
    """Format job details and error logs into a structured dictionary."""
    formatted_data = {
        "jobs": [{
            "job_id": job['JOB_ID'],
            "status": job['STATUS'],
            "files": job['FILE_NAME'],
            "created_date": job['CREATED_DATE'],
            "run_date": job['RUN_DATE'],
            "start_time": job['START_TIME'],
            "end_time": job['END_TIME'],
            "processing_time": job['PROCESSING_TIME']
        } for job in job_details],
        "errors": [{
            "module": error['MODULE_NAME'],
            "script": error['SCRIPT_NAME'],
            "line": error['LINE_NO'],
            "error": error['ERROR_DESC'],
            "stack_trace": error.get('ERROR_STACK_TRACE', '')
        } for error in error_logs] if error_logs else []
    }
    return formatted_data

def display_job_details(job_id: str, output_format: str = 'json') -> None:
    """
    Display job details including status and errors.
    Output format - 'json' or 'dataframe' (default: 'json')
    """
    try:
        # Get job details
        job_details = JobManager.fetch_job(job_id)
        error_logs = JobManager.fetch_error_logs(job_id)
        
        # Format data
        formatted_data = format_job_details(job_details, error_logs)
        
        if output_format.lower() == 'dataframe':
            print("\nJob Details (DataFrame View):")
            print("-" * 30)
            if formatted_data['jobs']:
                jobs_df = pd.DataFrame(formatted_data['jobs'])
                print("\nJobs:")
                print(jobs_df.to_string(index=False))
            
            if formatted_data['errors']:
                print("\nErrors:")
                errors_df = pd.DataFrame(formatted_data['errors'])
                print(errors_df.to_string(index=False))
        else:  # default to JSON
            print("\nJob Details (JSON View):")
            print("*" * 30)
            print(json.dumps(formatted_data, indent=2))
    
    except Exception as e:
        print(f"Error fetching job details: {e}", file=sys.stderr)
        sys.exit(1)

