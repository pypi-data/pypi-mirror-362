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
from .uploader import upload_file, display_job_details

load_dotenv()

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
