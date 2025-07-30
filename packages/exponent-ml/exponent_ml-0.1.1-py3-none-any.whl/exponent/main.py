import typer
from exponent.cli.commands import init, train, deploy
from exponent.cli.commands.analyze import run_analysis
from exponent.cli.commands.interactive import app as interactive_app
from exponent.core.auth import auth_manager

app = typer.Typer(
    name="exponent",
    help="Exponent-ML: Build ML models from the CLI using LLMs and Modal",
    add_completion=False,
    no_args_is_help=True
)

# Add commands
app.add_typer(init.app, name="init", help="Initialize new ML project")
app.add_typer(interactive_app, name="interactive", help="Interactive wizard for building ML models end-to-end")

# Add analyze command with authentication
@app.command()
@auth_manager.require_auth()
def analyze(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    prompt: str = typer.Option(None, "--prompt", "-p", help="Analysis prompt for AI"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory for analysis")
):
    """Analyze datasets with AI-powered analysis and visualization."""
    run_analysis(dataset_path, prompt, output_dir)

# Add train command with authentication
@app.command()
@auth_manager.require_auth()
def train(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to train"),
    dataset_path: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    task_description: str = typer.Option(None, "--task", "-t", help="Task description"),
    cloud: bool = typer.Option(False, "--cloud", "-c", help="Use cloud training (Modal)"),
    use_s3: bool = typer.Option(False, "--s3", help="Upload dataset to S3 for cloud training"),
    status: str = typer.Option(None, "--status", help="Check status of training job"),
    list_jobs: bool = typer.Option(False, "--list", help="List all training jobs")
):
    """Train ML models with Exponent-ML."""
    if status:
        # Check status of specific job
        from exponent.core.modal_runner import get_training_status
        try:
            status_info = get_training_status(status)
            typer.echo(f"📊 Job Status: {status_info}")
        except Exception as e:
            typer.echo(f"❌ Error getting job status: {e}")
            raise typer.Exit(1)
    elif list_jobs:
        # List all jobs
        from exponent.core.modal_runner import list_training_jobs
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
    else:
        # Run default training
        train.app.get_command("run")(project_id, dataset_path, task_description, cloud, use_s3)

app.add_typer(deploy.app, name="deploy", help="Deploy projects to GitHub")

@app.command()
def login(
    provider: str = typer.Option(None, "--provider", "-p", help="OAuth provider (google, github)")
):
    """Authenticate with Exponent-ML."""
    if auth_manager.authenticate_user(provider):
        typer.echo("✅ Login successful!")
    else:
        typer.echo("❌ Login failed!")
        raise typer.Exit(1)

@app.command()
def logout():
    """Logout from Exponent-ML."""
    auth_manager.clear_token()
    typer.echo("✅ Logged out successfully!")

@app.command()
def status():
    """Check authentication status."""
    if auth_manager.is_authenticated():
        user_info = auth_manager.get_user_info()
        typer.echo("✅ Authenticated")
        if user_info:
            typer.echo(f"👤 User: {user_info.get('name', 'Unknown')}")
            typer.echo(f"📧 Email: {user_info.get('email', 'Unknown')}")
            typer.echo(f"🔗 Provider: {user_info.get('provider', 'Unknown')}")
    else:
        typer.echo("❌ Not authenticated")
        typer.echo("💡 Run 'exponent login' to authenticate")

@app.command()
def version():
    """Show version information."""
    typer.echo("Exponent-ML v0.1.0")

@app.command()
def help():
    """Show detailed help and examples."""
    typer.echo("""
🧠 Exponent-ML: Build ML models from the CLI using LLMs and Modal

📋 Quick Start:
1. Initialize a project: exponent init quick "make a spam classifier"
2. Train your model: exponent train
3. Deploy to GitHub: exponent deploy

📚 Commands:

🔧 INIT - Create new ML projects
  exponent init quick "task description" --dataset data.csv
  exponent init run --task "classify emails" --dataset emails.csv

🎯 INTERACTIVE - Full agentic workflow
  exponent interactive wizard  # Complete ML pipeline

📊 ANALYZE - Analyze datasets with AI-powered analysis
  exponent analyze data.csv
  exponent analyze data.csv --prompt "Show customer churn patterns"
  exponent analyze data.csv --output my_analysis

🚀 TRAIN - Train ML models
  exponent train  # Train in current directory
  exponent train --project-id abc123 --dataset data.csv --task "classify"
  exponent train --cloud  # Use cloud training
  exponent train --status <job_id>  # Check training status
  exponent train --list  # List all jobs

🌐 DEPLOY - Deploy to GitHub
  exponent deploy  # Deploy current project
  exponent deploy --project-id abc123
  exponent deploy list  # List GitHub repos

💡 Examples:

# Quick start with plant disease classification
exponent init quick "make a plant disease classifier" --dataset plant_data.csv
exponent train
exponent deploy

# Interactive project creation
exponent interactive wizard
# Follow the prompts...

# Dataset analysis
exponent analyze data.csv --prompt "Show customer churn patterns"
exponent train --project-id my-project --dataset data.csv --task "predict sales" --cloud

# Check training status
exponent train --status job_12345

# Deploy to GitHub with custom name
exponent deploy --name my-awesome-model

📖 For more help on specific commands:
  exponent <command> --help
  exponent init --help
  exponent interactive --help
  exponent train --help
  exponent deploy --help
  exponent analyze --help
""")

if __name__ == "__main__":
    app()