import boto3
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from exponent.core.config import get_config

def analyze_dataset(dataset_path: str) -> Dict[str, Any]:
    """Analyze dataset structure and return column information."""
    path = Path(dataset_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    # Read dataset based on extension
    if path.suffix.lower() == '.csv':
        df = pd.read_csv(dataset_path)
    elif path.suffix.lower() == '.json':
        df = pd.read_json(dataset_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    
    # Analyze columns
    columns_info = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        sample_values = df[col].dropna().head(3).tolist()
        
        columns_info[col] = {
            'type': dtype,
            'sample_values': sample_values,
            'null_count': df[col].isnull().sum(),
            'unique_count': df[col].nunique()
        }
    
    # Detect target column
    target_column = detect_target_column(df)
    
    return {
        'columns': columns_info,
        'shape': df.shape,
        'file_size': path.stat().st_size,
        'file_path': str(path),
        'target_column': target_column
    }

def detect_target_column(df: pd.DataFrame) -> str:
    """Detect the target column based on common patterns."""
    # Common target column names
    target_patterns = [
        'target', 'label', 'class', 'y', 'output', 'prediction',
        'disease_present', 'is_disease', 'has_disease', 'infected',
        'churn', 'is_churn', 'customer_churn',
        'fraud', 'is_fraud', 'fraudulent',
        'spam', 'is_spam', 'spam_email',
        'sentiment', 'sentiment_score', 'positive',
        'price', 'target_price', 'predicted_price',
        'sales', 'target_sales', 'predicted_sales'
    ]
    
    # Check for exact matches first
    for pattern in target_patterns:
        for col in df.columns:
            if col.lower() == pattern:
                return col
    
    # Check for partial matches
    for pattern in target_patterns:
        for col in df.columns:
            if pattern in col.lower():
                return col
    
    # If no pattern match, look for binary columns (likely targets)
    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) == 2 and set(unique_vals).issubset({0, 1, True, False, '0', '1', 'True', 'False'}):
            return col
    
    # If still no match, look for the last column (common convention)
    return df.columns[-1]

def upload_dataset_to_s3(dataset_path: str, project_id: str) -> str:
    """Upload dataset to S3 and return the S3 URL. Optional for cloud training."""
    config = get_config()
    
    if not config.S3_BUCKET:
        raise ValueError("S3_BUCKET not configured")
    
    if not config.AWS_ACCESS_KEY_ID or not config.AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials not configured")
    
    # Create S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )
    
    path = Path(dataset_path)
    s3_key = f"datasets/{project_id}/{path.name}"
    
    # Upload file
    s3_client.upload_file(
        str(path),
        config.S3_BUCKET,
        s3_key
    )
    
    # Return S3 URL
    s3_url = f"https://{config.S3_BUCKET}.s3.{config.AWS_REGION}.amazonaws.com/{s3_key}"
    return s3_url

def create_dataset_summary(dataset_info: Dict[str, Any], s3_url: str) -> str:
    """Create a formatted summary of the dataset for the LLM prompt."""
    summary = f"""
**Dataset Information:**
- File: {dataset_info['file_path']}
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- S3 URL: {s3_url}

**Columns:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        summary += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            summary += f"  Sample values: {col_info['sample_values']}\n"
    
    return summary

def create_local_dataset_summary(dataset_info: Dict[str, Any], dataset_path: str) -> str:
    """Create a formatted summary of the dataset for local usage."""
    summary = f"""
**Dataset Information:**
- File: {dataset_info['file_path']}
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- Local path: {dataset_path}

**Columns:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        summary += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            summary += f"  Sample values: {col_info['sample_values']}\n"
    
    return summary

def upload_model_to_s3(model_path: str, project_id: str) -> str:
    """Upload trained model to S3."""
    config = get_config()
    
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION
        )
        
        # Create S3 key for model
        model_filename = Path(model_path).name
        s3_key = f"models/{project_id}/{model_filename}"
        
        # Upload model file
        s3_client.upload_file(model_path, config.S3_BUCKET, s3_key)
        
        # Return S3 URL
        s3_url = f"s3://{config.S3_BUCKET}/{s3_key}"
        
        print(f"✅ Model uploaded to S3: {s3_url}")
        return s3_url
        
    except Exception as e:
        print(f"❌ Error uploading model to S3: {e}")
        raise
