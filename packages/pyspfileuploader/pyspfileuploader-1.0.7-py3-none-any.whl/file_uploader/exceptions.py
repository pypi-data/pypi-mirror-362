import sys
import traceback
from typing import Optional

class FileUploaderException(Exception):
    """Base exception class for File Uploader package."""
    def __init__(self, message: str, module_name: Optional[str] = None, 
                 script_name: Optional[str] = None, line_no: Optional[int] = None):
        self.message = message
        
        # Get the caller's frame info
        caller_frame = None
        try:
            # Walk up the stack to find the first frame outside of the exception classes
            for frame in traceback.extract_stack():
                if 'exceptions.py' not in frame.filename:
                    caller_frame = frame
                    break
        except Exception:
            # Fallback to a simple method if stack walking fails
            caller_frame = traceback.extract_stack()[-3]  # -3 to skip __init__ and the raising frame
            
        # Set error location details
        self.module_name = module_name or self.__class__.__module__
        self.script_name = script_name or (caller_frame.filename if caller_frame else '<unknown>')
        self.line_no = line_no or (caller_frame.lineno if caller_frame else 0)
        self.error_desc = f"{self.__class__.__name__}: {message}"
        super().__init__(self.error_desc)

    def __str__(self):
        return f"""
                Error Details-
                Module: {self.module_name}
                Script: {self.script_name}
                Line Number: {self.line_no}
                Error Description: {self.error_desc}
                """

class StorageError(FileUploaderException):
    """Raised when there's an error with storage operations."""
    pass

class DatabaseError(FileUploaderException):
    """Raised when there's an error with database operations."""
    pass

class ConfigurationError(FileUploaderException):
    """Raised when there's an error with configuration."""
    pass

class ValidationError(FileUploaderException):
    """Raised when there's an error with input validation."""
    pass
