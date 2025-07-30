import typer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import uuid
import os
import anthropic
import re
import subprocess
import sys
from exponent.core.s3_utils import analyze_dataset
from exponent.core.config import get_config
from exponent.core.error_agent import ErrorAgent
from typing import Dict

app = typer.Typer()

def extract_code_blocks(content: str) -> Dict[str, str]:
    """Extract code blocks from markdown content."""
    code_blocks = {}
    
    # Pattern to match markdown code blocks with language labels
    pattern = r'```(\w+)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for lang, code in matches:
        # Clean up the code
        code = code.strip()
        if code:
            code_blocks[lang] = code
    
    # Also look for unlabeled code blocks
    unlabeled_pattern = r'```\n(.*?)```'
    unlabeled_matches = re.findall(unlabeled_pattern, content, re.DOTALL)
    
    for i, code in enumerate(unlabeled_matches):
        code = code.strip()
        if code:
            # Try to infer file type from content
            if 'import pandas' in code or 'pd.read_csv' in code:
                code_blocks[f'python_{i}'] = code
            elif 'def train' in code or 'model.fit' in code:
                code_blocks[f'train_{i}'] = code
            else:
                code_blocks[f'code_{i}'] = code
    
    return code_blocks

def generate_ai_analysis(dataset_path: str, prompt: str, dataset_info: dict) -> tuple[str, str]:
    """Generate AI-powered analysis and visualization script."""
    
    config = get_config()
    
    # Load a sample of the dataset for the AI
    try:
        df_sample = pd.read_csv(dataset_path, nrows=100)
        sample_data = df_sample.to_string(max_rows=20, max_cols=10)
    except Exception as e:
        sample_data = f"Error loading sample: {e}"
    
    # Create comprehensive prompt for analysis
    analysis_prompt = f"""
You are an expert data analyst and visualization specialist. Analyze the following dataset and create comprehensive visualizations based on the user's request.

**User Request**: {prompt}

**Dataset Information:**
- File: {Path(dataset_path).name}
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- File size: {dataset_info['file_size']} bytes

**Column Details:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        analysis_prompt += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            analysis_prompt += f"  Sample values: {col_info['sample_values']}\n"
    
    analysis_prompt += f"""
**Sample Data (first 100 rows):**
{sample_data}

**Your Task:**
1. **Provide a comprehensive analysis summary** of the dataset based on the user's request
2. **Generate a complete Python script** that creates relevant visualizations and analysis
3. **Focus on the user's specific request**: {prompt}

**Requirements for the Python script:**
- Use pandas, matplotlib, and seaborn for visualizations
- Load the dataset using: `df = pd.read_csv('{Path(dataset_path).name}')`
- Create multiple relevant visualizations based on the user's request
- Include proper titles, labels, and legends
- Save the final figure as 'dataset_analysis.png'
- Handle any potential errors gracefully
- Include print statements to show analysis results
- Make the visualizations publication-ready with good styling
- Use `plt.style.use('default')` or `sns.set_style('whitegrid')` for styling (NOT `plt.style.use('seaborn')`)
- Set figure size with `plt.figure(figsize=(width, height))` before creating plots

**Response Format:**
1. Start with a detailed analysis summary (text)
2. Then provide the Python script in a code block labeled 'python'

Example response format:
```
# Analysis Summary
[Your detailed analysis here...]

```python
# Python script for analysis and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_csv('{Path(dataset_path).name}')

# Your analysis and visualization code here...
```
"""
    
    # Call Claude API
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": analysis_prompt}]
    )
    
    content = response.content[0].text
    
    # Extract analysis summary and code
    # Split content into summary and code
    parts = content.split('```python')
    if len(parts) >= 2:
        summary = parts[0].strip()
        code = parts[1].split('```')[0].strip()
    else:
        # Fallback: try to extract code blocks
        code_blocks = extract_code_blocks(content)
        summary = content
        code = code_blocks.get('python', '')
    
    return summary, code

def sanitize_filename(prompt: str) -> str:
    """Convert prompt to a valid filename."""
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', prompt.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    # Limit length to avoid overly long filenames
    sanitized = sanitized[:50]
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it's not empty
    if not sanitized:
        sanitized = "analysis"
    return sanitized

