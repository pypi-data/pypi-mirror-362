import typer
import inquirer
from pathlib import Path
import os
import sys
from exponent.core.code_gen import generate_code_with_dataset_analysis
from exponent.core.s3_utils import analyze_dataset
from exponent.core.error_agent import ErrorAgent

app = typer.Typer()

def welcome_message():
    """Display welcome message and introduction to Exponent."""
    typer.echo("""
🧠 Welcome to Exponent-ML - Your AI-Powered ML Development Assistant!

Exponent-ML helps you build, train, and deploy machine learning models with:
• 🤖 AI-powered code generation
• 📊 Automatic dataset analysis
• 🚀 Cloud training with Modal
• 🌐 Easy deployment to GitHub/AWS
• 🔧 Intelligent error handling

Let's build your ML model together! 🚀
""")

def get_user_input() -> dict:
    """Get user input for model requirements."""
    typer.echo("\n📋 Let's start by understanding your project requirements...")
    
    questions = [
        inquirer.Text('prompt', 
                     message="💬 What kind of ML model do you want to build? (e.g., 'Build a spam classifier', 'Create a sales prediction model')"),
        inquirer.Text('dataset_path',
                     message="📁 Path to your dataset file (CSV, JSON, etc.)"),
        inquirer.Confirm('has_gpu',
                        message="🖥️ Do you want to use GPU for training?",
                        default=True),
        inquirer.Text('hyperparameters',
                     message="⚙️ Any specific hyperparameters? (optional, e.g., 'learning_rate=0.001, epochs=100')"),
        inquirer.Confirm('deploy_after',
                        message="🌐 Do you want to deploy after training?",
                        default=True)
    ]
    
    answers = inquirer.prompt(questions)
    return answers

def sanitize_project_name(prompt: str) -> str:
    """Convert prompt to a valid project name."""
    import re
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', prompt.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    # Limit length to avoid overly long names
    sanitized = sanitized[:50]
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it's not empty
    if not sanitized:
        sanitized = "ml_project"
    return sanitized

def create_project_structure(project_name: str) -> Path:
    """Create project directory structure."""
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    
    typer.echo(f"📁 Created project directory: {project_dir}")
    return project_dir

def analyze_dataset_and_generate_code(project_info: dict) -> dict:
    """Analyze dataset and generate initial code."""
    typer.echo(f"\n📊 Analyzing dataset: {project_info['dataset_path']}")
    
    try:
        # Analyze dataset
        dataset_info = analyze_dataset(project_info['dataset_path'])
        
        typer.echo(f"✅ Dataset analyzed successfully!")
        typer.echo(f"📈 Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns")
        typer.echo(f"📁 File size: {dataset_info['file_size']} bytes")
        
        columns = list(dataset_info['columns'].keys())
        typer.echo(f"📊 Columns: {columns}")
        
        # Generate code using existing function
        typer.echo(f"\n🤖 Generating code for: {project_info['prompt']}")
        
        project_id, created_files, dataset_analysis = generate_code_with_dataset_analysis(
            project_info['prompt'], 
            project_info['dataset_path']
        )
        
        # Copy files to project directory
        import shutil
        for file_path in created_files:
            if Path(file_path).exists():
                shutil.copy2(file_path, project_info['dir'])
        
        # Copy dataset to project directory
        dataset_name = Path(project_info['dataset_path']).name
        shutil.copy2(project_info['dataset_path'], project_info['dir'] / dataset_name)
        
        typer.echo(f"✅ Code generation complete!")
        typer.echo(f"📄 Generated files:")
        for file_path in created_files:
            if Path(file_path).exists():
                typer.echo(f"  - {Path(file_path).name}")
        
        # Update project info
        project_info['dataset_info'] = dataset_info
        project_info['created_files'] = created_files
        project_info['project_id'] = project_id
        
        return project_info
        
    except Exception as e:
        typer.echo(f"❌ Error during dataset analysis: {e}")
        raise typer.Exit(1)

