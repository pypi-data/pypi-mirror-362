import anthropic
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from exponent.core.config import get_config

class ErrorAgent:
    """Agent that monitors, analyzes, and fixes code execution errors."""
    
    def __init__(self):
        self.config = get_config()
        self.client = anthropic.Anthropic(api_key=self.config.ANTHROPIC_API_KEY)
        self.max_attempts = 3
        self.error_history = []
    
    def analyze_error(self, error_output: str, script_content: str, original_prompt: str, dataset_info: dict) -> Dict[str, str]:
        """Analyze error and generate fix instructions."""
        
        analysis_prompt = f"""
You are an expert Python debugging agent. Analyze the following error and provide a fix.

**Original Task**: {original_prompt}

**Dataset Info**: {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
Columns: {list(dataset_info['columns'].keys())}

**Error Output**:
{error_output}

**Current Script**:
```python
{script_content}
```

**Your Task**:
1. Analyze what caused the error
2. Identify the specific issue (import, syntax, logic, etc.)
3. Provide a corrected version of the script
4. Focus on the most common issues:
   - Missing imports
   - Incorrect matplotlib/seaborn usage
   - Syntax errors
   - Variable scope issues
   - File path issues

**Response Format**:
```
# Error Analysis
[Brief analysis of what went wrong]

# Fix Description
[What needs to be changed]

```python
# Fixed Script
[Complete corrected script]
```
"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        content = response.content[0].text
        
        # Extract analysis and fixed code
        parts = content.split('```python')
        if len(parts) >= 2:
            analysis = parts[0].strip()
            fixed_code = parts[1].split('```')[0].strip()
        else:
            analysis = content
            fixed_code = ""
        
        return {
            "analysis": analysis,
            "fixed_code": fixed_code,
            "error_type": self._classify_error(error_output)
        }
    
    def _classify_error(self, error_output: str) -> str:
        """Classify the type of error for better handling."""
        error_lower = error_output.lower()
        
        if "import" in error_lower and ("no module" in error_lower or "cannot import" in error_lower):
            return "import_error"
        elif "syntax" in error_lower:
            return "syntax_error"
        elif "matplotlib" in error_lower or "seaborn" in error_lower:
            return "plotting_error"
        elif "attribute" in error_lower and "has no attribute" in error_lower:
            return "attribute_error"
        elif "file not found" in error_lower or "no such file" in error_lower:
            return "file_error"
        elif "indentation" in error_lower:
            return "indentation_error"
        else:
            return "general_error"
    
    def apply_common_fixes(self, script_content: str) -> str:
        """Apply common fixes for known issues."""
        fixed_script = script_content
        
        # Fix matplotlib style issues
        fixed_script = fixed_script.replace("plt.style.use('seaborn')", "sns.set_style('whitegrid')")
        fixed_script = fixed_script.replace("plt.style.use('seaborn-v0_8')", "sns.set_style('whitegrid')")
        fixed_script = fixed_script.replace("plt.style.use('seaborn-v0_8-darkgrid')", "sns.set_style('darkgrid')")
        
        # Ensure proper imports
        if "import pandas" not in fixed_script:
            fixed_script = "import pandas as pd\n" + fixed_script
        if "import matplotlib.pyplot" not in fixed_script:
            fixed_script = "import matplotlib.pyplot as plt\n" + fixed_script
        if "import seaborn" not in fixed_script:
            fixed_script = "import seaborn as sns\n" + fixed_script
        if "import numpy" not in fixed_script:
            fixed_script = "import numpy as np\n" + fixed_script
        
        # Fix matplotlib backend for non-interactive environments
        if "plt.show()" in fixed_script and "plt.switch_backend" not in fixed_script:
            fixed_script = fixed_script.replace(
                "import matplotlib.pyplot as plt",
                "import matplotlib.pyplot as plt\nplt.switch_backend('Agg')"
            )
        
        # Fix common variable issues
        if "numerical_cols" in fixed_script and "numerical_cols = df.select_dtypes" not in fixed_script:
            # Add numerical_cols definition if it's used but not defined
            fixed_script = fixed_script.replace(
                "numerical_cols = df.select_dtypes(include=[np.number]).columns",
                "numerical_cols = df.select_dtypes(include=[np.number]).columns\nif len(numerical_cols) == 0:\n    numerical_cols = []"
            )
        
        # Remove any markdown formatting that might be left
        if fixed_script.startswith('```python'):
            fixed_script = fixed_script.replace('```python', '').replace('```', '')
        if fixed_script.startswith('```'):
            fixed_script = fixed_script.replace('```', '')
        
        return fixed_script
    
    def execute_with_retry(self, script_path: Path, original_prompt: str, dataset_info: dict) -> Tuple[bool, str, str]:
        """Execute script with automatic error fixing and retry."""
        
        for attempt in range(self.max_attempts):
            try:
                # Execute the script
                result = subprocess.run([sys.executable, str(script_path)], 
                                     capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    return True, result.stdout, ""
                
                # Script failed, analyze the error
                error_output = result.stderr
                self.error_history.append({
                    "attempt": attempt + 1,
                    "error": error_output,
                    "stdout": result.stdout
                })
                
                # Read current script
                with open(script_path, 'r') as f:
                    current_script = f.read()
                
                # Analyze error and get fix
                analysis_result = self.analyze_error(error_output, current_script, original_prompt, dataset_info)
                
                # Apply common fixes first
                fixed_script = self.apply_common_fixes(analysis_result["fixed_code"])
                
                # Write fixed script
                with open(script_path, 'w') as f:
                    f.write(fixed_script)
                
                # If this was the last attempt, return failure
                if attempt == self.max_attempts - 1:
                    return False, result.stdout, error_output
                
                # Continue to next attempt
                
            except subprocess.TimeoutExpired:
                return False, "", "Script execution timed out"
            except Exception as e:
                return False, "", f"Execution error: {str(e)}"
        
        return False, "", "Max attempts reached"
    
    def get_error_summary(self) -> str:
        """Get a summary of all errors encountered."""
        if not self.error_history:
            return "No errors encountered."
        
        summary = f"Error Summary ({len(self.error_history)} attempts):\n"
        for i, error_info in enumerate(self.error_history, 1):
            summary += f"\nAttempt {i}:\n"
            summary += f"Error: {error_info['error'][:200]}...\n"
            if error_info['stdout']:
                summary += f"Output: {error_info['stdout'][:100]}...\n"
        
        return summary 