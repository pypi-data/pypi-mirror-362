import modal
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from exponent.core.config import get_config

def setup_modal_app():
    """Setup Modal app with required dependencies."""
    config = get_config()
    
    if not config.MODAL_TOKEN_ID or not config.MODAL_TOKEN_SECRET:
        raise ValueError("Modal credentials not configured")
    
    # Set Modal credentials
    os.environ["MODAL_TOKEN_ID"] = config.MODAL_TOKEN_ID
    os.environ["MODAL_TOKEN_SECRET"] = config.MODAL_TOKEN_SECRET
    
    # Create Modal app
    app = modal.App("exponent-ml-training")
    
    # Define image with ML dependencies
    image = modal.Image.debian_slim().pip_install([
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "boto3",
        "requests"
    ])
    
    return app, image

def create_training_function(app, image):
    """Create Modal function for training."""
    
    @app.function(
        image=image,
        timeout=3600,  # 1 hour timeout
        memory=2048,   # 2GB RAM
        cpu=2.0        # 2 CPU cores
    )
    def train_model(project_id: str, dataset_path: str, task_description: str, model_code: str, use_s3: bool = False):
        """Train ML model in Modal cloud using generated code."""
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, confusion_matrix
        import joblib
        import boto3
        from pathlib import Path
        import json
        
        print(f"🚀 Starting training for project: {project_id}")
        print(f"📊 Dataset path: {dataset_path}")
        print(f"🎯 Task: {task_description}")
        
        # Load dataset
        if use_s3:
            # Download from S3
            print("📥 Downloading dataset from S3...")
            df = pd.read_csv(dataset_path)
        else:
            # Use local file (uploaded to Modal)
            print("📥 Loading local dataset...")
            df = pd.read_csv(dataset_path)
        
        print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Execute the generated training code
        print("🤖 Executing generated training code...")
        
        # Create a safe execution environment
        local_vars = {
            'df': df,
            'pd': pd,
            'np': np,
            'train_test_split': train_test_split,
            'classification_report': classification_report,
            'confusion_matrix': confusion_matrix,
            'joblib': joblib,
            'Path': Path,
            'print': print
        }
        
        try:
            # Execute the generated code
            exec(model_code, local_vars)
            
            # Try to get the trained model from the executed code
            model = local_vars.get('model')
            if model is None:
                # Look for common model variable names
                for var_name in ['trained_model', 'clf', 'classifier', 'regressor']:
                    if var_name in local_vars:
                        model = local_vars[var_name]
                        break
            
            if model is None:
                raise ValueError("No model found in generated code")
            
            # Save model
            model_path = f"/tmp/model_{project_id}.joblib"
            joblib.dump(model, model_path)
            
            # Upload model to S3 if configured
            model_s3_path = None
            if use_s3:
                config = get_config()
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                    region_name=config.AWS_REGION
                )
                
                s3_model_key = f"models/{project_id}/model.joblib"
                s3_client.upload_file(model_path, config.S3_BUCKET, s3_model_key)
                model_s3_path = f"s3://{config.S3_BUCKET}/{s3_model_key}"
            
            # Generate training report
            report = {
                "project_id": project_id,
                "dataset_shape": df.shape,
                "model_path": model_s3_path or model_path,
                "training_completed": True,
                "model_type": type(model).__name__
            }
            
            print("✅ Training completed successfully!")
            return report
            
        except Exception as e:
            print(f"❌ Error during training: {e}")
            raise
    
    return train_model

def submit_training_job(project_id: str, dataset_path: str, task_description: str, model_code: str, use_s3: bool = False) -> str:
    """Submit a training job to Modal with generated code."""
    try:
        app, image = setup_modal_app()
        train_func = create_training_function(app, image)
        
        # Upload dataset to S3 if needed
        if use_s3:
            from exponent.core.s3_utils import upload_dataset_to_s3
            s3_url = upload_dataset_to_s3(dataset_path, project_id)
            dataset_path = s3_url
        
        # Submit job
        print(f"🚀 Submitting training job for project: {project_id}")
        result = train_func.remote(project_id, dataset_path, task_description, model_code, use_s3)
        
        return result
        
    except Exception as e:
        print(f"❌ Error submitting training job: {e}")
        raise

def submit_local_training_job(project_id: str, dataset_path: str, task_description: str, model_code: str) -> str:
    """Submit a training job using local dataset with generated code."""
    try:
        app, image = setup_modal_app()
        train_func = create_training_function(app, image)
        
        # Submit job with local dataset
        print(f"🚀 Submitting local training job for project: {project_id}")
        result = train_func.remote(project_id, dataset_path, task_description, model_code, use_s3=False)
        
        return result
        
    except Exception as e:
        print(f"❌ Error submitting training job: {e}")
        raise

def get_training_status(job_id: str) -> Dict[str, Any]:
    """Get status of a training job."""
    # This would typically query Modal's API
    # For now, return a mock status
    return {
        "job_id": job_id,
        "status": "completed",
        "progress": 100
    }

def list_training_jobs() -> List[Dict[str, Any]]:
    """List all training jobs."""
    # This would query Modal's API
    # For now, return empty list
    return []