def interactive_code_improvement(project_info: dict) -> dict:
    """Interactive loop for improving the generated code."""
    typer.echo(f"\n🔄 Interactive Code Improvement Mode")
    typer.echo(f"💡 You can ask questions about the code or request improvements.")
    typer.echo(f"💡 Type 'done' when you're satisfied with the code.")
    
    # Initialize error agent for code improvements
    error_agent = ErrorAgent()
    
    while True:
        # Show current files
        typer.echo(f"\n📄 Current project files:")
        for file_path in project_info['created_files']:
            if Path(file_path).exists():
                typer.echo(f"  - {Path(file_path).name}")
        
        # Get user input
        user_question = typer.prompt(
            "\n💬 What would you like to improve? (or type 'done' to continue)",
            default="done"
        )
        
        if user_question.lower() in ['done', 'exit', 'quit']:
            typer.echo("✅ Moving to next step...")
            break
        
        if not user_question.strip():
            continue
        
        # Process the improvement request
        try:
            typer.echo(f"🤖 Processing improvement request...")
            
            # Generate improved code based on user request
            improved_code = generate_code_improvement(
                project_info['prompt'],
                user_question,
                project_info['dataset_info'],
                project_info['created_files']
            )
            
            # Apply the improvements
            project_info = apply_code_improvements(project_info, improved_code)
            
            typer.echo("✅ Code improvements applied!")
            
        except Exception as e:
            typer.echo(f"❌ Error applying improvements: {e}")
            typer.echo("💡 You can try asking a different question or type 'done' to continue.")
    
    return project_info

def generate_code_improvement(original_prompt: str, improvement_request: str, dataset_info: dict, current_files: list) -> dict:
    """Generate improved code based on user request."""
    from exponent.core.config import get_config
    import anthropic
    
    config = get_config()
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    # Read current code files
    current_code = {}
    for file_path in current_files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                current_code[Path(file_path).name] = f.read()
    
    improvement_prompt = f"""
You are an expert ML engineer helping improve code. The user wants to improve their ML project.

**Original Task**: {original_prompt}

**Dataset Info**: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
Columns: {list(dataset_info['columns'].keys())}

**User's Improvement Request**: {improvement_request}

**Current Code Files**:
"""
    
    for filename, code in current_code.items():
        improvement_prompt += f"\n```python\n# {filename}\n{code}\n```\n"
    
    improvement_prompt += """
**Your Task**:
1. Analyze the user's improvement request
2. Provide improved versions of the relevant code files
3. Maintain the existing functionality while adding the requested improvements
4. Focus on code quality, performance, and best practices

**Response Format**:
Provide the improved code files in markdown code blocks labeled with the filename.

Example:
```python
# model.py
[improved model code]
```

```python
# train.py
[improved training code]
```
"""
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": improvement_prompt}]
    )
    
    content = response.content[0].text
    
    # Extract improved code blocks
    import re
    code_blocks = {}
    pattern = r'```python\n# (\w+\.py)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for filename, code in matches:
        code_blocks[filename] = code.strip()
    
    return code_blocks

def apply_code_improvements(project_info: dict, improved_code: dict) -> dict:
    """Apply the improved code to the project."""
    for filename, code in improved_code.items():
        file_path = project_info['dir'] / filename
        if file_path.exists():
            with open(file_path, 'w') as f:
                f.write(code)
            typer.echo(f"✅ Updated {filename}")
    
    return project_info

def generate_training_script(project_info: dict) -> dict:
    """Generate training script with Modal integration."""
    typer.echo(f"\n🎯 Generating training script with Modal integration...")
    
    # Generate training script based on user preferences
    training_script = generate_modal_training_script(project_info)
    
    # Save training script
    train_file_path = project_info['dir'] / "train_modal.py"
    with open(train_file_path, 'w') as f:
        f.write(training_script)

    typer.echo(f"✅ Training script generated: {train_file_path}")
    
    # Update project info
    project_info['training_script'] = str(train_file_path)
    
    return project_info

