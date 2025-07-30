import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    ANTHROPIC_API_KEY: str
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    CLERK_SECRET_KEY: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: Optional[str] = None
    MODAL_TOKEN_ID: Optional[str] = None
    MODAL_TOKEN_SECRET: Optional[str] = None

def get_config() -> Config:
    """Load configuration from environment variables and .env file."""
    # Load from .env file if it exists
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    # Get required API key
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    return Config(
        ANTHROPIC_API_KEY=anthropic_key,
        CLERK_PUBLISHABLE_KEY=os.getenv("CLERK_PUBLISHABLE_KEY"),
        CLERK_SECRET_KEY=os.getenv("CLERK_SECRET_KEY"),
        AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID"),
        AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY"),
        AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
        S3_BUCKET=os.getenv("S3_BUCKET"),
        MODAL_TOKEN_ID=os.getenv("MODAL_TOKEN_ID"),
        MODAL_TOKEN_SECRET=os.getenv("MODAL_TOKEN_SECRET"),
    )

def check_optional_services() -> dict:
    """Check which optional services are configured."""
    config = get_config()
    
    services = {
        "s3": bool(config.AWS_ACCESS_KEY_ID and config.AWS_SECRET_ACCESS_KEY and config.S3_BUCKET),
        "modal": bool(config.MODAL_TOKEN_ID and config.MODAL_TOKEN_SECRET),
        "github": bool(os.getenv("GITHUB_TOKEN"))
    }
    
    return services
