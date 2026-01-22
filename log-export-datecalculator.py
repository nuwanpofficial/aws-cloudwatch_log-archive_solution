"""
AWS Lambda Function: CloudWatch Logs Export Date Calculator

This Lambda function calculates date ranges for the CloudWatch Logs to S3 export automation.
It returns yesterday's and today's dates in ISO format, plus a formatted S3 path component.

Required IAM Permissions: None (uses only Python standard library)

Return Format:
{
    "today": "2025-12-05T00:00:00Z",           # ISO timestamp for end of export range
    "yesterday": "2025-12-04T00:00:00Z",       # ISO timestamp for start of export range
    "yesterday_path": "2025/12/04"             # S3 path component (YYYY/MM/DD format)
}

Execution Requirements:
- Runtime: Python 3.9 or later
- Memory: 128 MB
- Timeout: 3 seconds
- Architecture: x86_64 or arm64
"""

from datetime import datetime, timedelta, timezone
import json


def lambda_handler(event, context):
    """
    Main Lambda handler function.
    
    Args:
        event (dict): Lambda event object (not used in this function)
        context (object): Lambda context object (not used in this function)
    
    Returns:
        dict: Dictionary containing today, yesterday, and yesterday_path
    """
    
    # Get current UTC time and normalize to midnight (00:00:00)
    now_utc = datetime.now(timezone.utc)
    today_midnight = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Calculate yesterday by subtracting 1 day
    yesterday_midnight = today_midnight - timedelta(days=1)
    
    # Format dates as ISO 8601 strings (required by CloudWatch Logs API)
    today_iso = today_midnight.strftime('%Y-%m-%dT%H:%M:%SZ')
    yesterday_iso = yesterday_midnight.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Format yesterday's date for S3 path structure (YYYY/MM/DD)
    yesterday_path = yesterday_midnight.strftime('%Y/%m/%d')
    
    # Construct response object
    response = {
        'today': today_iso,
        'yesterday': yesterday_iso,
        'yesterday_path': yesterday_path
    }
    
    # Log the response for debugging in CloudWatch Logs
    print(f"Date calculation result: {json.dumps(response, indent=2)}")
    
    return response
