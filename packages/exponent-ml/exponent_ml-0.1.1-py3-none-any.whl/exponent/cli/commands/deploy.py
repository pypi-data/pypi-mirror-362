import typer
from pathlib import Path
from exponent.core.github_utils import deploy_to_github, list_github_repos

app = typer.Typer()

def run_deployment(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    project_name: str = typer.Option(None, "--name", "-n", help="GitHub repository name"),
    project_path: str = typer.Option(None, "--path", help="Path to project directory")
):
    """Deploy ML project to GitHub."""
    
    if not project_id:
        # Try to find project in current directory
        current_dir = Path.cwd()
        if (current_dir / "train.py").exists() and (current_dir / "model.py").exists():
            typer.echo("🎯 Found ML project in current directory")
            project_path = str(current_dir)
            # Generate a project ID from directory name
            project_id = current_dir.name
        else:
            typer.echo("❌ No project ID provided and no ML project found in current directory")
            typer.echo("💡 Use 'exponent init' to create a new project first")
            raise typer.Exit(1)
    
    if not project_path:
        # Try to find project in ~/.exponent
        home_dir = Path.home() / ".exponent" / project_id
        if home_dir.exists():
            project_path = str(home_dir)
        else:
            typer.echo(f"❌ Project not found: {project_id}")
            raise typer.Exit(1)
    
    typer.echo(f"🚀 Deploying project {project_id} to GitHub...")
    
    try:
        result = deploy_to_github(project_id, Path(project_path), project_name)
        
        if result["deployment_successful"]:
            typer.echo("✅ Deployment successful!")
            typer.echo(f"🌐 GitHub URL: {result['github_url']}")
            typer.echo("📋 Next steps:")
            typer.echo("1. Set up GitHub secrets for automated training")
            typer.echo("2. Push changes to trigger training workflow")
        else:
            typer.echo(f"❌ Deployment failed: {result.get('error', 'Unknown error')}")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Error deploying to GitHub: {e}")
        raise typer.Exit(1)

@app.callback()
def deploy_callback(
    ctx: typer.Context,
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    project_name: str = typer.Option(None, "--name", "-n", help="GitHub repository name"),
    project_path: str = typer.Option(None, "--path", help="Path to project directory")
):
    """Deploy ML projects to GitHub with Exponent-ML."""
    if ctx.invoked_subcommand is None:
        # No subcommand specified, run default deployment
        run_deployment(project_id, project_name, project_path)

@app.command()
def run(
    project_id: str = typer.Option(None, "--project-id", "-p", help="Project ID to deploy"),
    project_name: str = typer.Option(None, "--name", "-n", help="GitHub repository name"),
    project_path: str = typer.Option(None, "--path", help="Path to project directory")
):
    """Deploy ML project to GitHub."""
    run_deployment(project_id, project_name, project_path)

@app.command()
def list():
    """List GitHub repositories created by Exponent-ML."""
    try:
        repos = list_github_repos()
        if repos:
            typer.echo("📋 Exponent-ML GitHub Repositories:")
            for repo in repos:
                typer.echo(f"  - {repo['name']}: {repo['url']}")
                typer.echo(f"    Created: {repo['created_at']}")
        else:
            typer.echo("📋 No Exponent-ML repositories found")
    except Exception as e:
        typer.echo(f"❌ Error listing repositories: {e}")
        raise typer.Exit(1)
