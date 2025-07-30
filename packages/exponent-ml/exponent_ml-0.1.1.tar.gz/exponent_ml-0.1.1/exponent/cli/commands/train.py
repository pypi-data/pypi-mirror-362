import typer
from pathlib import Path
from exponent.core.modal_runner import submit_training_job, submit_local_training_job, get_training_status, list_training_jobs

app = typer.Typer()

def load_model_code(project_id: str) -> str:
    """Load the generated model code from the project directory."""
    # Try to find project in ~/.exponent
    home_dir = Path.home() / ".exponent" / project_id
    if home_dir.exists():
        # Look for model.py or train.py
        model_file = home_dir / "model.py"
        train_file = home_dir / "train.py"
        
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                return f.read()
        elif train_file.exists():
            with open(train_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"No model.py or train.py found in project {project_id}")
    else:
        # Try current directory
        current_dir = Path.cwd()
        model_file = current_dir / "model.py"
        train_file = current_dir / "train.py"
        
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                return f.read()
        elif train_file.exists():
            with open(train_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise FileNotFoundError("No model.py or train.py found in current directory")

@app.command()
def run(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to train"),
    dataset_path: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    task_description: str = typer.Option(None, "--task", "-t", help="Task description"),
    cloud: bool = typer.Option(False, "--cloud", "-c", help="Use cloud training (Modal)"),
    use_s3: bool = typer.Option(False, "--s3", help="Upload dataset to S3 for cloud training")
):
    """Train an ML model locally or in the cloud using generated code."""
    
    if not project_id:
        # Try to find project in current directory
        current_dir = Path.cwd()
        if (current_dir / "train.py").exists():
            typer.echo("🎯 Found train.py in current directory")
            typer.echo("🚀 Starting local training...")
            
            # Run local training
            import subprocess
            try:
                result = subprocess.run(["python", "train.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    typer.echo("✅ Local training completed successfully!")
                    typer.echo(result.stdout)
                else:
                    typer.echo(f"❌ Local training failed: {result.stderr}")
                    raise typer.Exit(1)
            except Exception as e:
                typer.echo(f"❌ Error running local training: {e}")
                raise typer.Exit(1)
        else:
            typer.echo("❌ No project ID provided and no train.py found in current directory")
            typer.echo("💡 Use 'exponent init' to create a new project first")
            raise typer.Exit(1)
    else:
        # Cloud training with Modal
        if not dataset_path or not task_description:
            typer.echo("❌ Both --dataset and --task are required for cloud training")
            raise typer.Exit(1)
        
        # Load the generated model code
        try:
            model_code = load_model_code(project_id)
            typer.echo("✅ Loaded generated model code")
        except Exception as e:
            typer.echo(f"❌ Error loading model code: {e}")
            raise typer.Exit(1)
        
        if cloud:
            typer.echo(f"🚀 Submitting cloud training job for project: {project_id}")
            
            try:
                result = submit_training_job(project_id, dataset_path, task_description, model_code, use_s3=use_s3)
                typer.echo("✅ Cloud training job submitted successfully!")
                typer.echo(f"📊 Job details: {result}")
                
            except Exception as e:
                typer.echo(f"❌ Error submitting cloud training job: {e}")
                raise typer.Exit(1)
        else:
            # Local training with Modal (dataset stays local)
            typer.echo(f"🚀 Submitting local training job for project: {project_id}")
            
            try:
                result = submit_local_training_job(project_id, dataset_path, task_description, model_code)
                typer.echo("✅ Local training job submitted successfully!")
                typer.echo(f"📊 Job details: {result}")
                
            except Exception as e:
                typer.echo(f"❌ Error submitting local training job: {e}")
                raise typer.Exit(1)

@app.command()
def status(
    job_id: str = typer.Argument(..., help="Training job ID")
):
    """Check status of a training job."""
    try:
        status_info = get_training_status(job_id)
        typer.echo(f"📊 Job Status: {status_info}")
    except Exception as e:
        typer.echo(f"❌ Error getting job status: {e}")
        raise typer.Exit(1)

@app.command()
def list():
    """List all training jobs."""
    try:
        jobs = list_training_jobs()
        if jobs:
            typer.echo("📋 Training Jobs:")
            for job in jobs:
                typer.echo(f"  - {job}")
        else:
            typer.echo("📋 No training jobs found")
    except Exception as e:
        typer.echo(f"❌ Error listing jobs: {e}")
        raise typer.Exit(1)
