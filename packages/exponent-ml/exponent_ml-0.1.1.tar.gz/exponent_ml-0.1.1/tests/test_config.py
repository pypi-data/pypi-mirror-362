import pytest
from unittest.mock import patch, mock_open
from exponent.core.config import get_config, check_optional_services
import os

class TestConfig:
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test_key',
        'AWS_ACCESS_KEY_ID': 'test_aws_key',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret',
        'CLERK_PUBLISHABLE_KEY': 'pk_test_123',
        'CLERK_SECRET_KEY': 'sk_test_123'
    })
    def test_get_config(self):
        config = get_config()
        assert config.ANTHROPIC_API_KEY == 'test_key'
        assert config.AWS_ACCESS_KEY_ID == 'test_aws_key'
        assert config.CLERK_PUBLISHABLE_KEY == 'pk_test_123'
    
    def test_get_config_missing_required(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                get_config()
    
    @patch.dict(os.environ, {
        'ANTHROPIC_API_KEY': 'test_key',
        'AWS_ACCESS_KEY_ID': 'test_aws_key',
        'AWS_SECRET_ACCESS_KEY': 'test_aws_secret',
        'S3_BUCKET': 'test_bucket',
        'MODAL_TOKEN_ID': 'test_modal_id',
        'MODAL_TOKEN_SECRET': 'test_modal_secret',
        'GITHUB_TOKEN': 'test_github_token'
    })
    def test_check_optional_services(self):
        services = check_optional_services()
        assert services['s3'] == True
        assert services['modal'] == True
        assert services['github'] == True 