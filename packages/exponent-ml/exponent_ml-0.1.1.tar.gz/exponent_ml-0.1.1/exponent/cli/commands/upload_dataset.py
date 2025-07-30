import typer
from pathlib import Path
from exponent.core.s3_utils import analyze_dataset, upload_dataset_to_s3, create_dataset_summary

app = typer.Typer()

def run_upload(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID for organization"),
    upload_to_s3: bool = typer.Option(False, "--upload", "-u", help="Upload to S3 for cloud training")
):
    """Analyze dataset and optionally upload to S3 for cloud training."""
    
    # Validate file exists
    if not Path(dataset_path).exists():
        typer.echo(f"❌ Dataset not found: {dataset_path}")
        raise typer.Exit(1)
    
    # Generate project ID if not provided
    if not project_id:
        import uuid
        project_id = str(uuid.uuid4())
        typer.echo(f"📝 Generated project ID: {project_id}")
    
    try:
        # Analyze dataset
        typer.echo("📊 Analyzing dataset...")
        dataset_info = analyze_dataset(dataset_path)
        
        # Display analysis results
        typer.echo(f"✅ Dataset analyzed successfully!")
        typer.echo(f"📈 Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns")
        typer.echo(f"📁 File size: {dataset_info['file_size']} bytes")
        
        columns = list(dataset_info['columns'].keys())
        typer.echo(f"📊 Columns: {columns}")
        
        # Upload to S3 if requested
        s3_url = None
        if upload_to_s3:
            typer.echo("☁️  Uploading to S3...")
            try:
                s3_url = upload_dataset_to_s3(dataset_path, project_id)
                typer.echo(f"✅ Dataset uploaded successfully!")
                typer.echo(f"🔗 S3 URL: {s3_url}")
            except Exception as e:
                typer.echo(f"❌ Failed to upload to S3: {e}")
                typer.echo("💡 You can still use the dataset locally without S3")
        else:
            typer.echo("💡 Dataset will be used locally. Use --upload for cloud training.")
        
        typer.echo(f"🆔 Project ID: {project_id}")
        
        # Show dataset summary
        if s3_url:
            summary = create_dataset_summary(dataset_info, s3_url)
        else:
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
        
        typer.echo("\n📋 Dataset Summary:")
        typer.echo(summary)
        
    except Exception as e:
        typer.echo(f"❌ Error processing dataset: {e}")
        raise typer.Exit(1)

@app.callback()
def upload_callback(
    ctx: typer.Context,
    dataset_path: str = typer.Argument(None, help="Path to dataset file"),
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID for organization"),
    upload_to_s3: bool = typer.Option(False, "--upload", "-u", help="Upload to S3 for cloud training")
):
    """Upload and analyze datasets with Exponent-ML."""
    if ctx.invoked_subcommand is None:
        # No subcommand specified, but we need a dataset path
        if not dataset_path:
            typer.echo("❌ Dataset path is required")
            typer.echo("💡 Usage: exponent upload-dataset <dataset_path> [options]")
            raise typer.Exit(1)
        # Run default upload
        run_upload(dataset_path, project_id, upload_to_s3)

@app.command()
def run(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID for organization"),
    upload_to_s3: bool = typer.Option(False, "--upload", "-u", help="Upload to S3 for cloud training")
):
    """Analyze dataset and optionally upload to S3 for cloud training."""
    run_upload(dataset_path, project_id, upload_to_s3)

@app.command()
def analyze(
    dataset_path: str = typer.Argument(..., help="Path to dataset file")
):
    """Analyze dataset structure without uploading."""
    
    # Validate file exists
    if not Path(dataset_path).exists():
        typer.echo(f"❌ Dataset not found: {dataset_path}")
        raise typer.Exit(1)
    
    try:
        # Analyze dataset
        typer.echo("📊 Analyzing dataset...")
        dataset_info = analyze_dataset(dataset_path)
        
        # Display analysis results
        typer.echo(f"✅ Dataset analyzed successfully!")
        typer.echo(f"📈 Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns")
        typer.echo(f"📁 File size: {dataset_info['file_size']} bytes")
        
        typer.echo("\n📊 Column Details:")
        for col_name, col_info in dataset_info['columns'].items():
            typer.echo(f"  - {col_name}: {col_info['type']}")
            typer.echo(f"    Unique values: {col_info['unique_count']}")
            typer.echo(f"    Null values: {col_info['null_count']}")
            if col_info['sample_values']:
                typer.echo(f"    Sample values: {col_info['sample_values']}")
        
    except Exception as e:
        typer.echo(f"❌ Error analyzing dataset: {e}")
        raise typer.Exit(1)