def generate_modal_training_script(project_info: dict) -> str:
    """Generate Modal training script with user preferences."""
    from exponent.core.config import get_config
    import anthropic
    
    config = get_config()
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    # Read existing model code
    model_file = project_info['dir'] / "model.py"
    model_code = ""
    if model_file.exists():
        with open(model_file, 'r') as f:
            model_code = f.read()
    
    # Get dataset filename from project directory
    dataset_files = list(project_info['dir'].glob("*.csv"))
    dataset_filename = dataset_files[0].name if dataset_files else "dataset.csv"
    
    # Get dataset column information
    dataset_info = project_info.get('dataset_info', {})
    columns = dataset_info.get('columns', [])
    target_column = dataset_info.get('target_column', 'target')
    
    training_prompt = f"""
Generate a complete Modal training script for the following ML project:

**Project Details**:
- Project: {project_info['prompt']}
- Dataset: {dataset_filename} ({dataset_info.get('shape', [0, 0])[0]} rows, {dataset_info.get('shape', [0, 0])[1]} columns)
- Features: {', '.join(columns) if columns else 'auto-detected'}
- Target: {target_column}
- GPU: {'Yes' if project_info['use_gpu'] else 'No'}
- Hyperparameters: {project_info['hyperparameters'] or 'Default'}

**Model Code**:
```python
{model_code}
```

**Critical Requirements**:
1. Use Modal for cloud training with proper error handling
2. Load dataset from '{dataset_filename}' (exact filename)
3. Include real-time logging and progress tracking
4. Handle GPU if requested: {project_info['use_gpu']}
5. Apply custom hyperparameters: {project_info['hyperparameters']}
6. Save model artifacts (joblib format)
7. Generate training metrics, confusion matrix, and feature importance plots
8. Handle errors gracefully with retry logic
9. Use proper Python syntax (no markdown formatting)

**Generate a production-ready Modal training script** that:
- Sets up Modal app and image with proper dependencies
- Loads the dataset from the correct filename
- Preprocesses data (scaling, encoding if needed)
- Trains the model with the specified configuration
- Logs progress in real-time
- Saves the trained model and scaler
- Generates comprehensive training reports and visualizations
- Handles all edge cases and errors

**Important**: 
- Use the exact dataset filename: '{dataset_filename}'
- Ensure all Python code is properly formatted (no markdown)
- Include proper imports and error handling
- Make the script executable and production-ready
"""
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": training_prompt}]
    )
    
    generated_script = response.content[0].text
    
    # Clean up the generated script
    cleaned_script = clean_generated_script(generated_script, dataset_filename)
    
    return cleaned_script

def clean_generated_script(script_content: str, dataset_filename: str) -> str:
    """Clean and validate the generated training script."""
    # Remove markdown formatting if present
    if script_content.startswith('```python'):
        script_content = script_content.replace('```python', '').replace('```', '')
    
    if script_content.startswith('```'):
        script_content = script_content.replace('```', '')
    
    # Ensure the script uses the correct dataset filename
    script_content = script_content.replace('plant_disease_data.csv', dataset_filename)
    script_content = script_content.replace('dataset.csv', dataset_filename)
    
    # Add common imports if missing
    required_imports = [
        'import pandas as pd',
        'import numpy as np',
        'import matplotlib.pyplot as plt',
        'import seaborn as sns',
        'from sklearn.model_selection import train_test_split',
        'from sklearn.preprocessing import StandardScaler',
        'from sklearn.metrics import classification_report, confusion_matrix'
    ]
    
    for import_stmt in required_imports:
        if import_stmt not in script_content:
            script_content = import_stmt + '\n' + script_content
    
    # Ensure proper matplotlib backend for non-interactive environments
    if 'plt.show()' in script_content:
        script_content = script_content.replace(
            'import matplotlib.pyplot as plt',
            'import matplotlib.pyplot as plt\nplt.switch_backend("Agg")'
        )
    
    return script_content.strip()

