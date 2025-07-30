import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
import tempfile
import os

from exponent.core.auth import AuthManager, AuthCallbackHandler
from queue import Queue

class TestAuthManager:
    def setup_method(self):
        self.auth_manager = AuthManager()
        self.temp_dir = tempfile.mkdtemp()
        self.auth_manager.token_file = Path(self.temp_dir) / "auth_token.json"
    
    def teardown_method(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_store_and_get_token(self):
        token_data = {"access_token": "test_token", "user_id": "123"}
        self.auth_manager.store_token(token_data)
        
        retrieved = self.auth_manager.get_stored_token()
        assert retrieved == token_data
    
    def test_clear_token(self):
        token_data = {"access_token": "test_token"}
        self.auth_manager.store_token(token_data)
        assert self.auth_manager.token_file.exists()
        
        self.auth_manager.clear_token()
        assert not self.auth_manager.token_file.exists()
    
    @patch('exponent.core.auth.Clerk')
    def test_initialize_clerk(self, mock_clerk):
        with patch.dict(os.environ, {
            'CLERK_PUBLISHABLE_KEY': 'pk_test_123',
            'CLERK_SECRET_KEY': 'sk_test_123'
        }):
            self.auth_manager.initialize_clerk()
            mock_clerk.assert_called_once_with(secret_key='sk_test_123')
    
    def test_initialize_clerk_missing_keys(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Clerk keys not found"):
                self.auth_manager.initialize_clerk()

class TestAuthCallbackHandler:
    def test_successful_callback(self):
        auth_code_queue = Queue()
        handler = AuthCallbackHandler(auth_code_queue, None, None, None)
        
        # Mock the request
        handler.path = "/?code=test_auth_code"
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        handler.wfile = Mock()
        
        handler.do_GET()
        
        # Check that auth code was put in queue
        auth_code = auth_code_queue.get_nowait()
        assert auth_code == "test_auth_code"
        
        # Check response was sent
        handler.send_response.assert_called_with(200) 