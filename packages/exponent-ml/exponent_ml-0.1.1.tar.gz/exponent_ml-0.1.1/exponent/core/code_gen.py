import anthropic
import uuid
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from exponent.core.config import get_config
from exponent.core.s3_utils import analyze_dataset, create_dataset_summary

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

def save_code_files(code_blocks: Dict[str, str], output_path: Path) -> List[str]:
    """Save code blocks to files and return list of created files."""
    created_files = []
    
    # Map language labels to filenames
    file_mapping = {
        'python': 'model.py',
        'model': 'model.py',
        'train': 'train.py',
        'predict': 'predict.py',
        'requirements': 'requirements.txt',
        'readme': 'README.md',
        'md': 'README.md'
    }
    
    for lang, code in code_blocks.items():
        # Determine filename
        if lang in file_mapping:
            filename = file_mapping[lang]
        elif lang.startswith('python'):
            filename = 'model.py'
        elif lang.startswith('train'):
            filename = 'train.py'
        elif lang.startswith('predict'):
            filename = 'predict.py'
        else:
            # Default to .py extension
            filename = f"{lang}.py"
        
        # Save file
        file_path = output_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        created_files.append(str(file_path))
    
    return created_files

def generate_code_from_prompt(task_description: str, dataset_path: str = None) -> Tuple[str, List[str]]:
    """Generate ML code from prompt and optional dataset."""
    config = get_config()
    project_id = str(uuid.uuid4())
    out_path = Path.home() / ".exponent" / project_id
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Analyze dataset if provided
    dataset_summary = ""
    if dataset_path:
        try:
            dataset_info = analyze_dataset(dataset_path)
            dataset_summary = create_local_dataset_summary(dataset_info, dataset_path)
        except Exception as e:
            print(f"Warning: Could not analyze dataset: {e}")
    
    # Create comprehensive prompt
    full_prompt = f"""
You are an expert ML engineer. Generate production-ready Python code for the following machine learning task:

**Task**: {task_description}

{dataset_summary}

**Requirements:**
1. Generate clean, well-documented Python code
2. Include proper error handling and logging
3. Use modern ML libraries (scikit-learn, pandas, numpy)
4. Include data preprocessing and feature engineering
5. Add model evaluation metrics
6. Make code modular and reusable
7. Use local file paths for data loading (no cloud dependencies)

**Generate these files:**
1. `model.py` - Model definition and training pipeline
2. `train.py` - Training script with data loading and model training
3. `predict.py` - Prediction script for making predictions
4. `requirements.txt` - Python dependencies
5. `README.md` - Project documentation

Respond with markdown code blocks labeled with the filename (e.g., ```python for model.py, ```train for train.py, etc.).
"""

    # Call Claude API
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    content = response.content[0].text
    
    # Extract and save code blocks
    code_blocks = extract_code_blocks(content)
    created_files = save_code_files(code_blocks, out_path)
    
    # Copy dataset to project directory if provided
    if dataset_path:
        try:
            import shutil
            dataset_name = Path(dataset_path).name
            shutil.copy2(dataset_path, out_path / dataset_name)
            created_files.append(str(out_path / dataset_name))
        except Exception as e:
            print(f"Warning: Could not copy dataset to project directory: {e}")
    
    return project_id, created_files

def generate_code_with_dataset_analysis(task_description: str, dataset_path: str) -> Tuple[str, List[str], Dict[str, Any]]:
    """Generate code with full dataset analysis for local usage."""
    config = get_config()
    project_id = str(uuid.uuid4())
    out_path = Path.home() / ".exponent" / project_id
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Analyze dataset
    dataset_info = analyze_dataset(dataset_path)
    dataset_summary = create_local_dataset_summary(dataset_info, dataset_path)
    
    # Create enhanced prompt with dataset insights
    full_prompt = f"""
You are an expert ML engineer. Generate production-ready Python code for the following machine learning task:

**Task**: {task_description}

{dataset_summary}

**Dataset Analysis Insights:**
- Total rows: {dataset_info['shape'][0]}
- Total columns: {dataset_info['shape'][1]}
- File size: {dataset_info['file_size']} bytes
- Local file path: {dataset_path}

**Column Details:**
"""
    
    for col_name, col_info in dataset_info['columns'].items():
        full_prompt += f"- {col_name}: {col_info['type']} (unique: {col_info['unique_count']}, nulls: {col_info['null_count']})\n"
        if col_info['sample_values']:
            full_prompt += f"  Sample values: {col_info['sample_values']}\n"
    
    full_prompt += """
**Requirements:**
1. Generate clean, well-documented Python code
2. Include proper error handling and logging
3. Use modern ML libraries (scikit-learn, pandas, numpy)
4. Include data preprocessing and feature engineering
5. Add model evaluation metrics
6. Make code modular and reusable
7. Handle the specific data types and null values in the dataset
8. Use local file paths for data loading (no cloud dependencies)
9. Include data validation and error handling for missing files

**Generate these files:**
1. `model.py` - Model definition and training pipeline
2. `train.py` - Training script with data loading and model training
3. `predict.py` - Prediction script for making predictions
4. `requirements.txt` - Python dependencies
5. `README.md` - Project documentation

Respond with markdown code blocks labeled with the filename (e.g., ```python for model.py, ```train for train.py, etc.).
"""

    # Call Claude API
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    content = response.content[0].text
    
    # Extract and save code blocks
    code_blocks = extract_code_blocks(content)
    created_files = save_code_files(code_blocks, out_path)
    
    # Copy dataset to project directory
    try:
        import shutil
        dataset_name = Path(dataset_path).name
        shutil.copy2(dataset_path, out_path / dataset_name)
        created_files.append(str(out_path / dataset_name))
    except Exception as e:
        print(f"Warning: Could not copy dataset to project directory: {e}")
    
    return project_id, created_files, dataset_info

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