def run_modal_training(project_info: dict) -> dict:
    """Run training job in Modal with real-time logs."""
    typer.echo(f"\n🚀 Starting Modal training job...")
    
    try:
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_info['dir'])
        
        # Initialize error agent for training
        error_agent = ErrorAgent()
        
        # Run the training script
        training_script_path = Path("train_modal.py")
        if not training_script_path.exists():
            typer.echo("❌ Training script not found. Generating one...")
            project_info = generate_training_script(project_info)
            training_script_path = Path("train_modal.py")
        
        typer.echo("🔄 Running training with error handling...")
        
        # Execute training with error handling
        success, stdout, stderr = error_agent.execute_with_retry(
            training_script_path,
            f"Train {project_info['prompt']}",
            project_info['dataset_info']
        )
        
        if success:
            typer.echo("✅ Training completed successfully!")
            if stdout:
                typer.echo("📋 Training output:")
                typer.echo(stdout)
            
            # Check for model artifacts
            model_files = list(Path(".").glob("*.joblib")) + list(Path(".").glob("*.pkl")) + list(Path(".").glob("*.h5"))
            if model_files:
                typer.echo("📦 Model artifacts saved:")
                for model_file in model_files:
                    typer.echo(f"  - {model_file.name}")
            
            project_info['training_completed'] = True
            project_info['training_output'] = stdout
            
        else:
            typer.echo("❌ Training failed after all retry attempts.")
            if stderr:
                typer.echo(f"Final error: {stderr}")
            
            # Show error summary
            error_summary = error_agent.get_error_summary()
            typer.echo("\n🔍 Training Error Summary:")
            typer.echo(error_summary)
            
            project_info['training_completed'] = False
            project_info['training_error'] = stderr
        
        # Return to original directory
        os.chdir(original_dir)
        
        return project_info
        
    except Exception as e:
        typer.echo(f"❌ Error during training: {e}")
        project_info['training_completed'] = False
        project_info['training_error'] = str(e)
        return project_info

def handle_deployment(project_info: dict) -> dict:
    """Handle deployment to GitHub or AWS based on user preference."""
    if not project_info.get('deploy_after', False):
        typer.echo("\n🌐 Skipping deployment (user chose not to deploy)")
        return project_info
    
    typer.echo(f"\n🌐 Deployment Options")
    typer.echo(f"Choose where to deploy your trained model:")
    
    deployment_choice = typer.prompt(
        "🎯 Deployment target (github/aws/both/none)",
        default="github"
    ).lower()
    
    if deployment_choice in ['none', 'skip']:
        typer.echo("✅ Skipping deployment")
        return project_info
    
    project_info['deployment_target'] = deployment_choice
    
    if deployment_choice in ['github', 'both']:
        project_info = deploy_to_github(project_info)
    
    if deployment_choice in ['aws', 'both']:
        project_info = deploy_to_aws(project_info)
    
    return project_info

def deploy_to_github(project_info: dict) -> dict:
    """Deploy project to GitHub."""
    typer.echo(f"\n🌐 Deploying to GitHub...")
    
    try:
        from exponent.core.github_utils import deploy_to_github as github_deploy
        
        # Get repository name
        repo_name = typer.prompt(
            "📝 GitHub repository name",
            default=f"ml-{project_info['name']}"
        )
        
        # Deploy to GitHub
        result = github_deploy(
            project_info['project_id'],
            project_info['dir'],
            repo_name
        )
        
        if result["deployment_successful"]:
            typer.echo("✅ GitHub deployment successful!")
            typer.echo(f"🌐 Repository URL: {result['github_url']}")
            project_info['github_url'] = result['github_url']
            project_info['github_deployment_successful'] = True
        else:
            typer.echo(f"❌ GitHub deployment failed: {result.get('error', 'Unknown error')}")
            project_info['github_deployment_successful'] = False
            
    except Exception as e:
        typer.echo(f"❌ Error deploying to GitHub: {e}")
        project_info['github_deployment_successful'] = False
        project_info['github_error'] = str(e)
    
    return project_info

