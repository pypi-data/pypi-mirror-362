"""
Tests for CLI functionality
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from promptversion.cli import cli


class TestCLI:
    def setup_method(self):
        """Setup temporary directory for tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = Path.cwd()
        Path(self.temp_dir).chmod(0o755)
        import os

        os.chdir(self.temp_dir)
        self.runner = CliRunner()

    def teardown_method(self):
        """Cleanup temporary directory"""
        import os

        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)

    def test_init_command(self):
        """Test promptversion init"""
        result = self.runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert "✓ Initialized prompt repository" in result.output
        assert Path("prompts").exists()
        assert Path(".promptversion").exists()
        assert Path("prompts/example.yaml").exists()

    def test_create_command(self):
        """Test promptversion create"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(
            cli, ["create", "test_prompt", "--description", "Test prompt"]
        )
        assert result.exit_code == 0
        assert "Created prompt 'test_prompt'" in result.output
        assert Path("prompts/test_prompt.yaml").exists()

    def test_list_command(self):
        """Test promptversion list"""
        self.runner.invoke(cli, ["init"])
        self.runner.invoke(cli, ["create", "prompt1"])
        self.runner.invoke(cli, ["create", "prompt2"])

        result = self.runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "prompt1" in result.output
        assert "prompt2" in result.output
        assert "example" in result.output

    def test_show_command(self):
        """Test promptversion show"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["show", "example"])
        assert result.exit_code == 0
        assert "Prompt: example" in result.output
        assert "Version:" in result.output
        assert "Template:" in result.output

    def test_show_vars_command(self):
        """Test promptversion show --vars"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["show", "example", "--vars"])
        assert result.exit_code == 0
        assert "Variables:" in result.output
        assert "name:" in result.output

    def test_test_command(self):
        """Test promptversion test"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["test", "example", "--var", "name=Alice"])
        assert result.exit_code == 0
        assert "Rendered prompt 'example'" in result.output
        assert "Alice" in result.output

    def test_versions_command_no_history(self):
        """Test promptversion versions with no history"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["versions", "example"])
        assert result.exit_code == 0
        assert "No version history" in result.output

    def test_error_handling(self):
        """Test error cases"""
        self.runner.invoke(cli, ["init"])

        # Test nonexistent prompt
        result = self.runner.invoke(cli, ["show", "nonexistent"])
        assert result.exit_code == 0
        assert "Error showing prompt" in result.output

        # Test invalid variable format
        result = self.runner.invoke(cli, ["test", "example", "--var", "invalid_format"])
        assert result.exit_code == 0
        assert "Invalid variable format" in result.output