def run_analysis(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    prompt: str = typer.Option(None, "--prompt", "-p", help="Analysis prompt for AI"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory for analysis")
):
    """Analyze dataset with AI-powered analysis and visualization."""
    
    # Validate file exists
    if not Path(dataset_path).exists():
        typer.echo(f"❌ Dataset not found: {dataset_path}")
        raise typer.Exit(1)
    
    # Get user prompt if not provided
    if not prompt:
        prompt = typer.prompt("💬 What would you like to analyze? (e.g., 'Show correlations between numerical columns', 'Create visualizations for customer churn patterns')")
    
    # Generate project name from prompt
    project_name = sanitize_filename(prompt)
    
    # Set output directory
    if not output_dir:
        output_dir = f"{project_name}_{str(uuid.uuid4())[:8]}"
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    try:
        # Analyze dataset structure
        typer.echo("📊 Analyzing dataset structure...")
        dataset_info = analyze_dataset(dataset_path)
        
        # Display basic info
        typer.echo(f"✅ Dataset loaded successfully!")
        typer.echo(f"📈 Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns")
        typer.echo(f"📁 File size: {dataset_info['file_size']} bytes")
        
        columns = list(dataset_info['columns'].keys())
        typer.echo(f"📊 Columns: {columns}")
        
        typer.echo(f"🤖 Generating AI-powered analysis based on: {prompt}")
        
        # Generate AI analysis and script
        summary, analysis_script = generate_ai_analysis(dataset_path, prompt, dataset_info)
        
        # Display AI analysis summary
        typer.echo("\n📋 AI Analysis Summary:")
        typer.echo("=" * 50)
        typer.echo(summary)
        typer.echo("=" * 50)
        
        # Save analysis script
        script_path = Path(output_dir) / "analysis_script.py"
        with open(script_path, 'w') as f:
            f.write(analysis_script)
        
        # Copy dataset to output directory
        import shutil
        dataset_copy_path = Path(output_dir) / Path(dataset_path).name
        shutil.copy2(dataset_path, dataset_copy_path)
        
        # Create requirements file
        requirements = """pandas
matplotlib
seaborn
numpy"""
        
        req_path = Path(output_dir) / "requirements.txt"
        with open(req_path, 'w') as f:
            f.write(requirements)
        
        # Create README
        readme_content = f"""# AI-Powered Dataset Analysis

## Analysis ID: {output_dir}

### Dataset: {Path(dataset_path).name}
- Shape: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
- File size: {dataset_info['file_size']} bytes

### Analysis Prompt
{prompt}

### AI Analysis Summary
{summary}

### Files Generated
- `analysis_script.py` - AI-generated Python script for analysis
- `{Path(dataset_path).name}` - Dataset copy
- `requirements.txt` - Python dependencies
- `dataset_analysis.png` - Generated visualizations (after running script)

### How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run analysis: `python analysis_script.py`
3. Check `dataset_analysis.png` for visualizations

### Columns in Dataset
"""
        for col_name, col_info in dataset_info['columns'].items():
            readme_content += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        
        readme_path = Path(output_dir) / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        # Display results
        typer.echo(f"\n✅ AI analysis setup complete!")
        typer.echo(f"📁 Output directory: {output_dir}")
        typer.echo(f"📄 Generated files:")
        typer.echo(f"  - analysis_script.py (AI-generated)")
        typer.echo(f"  - {Path(dataset_path).name}")
        typer.echo(f"  - requirements.txt")
        typer.echo(f"  - README.md")
        
        typer.echo(f"\n🚀 Next steps:")
        typer.echo(f"1. cd {output_dir}")
        typer.echo(f"2. pip install -r requirements.txt")
        typer.echo(f"3. python analysis_script.py")
        typer.echo(f"4. Check dataset_analysis.png for visualizations")
        
        # Ask if user wants to run the analysis now
        run_now = typer.confirm("🤔 Would you like to run the AI-generated analysis now?")
        if run_now:
            typer.echo("🚀 Running AI-generated analysis with intelligent error handling...")
            
            try:
                # Change to output directory
                os.chdir(output_dir)
                
                # Initialize error agent
                error_agent = ErrorAgent()
                
                # Execute with automatic error fixing and retry
                success, stdout, stderr = error_agent.execute_with_retry(
                    Path("analysis_script.py"), 
                    prompt, 
                    dataset_info
                )
                
                if success:
                    typer.echo("✅ AI analysis completed successfully!")
                    typer.echo("📊 Check dataset_analysis.png for visualizations")
                    if stdout:
                        typer.echo("📋 Analysis output:")
                        typer.echo(stdout)
                    
                    # Try to open the image
                    image_path = Path("dataset_analysis.png")
                    if image_path.exists():
                        typer.echo("🖼️ Opening dataset_analysis.png...")
                        if sys.platform.startswith("win"):
                            os.startfile(str(image_path))
                        elif sys.platform == "darwin":
                            subprocess.run(["open", str(image_path)])
                        else:
                            subprocess.run(["xdg-open", str(image_path)])
                    else:
                        typer.echo("⚠️ No image found to display.")
                else:
                    typer.echo("❌ Analysis failed after all retry attempts.")
                    if stderr:
                        typer.echo(f"Final error: {stderr}")
                    if stdout:
                        typer.echo("📋 Analysis output:")
                        typer.echo(stdout)
                    
                    # Show error summary
                    error_summary = error_agent.get_error_summary()
                    typer.echo("\n🔍 Error Analysis Summary:")
                    typer.echo(error_summary)
                    
                    typer.echo("💡 You can still run the script manually in the output directory")
                    
            except Exception as e:
                typer.echo(f"❌ Error running analysis: {e}")
                typer.echo("💡 You can still run the script manually in the output directory")
        
    except Exception as e:
        typer.echo(f"❌ Error during analysis: {e}")
        raise typer.Exit(1)

@app.command()
def analyze(
    dataset_path: str = typer.Argument(..., help="Path to dataset file"),
    prompt: str = typer.Option(None, "--prompt", "-p", help="Analysis prompt for AI"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory for analysis")
):
    """Analyze dataset with AI-powered analysis and visualization."""
    run_analysis(dataset_path, prompt, output_dir) 