def deploy_to_aws(project_info: dict) -> dict:
    """Deploy project to AWS."""
    typer.echo(f"\n☁️ Deploying to AWS...")
    
    try:
        # Check if model artifacts exist
        model_files = list(project_info['dir'].glob("*.joblib")) + list(project_info['dir'].glob("*.pkl"))
        
        if not model_files:
            typer.echo("❌ No model artifacts found for AWS deployment")
            typer.echo("💡 Make sure training completed successfully first")
            project_info['aws_deployment_successful'] = False
            return project_info
        
        # Upload model to S3
        from exponent.core.s3_utils import upload_model_to_s3
        
        model_file = model_files[0]  # Use first model file
        s3_url = upload_model_to_s3(str(model_file), project_info['project_id'])
        
        typer.echo("✅ Model uploaded to AWS S3!")
        typer.echo(f"☁️ S3 URL: {s3_url}")
        
        project_info['aws_s3_url'] = s3_url
        project_info['aws_deployment_successful'] = True
        
        # TODO: Add AWS Lambda deployment for model serving
        typer.echo("💡 AWS Lambda deployment coming soon...")
        
    except Exception as e:
        typer.echo(f"❌ Error deploying to AWS: {e}")
        project_info['aws_deployment_successful'] = False
        project_info['aws_error'] = str(e)
    
    return project_info

def run_interactive_wizard():
    """Run the interactive ML model building wizard with comprehensive error handling."""
    
    # Initialize error agent for the entire workflow
    error_agent = ErrorAgent()
    workflow_errors = []
    
    try:
        # Welcome message
        welcome_message()
        
        # Get user input
        user_input = get_user_input()
        
        if not user_input:
            typer.echo("❌ No input provided. Exiting.")
            raise typer.Exit(1)
        
        prompt = user_input['prompt']
        dataset_path = user_input['dataset_path']
        use_gpu = user_input['has_gpu']
        hyperparameters = user_input['hyperparameters']
        deploy_after = user_input['deploy_after']
        
        # Validate dataset exists
        if not Path(dataset_path).exists():
            typer.echo(f"❌ Dataset not found: {dataset_path}")
            raise typer.Exit(1)
        
        # Create project structure
        project_name = sanitize_project_name(prompt)
        project_dir = create_project_structure(project_name)
        
        typer.echo(f"\n🎯 Project: {prompt}")
        typer.echo(f"📊 Dataset: {dataset_path}")
        typer.echo(f"🖥️ GPU: {'Yes' if use_gpu else 'No'}")
        typer.echo(f"⚙️ Hyperparameters: {hyperparameters or 'Default'}")
        typer.echo(f"🌐 Deploy after training: {'Yes' if deploy_after else 'No'}")
        
        # Store project info for later use
        project_info = {
            'name': project_name,
            'dir': project_dir,
            'prompt': prompt,
            'dataset_path': dataset_path,
            'use_gpu': use_gpu,
            'hyperparameters': hyperparameters,
            'deploy_after': deploy_after,
            'workflow_errors': workflow_errors
        }
        
        # Step 1: Dataset Analysis & Code Generation
        typer.echo(f"\n🔄 Step 1/5: Dataset Analysis & Code Generation")
        try:
            project_info = analyze_dataset_and_generate_code(project_info)
            typer.echo("✅ Step 1 completed successfully!")
        except Exception as e:
            error_msg = f"Step 1 failed: {str(e)}"
            workflow_errors.append(error_msg)
            typer.echo(f"❌ {error_msg}")
            
            # Try to recover with error agent
            recovery_success = handle_workflow_error(error_agent, project_info, error_msg, "dataset_analysis")
            if not recovery_success:
                show_workflow_failure_summary(workflow_errors)
                raise typer.Exit(1)
        
        # Step 2: Interactive Code Improvement
        typer.echo(f"\n🔄 Step 2/5: Interactive Code Improvement")
        try:
            project_info = interactive_code_improvement(project_info)
            typer.echo("✅ Step 2 completed successfully!")
        except Exception as e:
            error_msg = f"Step 2 failed: {str(e)}"
            workflow_errors.append(error_msg)
            typer.echo(f"❌ {error_msg}")
            
            recovery_success = handle_workflow_error(error_agent, project_info, error_msg, "code_improvement")
            if not recovery_success:
                show_workflow_failure_summary(workflow_errors)
                raise typer.Exit(1)
        
        # Step 3: Training Script Generation
        typer.echo(f"\n🔄 Step 3/5: Training Script Generation")
        try:
            project_info = generate_training_script(project_info)
            typer.echo("✅ Step 3 completed successfully!")
        except Exception as e:
            error_msg = f"Step 3 failed: {str(e)}"
            workflow_errors.append(error_msg)
            typer.echo(f"❌ {error_msg}")
            
            recovery_success = handle_workflow_error(error_agent, project_info, error_msg, "training_script")
            if not recovery_success:
                show_workflow_failure_summary(workflow_errors)
                raise typer.Exit(1)
        
        # Step 4: Modal Training
        typer.echo(f"\n🔄 Step 4/5: Modal Training")
        if typer.confirm("🚀 Start training now?", default=True):
            try:
                project_info = run_modal_training(project_info)
                if project_info.get('training_completed'):
                    typer.echo("✅ Step 4 completed successfully!")
                else:
                    error_msg = "Training failed or was not completed"
                    workflow_errors.append(error_msg)
                    typer.echo(f"⚠️ {error_msg}")
            except Exception as e:
                error_msg = f"Step 4 failed: {str(e)}"
                workflow_errors.append(error_msg)
                typer.echo(f"❌ {error_msg}")
                
                recovery_success = handle_workflow_error(error_agent, project_info, error_msg, "training")
                if not recovery_success:
                    show_workflow_failure_summary(workflow_errors)
                    raise typer.Exit(1)
        else:
            typer.echo("💡 You can run training later with: python train_modal.py")
        
        # Step 5: Deployment
        typer.echo(f"\n🔄 Step 5/5: Deployment")
        try:
            project_info = handle_deployment(project_info)
            typer.echo("✅ Step 5 completed successfully!")
        except Exception as e:
            error_msg = f"Step 5 failed: {str(e)}"
            workflow_errors.append(error_msg)
            typer.echo(f"❌ {error_msg}")
            
            recovery_success = handle_workflow_error(error_agent, project_info, error_msg, "deployment")
            if not recovery_success:
                show_workflow_failure_summary(workflow_errors)
                raise typer.Exit(1)
        
        # Check if we have too many errors
        if len(workflow_errors) >= 3:
            typer.echo(f"\n⚠️ Too many errors encountered ({len(workflow_errors)}). Stopping workflow.")
            show_workflow_failure_summary(workflow_errors)
            raise typer.Exit(1)
        
        return project_info
        
    except Exception as e:
        workflow_errors.append(f"Workflow failed: {str(e)}")
        show_workflow_failure_summary(workflow_errors)
        raise typer.Exit(1)

