# Exponent-ML

**Prompt + Dataset → Trained + Deployed ML Models in One Line**

Exponent-ML is a CLI tool that lets anyone create, train, and deploy machine learning models by describing their task and uploading a dataset. The tool uses LLMs to generate runnable training pipelines based on both user intent and real dataset structure, with optional deployment to GitHub or cloud platforms.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/exponent-ml.git
cd exponent-ml

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Setup

Create a `.env` file with your API keys:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Authentication (OAuth)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Optional (for cloud features)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket_name
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
GITHUB_TOKEN=your_github_token
```

**Note**: Only `ANTHROPIC_API_KEY` is required. OAuth credentials are needed for authentication.

### Authentication Setup

Before using Exponent-ML, you need to set up OAuth authentication:

#### Option 1: Use the setup script
```bash
# Set up Google OAuth
python scripts/setup_oauth.py google

# Set up GitHub OAuth  
python scripts/setup_oauth.py github

# Check your configuration
python scripts/setup_oauth.py check
```

#### Option 2: Manual setup
1. **Google OAuth**: Go to [Google Cloud Console](https://console.developers.google.com/)
   - Create a new project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Set redirect URI to `http://localhost:8080`

2. **GitHub OAuth**: Go to [GitHub OAuth Apps](https://github.com/settings/developers)
   - Create a new OAuth App
   - Set callback URL to `http://localhost:8080`

3. Add credentials to your `.env` file:
```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### Basic Usage

```bash
# Login with OAuth
exponent login --provider google
exponent login --provider github

# Check authentication status
exponent status

# Interactive wizard
exponent init

# Quick start with task and dataset
exponent init quick "Predict email spam" --dataset spam.csv

# Train a model
exponent train

# Deploy to GitHub
exponent deploy
```

## 📋 Commands

### `exponent init`

Initialize a new ML project with interactive wizard:

```bash
exponent init
```

**Options:**
- `--task, -t`: ML task description
- `--dataset, -d`: Path to dataset file
- `--interactive, -i`: Run in interactive mode (default: True)

**Subcommands:**
- `exponent init quick <task>`: Quick initialization without prompts

### `exponent upload-dataset`

Analyze datasets and optionally upload to S3 for cloud training:

```bash
exponent upload-dataset spam.csv
```

**Options:**
- `--project-id, -p`: Project ID for organization
- `--upload, -u`: Upload to S3 for cloud training

**Subcommands:**
- `exponent upload-dataset analyze <file>`: Analyze dataset without uploading

### `exponent train`

Train ML models locally or in the cloud:

```bash
exponent train
```

**Options:**
- `--project-id, -p`: Project ID to train
- `--dataset, -d`: Path to dataset file
- `--task, -t`: Task description
- `--cloud, -c`: Use cloud training (Modal)
- `--s3`: Upload dataset to S3 for cloud training

**Subcommands:**
- `exponent train status <job_id>`: Check training job status
- `exponent train list`: List all training jobs

### `exponent deploy`

Deploy projects to GitHub:

```bash
exponent deploy
```

**Options:**
- `--project-id, -p`: Project ID to deploy
- `--name, -n`: GitHub repository name
- `--path`: Path to project directory

**Subcommands:**
- `exponent deploy list`: List GitHub repositories

## 🧠 How It Works

1. **Task Description**: You describe your ML task in natural language
2. **Dataset Analysis**: The tool analyzes your dataset structure (columns, types, etc.)
3. **Code Generation**: An LLM generates production-ready Python code based on your task and dataset
4. **Dynamic Training**: The generated code is executed in Modal's cloud infrastructure
5. **Deployment**: Projects can be deployed to GitHub with automated workflows

**No hard-coded templates** - every model is generated specifically for your task and dataset!

## 📁 Generated Project Structure

```
~/.exponent/<project-id>/
├── model.py          # Model definition and training pipeline
├── train.py          # Training script with data loading
├── predict.py        # Prediction script for making predictions
├── requirements.txt  # Python dependencies
└── README.md        # Project documentation
```

## 🔧 Configuration

### Required Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key for code generation

### Optional Environment Variables

- `AWS_ACCESS_KEY_ID`: AWS access key for S3 uploads
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for S3 uploads
- `AWS_REGION`: AWS region (default: us-east-1)
- `S3_BUCKET`: S3 bucket name for dataset storage
- `MODAL_TOKEN_ID`: Modal token for cloud training
- `MODAL_TOKEN_SECRET`: Modal token secret for cloud training
- `GITHUB_TOKEN`: GitHub token for repository creation

## 🛠️ Development

### Project Structure

```
exponent-ml/
├── exponent/
│   ├── cli/              # CLI interface (Typer)
│   │   └── commands/     # CLI commands
│   ├── core/             # Core logic
│   │   ├── code_gen.py   # LLM code generation
│   │   ├── config.py     # Configuration management
│   │   ├── s3_utils.py   # S3 dataset handling
│   │   ├── modal_runner.py # Modal cloud training
│   │   └── github_utils.py # GitHub deployment
│   └── main.py           # CLI entry point
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

### Local Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Format code
black exponent/
isort exponent/

# Lint code
flake8 exponent/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com/) for Claude API
- [Modal](https://modal.com/) for cloud infrastructure
- [Typer](https://typer.tiangolo.com/) for CLI framework
- [scikit-learn](https://scikit-learn.org/) for ML algorithms 