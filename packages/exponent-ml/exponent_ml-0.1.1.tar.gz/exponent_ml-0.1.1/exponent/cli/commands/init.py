import typer
import inquirer
from pathlib import Path
from exponent.core.code_gen import generate_code_with_dataset_analysis, generate_code_from_prompt
from exponent.core.s3_utils import analyze_dataset
from exponent.core.auth import auth_manager

app = typer.Typer()

def run_initialization(
    task: str = typer.Option(None, "--task", "-t", help="ML task description"),
    dataset: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    interactive: bool = typer.Option(True, "--interactive", "-i", help="Run in interactive mode")
):
    """Initialize a new ML project with interactive wizard."""
    
    if interactive:
        # Interactive wizard flow
        typer.echo("🧠 Let's set up your ML project!")
        
        # Get task description
        if not task:
            task = typer.prompt("💬 What task do you want to solve? (e.g., 'Predict email spam based on subject and body')")
        
        # Get dataset path
        if not dataset:
            dataset = typer.prompt("📁 Dataset path? (CSV or JSON file)")
        
        # Validate dataset exists
        if dataset and not Path(dataset).exists():
            typer.echo(f"❌ Dataset not found: {dataset}")
            raise typer.Exit(1)
    
    # Analyze dataset if provided
    dataset_info = None
    if dataset:
        try:
            typer.echo("📊 Analyzing dataset...")
            dataset_info = analyze_dataset(dataset)
            
            # Display column information
            columns = list(dataset_info['columns'].keys())
            typer.echo(f"📊 Columns detected: {columns}")
            typer.echo(f"📈 Dataset shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns")
            
        except Exception as e:
            typer.echo(f"⚠️  Warning: Could not analyze dataset: {e}")
            dataset = None
    
    # Generate code
    typer.echo("🤖 Generating code with LLM...")
    
    try:
        if dataset and dataset_info:
            project_id, created_files, dataset_analysis = generate_code_with_dataset_analysis(task, dataset)
        else:
            project_id, created_files = generate_code_from_prompt(task, dataset)
        
        # Display results
        typer.echo(f"✅ Project created with ID: {project_id}")
        typer.echo(f"📁 Project location: ~/.exponent/{project_id}")
        typer.echo("📄 Generated files:")
        for file_path in created_files:
            typer.echo(f"  - {Path(file_path).name}")
        
        # Show next steps
        typer.echo("\n🚀 Next steps:")
        typer.echo("1. Review the generated code")
        typer.echo("2. Run 'exponent train' to train your model")
        typer.echo("3. Run 'exponent deploy' to deploy to GitHub")
        
    except Exception as e:
        typer.echo(f"❌ Error generating code: {e}")
        raise typer.Exit(1)

@app.callback()
def init_callback(
    ctx: typer.Context,
    task: str = typer.Option(None, "--task", "-t", help="ML task description"),
    dataset: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    interactive: bool = typer.Option(True, "--interactive", "-i", help="Run in interactive mode")
):
    """Initialize new ML projects with Exponent-ML."""
    if ctx.invoked_subcommand is None:
        # No subcommand specified, run default initialization
        run_initialization(task, dataset, interactive)

@app.command()
def run(
    task: str = typer.Option(None, "--task", "-t", help="ML task description"),
    dataset: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file"),
    interactive: bool = typer.Option(True, "--interactive", "-i", help="Run in interactive mode")
):
    """Initialize a new ML project with interactive wizard."""
    run_initialization(task, dataset, interactive)

@app.command()
def quick(
    task: str = typer.Argument(..., help="ML task description"),
    dataset: str = typer.Option(None, "--dataset", "-d", help="Path to dataset file")
):
    """Quick initialization without interactive prompts."""
    run_initialization(task=task, dataset=dataset, interactive=False)