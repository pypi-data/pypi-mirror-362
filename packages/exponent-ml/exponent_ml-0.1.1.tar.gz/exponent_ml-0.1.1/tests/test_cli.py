import pytest
from typer.testing import CliRunner
from exponent.main import app

runner = CliRunner()

class TestCLI:
    def test_version(self):
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Exponent-ML v0.1.0" in result.stdout
    
    def test_help(self):
        result = runner.invoke(app, ["help"])
        assert result.exit_code == 0
        assert "Exponent-ML" in result.stdout
    
    @patch('exponent.core.auth.auth_manager.is_authenticated')
    def test_analyze_requires_auth(self, mock_auth):
        mock_auth.return_value = False
        result = runner.invoke(app, ["analyze", "test.csv"])
        assert result.exit_code != 0  # Should fail without auth
    
    @patch('exponent.core.auth.auth_manager.is_authenticated')
    @patch('exponent.cli.commands.analyze.run_analysis')
    def test_analyze_with_auth(self, mock_analysis, mock_auth):
        mock_auth.return_value = True
        result = runner.invoke(app, ["analyze", "test.csv"])
        assert result.exit_code == 0
        mock_analysis.assert_called_once() 