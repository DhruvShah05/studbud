"""
AWS S3 client for file storage operations
Replaces Supabase Storage
"""
import boto3
from botocore.exceptions import ClientError
from config import Config
from typing import Optional
import os

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

S3_BUCKET = Config.S3_BUCKET_NAME


def upload_file_to_storage(file_bytes: bytes, filename: str, workspace_id: str, content_type: str = None) -> str:
    """
    Upload file to S3 storage
    Returns public URL
    """
    try:
        # Construct S3 key (path)
        s3_key = f"{workspace_id}/{filename}"
        
        # Determine content type if not provided
        if not content_type:
            content_type = get_content_type(filename)
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type
        )
        
        # Generate public URL
        public_url = f"https://{S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}"
        
        return public_url
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return None


def upload_audio_file(file_path: str, filename: str) -> str:
    """
    Upload audio file to S3 storage
    Returns public URL
    """
    try:
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Construct S3 key
        s3_key = f"audio/{filename}"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=file_data,
            ContentType='audio/mpeg'
        )
        
        # Generate public URL
        public_url = f"https://{S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}"
        
        return public_url
    except Exception as e:
        raise Exception(f"Failed to upload audio to S3: {str(e)}")


def delete_file_from_storage(file_url: str) -> bool:
    """
    Delete file from S3 storage
    Extracts S3 key from URL and deletes
    """
    try:
        # Extract S3 key from URL
        # URL format: https://bucket.s3.region.amazonaws.com/key
        s3_key = file_url.split(f"{S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/")[1]
        
        # Delete from S3
        s3_client.delete_object(
            Bucket=S3_BUCKET,
            Key=s3_key
        )
        
        return True
    except Exception as e:
        print(f"Error deleting file from S3: {e}")
        return False


def generate_presigned_url(file_url: str, expiration: int = 3600) -> Optional[str]:
    """
    Generate presigned URL for temporary secure access
    Useful for private files
    
    Args:
        file_url: Public S3 URL
        expiration: URL expiration time in seconds (default 1 hour)
    
    Returns:
        Presigned URL or None if error
    """
    try:
        # Extract S3 key from URL
        s3_key = file_url.split(f"{S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/")[1]
        
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': s3_key
            },
            ExpiresIn=expiration
        )
        
        return presigned_url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None


def get_content_type(filename: str) -> str:
    """Determine content type based on file extension"""
    ext = filename.lower().split('.')[-1]
    
    content_types = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword',
        'txt': 'text/plain',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'mp4': 'video/mp4'
    }
    
    return content_types.get(ext, 'application/octet-stream')


def check_s3_connection() -> bool:
    """Check if S3 connection is working"""
    try:
        s3_client.head_bucket(Bucket=S3_BUCKET)
        return True
    except ClientError:
        return False