def handle_workflow_error(error_agent: ErrorAgent, project_info: dict, error_msg: str, step_name: str) -> bool:
    """Handle workflow errors with intelligent recovery."""
    typer.echo(f"\n🔧 Attempting to recover from error in {step_name}...")
    
    try:
        # Analyze the error with the error agent
        recovery_prompt = f"""
You are an expert ML workflow recovery agent. A step in the ML pipeline failed and we need to recover.

**Failed Step**: {step_name}
**Error**: {error_msg}
**Project**: {project_info['prompt']}
**Dataset**: {project_info['dataset_info']['shape'][0]} rows, {project_info['dataset_info']['shape'][1]} columns

**Your Task**:
1. Analyze what went wrong
2. Provide specific recovery steps
3. Suggest alternative approaches if needed
4. Give clear instructions to the user

**Response Format**:
```
# Error Analysis
[Brief analysis of what went wrong]

# Recovery Steps
[Step-by-step recovery instructions]

# Alternative Approaches
[If recovery isn't possible, suggest alternatives]
```
"""
        
        from exponent.core.config import get_config
        import anthropic
        
        config = get_config()
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": recovery_prompt}]
        )
        
        recovery_analysis = response.content[0].text
        
        typer.echo("\n🔍 Error Analysis:")
        typer.echo("=" * 40)
        typer.echo(recovery_analysis)
        typer.echo("=" * 40)
        
        # Ask user if they want to continue
        continue_workflow = typer.confirm(
            f"🤔 Do you want to continue with the workflow? (The error has been analyzed above)",
            default=True
        )
        
        if continue_workflow:
            typer.echo("✅ Continuing workflow...")
            return True
        else:
            typer.echo("❌ User chose to stop workflow.")
            return False
            
    except Exception as recovery_error:
        typer.echo(f"❌ Error during recovery analysis: {recovery_error}")
        typer.echo("💡 Continuing workflow anyway...")
        return True

