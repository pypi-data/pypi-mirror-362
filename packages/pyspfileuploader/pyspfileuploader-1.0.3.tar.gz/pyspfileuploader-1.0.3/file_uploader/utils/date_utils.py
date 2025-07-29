from datetime import datetime

def format_date(date: datetime) -> str:
    """Format a date in DD-MM-YYYY format."""
    return date.strftime("%d-%m-%Y")

def format_datetime(date: datetime) -> str:
    """Format a datetime in DD-MM-YYYY HH:mm:ss format."""
    return date.strftime("%d-%m-%Y %H:%M:%S")
