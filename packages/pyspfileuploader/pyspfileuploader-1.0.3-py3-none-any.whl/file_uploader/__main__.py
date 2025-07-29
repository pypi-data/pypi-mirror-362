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
    
    storage_type = os.getenv("STORAGE_TYPE", "local")
    if storage_type not in ["local"] + list(required_vars.keys()):
        raise ConfigurationError(f"Unsupported storage type: {storage_type}")
    
    config = {}
    if storage_type == "local":
        config["BASE_PATH"] = str(BASE_PATH)
    else:
        for var in required_vars[storage_type]:
            value = os.getenv(var)
            if not value:
                raise ConfigurationError(f"Missing required environment variable: {var}")
            config[var] = value
    
    return config

def upload_file(file_path: str, job_id: Optional[str] = None, storage_type: Optional[str] = None, created_date: Optional[str] = None) -> str:
    """
    Upload a file to the configured storage.
    
    Args:
        file_path: Path to the file to upload
        job_id: Optional job ID for tracking
        storage_type: Optional storage type override
        created_date: Optional created date (format: DD-MM-YYYY)
    
    Returns:
        job_id: The ID of the created job
    """
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
    
    Args:
        job_id: The job ID to display details for
        output_format: Output format - 'json' or 'dataframe' (default: 'json')
    """
    try:
        # Get job details
        job_details = JobManager.fetch_job(job_id)
        error_logs = JobManager.fetch_error_logs(job_id)
        
        # Format data
        formatted_data = format_job_details(job_details, error_logs)
        
        if output_format.lower() == 'dataframe':
            print("\nJob Details (DataFrame View):")
            print("-" * 50)
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
            print("-" * 50)
            print(json.dumps(formatted_data, indent=2))
    
    except Exception as e:
        print(f"Error fetching job details: {e}", file=sys.stderr)
        sys.exit(1)

def parse_upload_args(args: list) -> tuple:
    """Parse upload command arguments flexibly."""
    file_paths = []
    job_id = None
    storage_type = None
    created_date = None
    
    # First argument must be a file, collect all consecutive file paths
    for arg in args:
        # If we hit a special argument, stop collecting file paths
        if arg in ["local", "s3", "adls", "blob"] or \
           ("-" in arg and len(arg.split("-")) == 3) or \
           (not arg.endswith(('.txt', '.dat', '.ksh', '.dml', '.xfr', '.xlsx', '.docx', '.csv', '.json', '.xml', '.zip'))):
            break
        file_paths.append(arg)
    
    # Look at remaining arguments after file paths
    remaining_args = args[len(file_paths):]
    for arg in remaining_args:
        if arg in ["local", "s3", "adls", "blob"]:
            storage_type = arg
        elif "-" in arg and len(arg.split("-")) == 3:  # Looks like a date DD-MM-YYYY
            created_date = arg
        else:
            job_id = arg  # If it's not a storage type or date, treat as job_id
            
    return file_paths, job_id, storage_type, created_date

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Upload files:")
        print("    file-uploader upload <file1> [file2] [file3] ... [options]")
        print("\nSupported file types:")
        print("    - Individual files: .txt, .csv, .json, .xml")
        print("    - ZIP archives: .zip (will be automatically extracted)")
        print("\nOptions (can be in any order after files):")
        print("    <job_id>      : Custom job ID (optional)")
        print("    <storage_type>: local|s3|adls|blob (optional, default: local)")
        print("    <date>        : DD-MM-YYYY (optional, default: current date)")
        print("\nExamples:")
        print("  Single file:")
        print("    file-uploader upload data.txt")
        print("    file-uploader upload data.txt s3")
        print("  ZIP file (contents will be extracted):")
        print("    file-uploader upload files.zip")
        print("    file-uploader upload files.zip s3 13-07-2025")
        print("  Multiple files:")
        print("    file-uploader upload file1.txt file2.txt file3.txt")
        print("    file-uploader upload *.txt")
        print("    file-uploader upload file1.zip file2.txt s3 13-07-2025")
        print("\nGet job details:")
        print("  file-uploader status <job_id> [format]")
        print("\nFormat options:")
        print("  json      : Display output in JSON format (default)")
        print("  dataframe : Display output in DataFrame format")
        print("\nExample:")
        print("  file-uploader status myjob123")
        print("  file-uploader status myjob123 dataframe")
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "upload":
        if len(sys.argv) < 3:
            print("Error: At least one file path required for upload")
            sys.exit(1)
        file_paths, job_id, storage_type, created_date = parse_upload_args(sys.argv[2:])
        
        if not file_paths:
            print("Error: No valid files specified")
            sys.exit(1)
            
        try:
            # Upload first file with generated/provided job ID
            first_file = file_paths[0]
            job_id = upload_file(first_file, job_id, storage_type, created_date)
            if first_file.lower().endswith('.zip'):
                print(f"ZIP file processed successfully: {first_file}")
            else:
                print(f"File uploaded successfully: {first_file}")
            
            # Upload remaining files with same job ID
            for file_path in file_paths[1:]:
                try:
                    upload_file(file_path, job_id, storage_type, created_date)
                    if file_path.lower().endswith('.zip'):
                        print(f"ZIP file processed successfully: {file_path}")
                    else:
                        print(f"File uploaded successfully: {file_path}")
                except Exception as e:
                    print(f"Error uploading {file_path}: {e}", file=sys.stderr)
            
            print(f"\nAll files processed under Job ID: {job_id}")
            # Show job details after all uploads
            # display_job_details(job_id)
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("Error: Job ID required for status check")
            sys.exit(1)
            
        # Parse output_format option if provided
        job_id = sys.argv[2]
        output_format = 'json'  # default
        if len(sys.argv) > 3:
            if sys.argv[3] in ['json', 'dataframe']:
                output_format = sys.argv[3]
            else:
                print("Warning: Invalid format option. Using default (json)")
        
        display_job_details(job_id, output_format)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