def show_workflow_failure_summary(workflow_errors: list):
    """Show comprehensive failure summary with guidance."""
    typer.echo(f"\n❌ Workflow Failed!")
    typer.echo("=" * 50)
    typer.echo(f"📊 Total Errors: {len(workflow_errors)}")
    
    typer.echo(f"\n🔍 Error Summary:")
    for i, error in enumerate(workflow_errors, 1):
        typer.echo(f"{i}. {error}")
    
    typer.echo(f"\n💡 How to Fix:")
    typer.echo(f"1. Check your dataset path and format")
    typer.echo(f"2. Ensure you have proper API keys configured")
    typer.echo(f"3. Verify your internet connection")
    typer.echo(f"4. Try running individual commands:")
    typer.echo(f"   • exponent init quick 'your task' --dataset your_data.csv")
    typer.echo(f"   • exponent analyze your_data.csv --prompt 'your analysis'")
    typer.echo(f"   • exponent train")
    typer.echo(f"   • exponent deploy")
    
    typer.echo(f"\n🆘 Need Help?")
    typer.echo(f"• Check the error messages above")
    typer.echo(f"• Review the generated files in your project directory")
    typer.echo(f"• Try running the workflow step by step")
    typer.echo(f"• Contact support if issues persist")
    
    typer.echo("=" * 50)

@app.command()
def wizard():
    """Interactive wizard for building ML models end-to-end."""
    try:
        project_info = run_interactive_wizard()
        
        # Show comprehensive completion summary
        typer.echo(f"\n🎉 Project Complete!")
        typer.echo(f"=" * 50)
        typer.echo(f"📁 Project: {project_info['name']}")
        typer.echo(f"🎯 Model: {project_info['prompt']}")
        typer.echo(f"📊 Dataset: {project_info['dataset_info']['shape'][0]} rows, {project_info['dataset_info']['shape'][1]} columns")
        typer.echo(f"📄 Generated files: {len(project_info['created_files'])} files")
        
        # Training status
        if project_info.get('training_completed'):
            typer.echo(f"✅ Training: Completed successfully")
            model_files = list(project_info['dir'].glob("*.joblib")) + list(project_info['dir'].glob("*.pkl"))
            if model_files:
                typer.echo(f"📦 Model artifacts: {len(model_files)} files")
        else:
            typer.echo(f"⚠️ Training: Not completed or failed")
        
        # Deployment status
        if project_info.get('github_deployment_successful'):
            typer.echo(f"🌐 GitHub: {project_info.get('github_url', 'Deployed')}")
        if project_info.get('aws_deployment_successful'):
            typer.echo(f"☁️ AWS: {project_info.get('aws_s3_url', 'Deployed')}")
        
        typer.echo(f"=" * 50)
        
        # Next steps
        typer.echo(f"\n🚀 Next steps:")
        typer.echo(f"1. ✅ Dataset analysis and code generation")
        typer.echo(f"2. ✅ Interactive code improvement")
        typer.echo(f"3. ✅ Training script generation")
        typer.echo(f"4. ✅ Modal training with real-time logs")
        typer.echo(f"5. ✅ Deployment to GitHub/AWS")
        
        typer.echo(f"\n💡 You can now:")
        typer.echo(f"   • Review the code in {project_info['dir']}")
        typer.echo(f"   • Run 'python train_modal.py' to retrain")
        typer.echo(f"   • Use the deployed model in your applications")
        typer.echo(f"   • Share the GitHub repository with your team")
        
    except Exception as e:
        typer.echo(f"❌ Error in interactive wizard: {e}")
        raise typer.Exit(1) 