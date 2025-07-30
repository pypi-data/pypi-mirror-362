"""
Tests for missing CLI functionality and edge cases
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from click.testing import CliRunner
from promptversion.cli import cli


class TestCLICommitAndTag:
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

    def test_commit_command(self):
        """Test promptversion commit"""
        # Setup
        self.runner.invoke(cli, ["init"])
        self.runner.invoke(cli, ["create", "test_prompt"])

        # Modify the prompt file
        prompt_path = Path("prompts/test_prompt.yaml")
        with open(prompt_path) as f:
            data = yaml.safe_load(f)

        data["template"] = "Modified template {{user_input}}"
        data["version"] = "0.2.0"  # This will be overridden by commit

        with open(prompt_path, "w") as f:
            yaml.dump(data, f)

        # Test commit
        result = self.runner.invoke(
            cli,
            [
                "commit",
                "test_prompt",
                "--message",
                "Updated template",
                "--bump",
                "minor",
            ],
        )
        assert result.exit_code == 0
        assert "Committed test_prompt" in result.output
        assert "Updated template" in result.output

        # Verify version was bumped (should be higher than 0.1.0)
        with open(prompt_path) as f:
            updated_data = yaml.safe_load(f)

        # Version should be bumped from 0.1.0
        version_parts = updated_data["version"].split(".")
        major, minor, patch = map(int, version_parts)

        # For minor bump from 0.1.0, should be 0.2.0 or higher
        assert minor >= 2 or major > 0

        # Check version history (should contain the new version)
        result = self.runner.invoke(cli, ["versions", "test_prompt"])
        assert result.exit_code == 0
        assert (
            updated_data["version"] in result.output
        )  # Check for the actual version that was created
        assert "Updated template" in result.output

    def test_tag_command(self):
        """Test promptversion tag"""
        # Setup with a committed version
        self.runner.invoke(cli, ["init"])
        self.runner.invoke(cli, ["create", "test_prompt"])
        self.runner.invoke(
            cli, ["commit", "test_prompt", "--message", "Initial", "--bump", "patch"]
        )

        # Create tag
        result = self.runner.invoke(cli, ["tag", "test_prompt", "stable", "0.1.1"])
        assert result.exit_code == 0
        assert "Tagged test_prompt v0.1.1 as 'stable'" in result.output

        # Test tag without specifying version (should use current)
        result = self.runner.invoke(cli, ["tag", "test_prompt", "latest"])
        assert result.exit_code == 0
        assert "Tagged test_prompt" in result.output
        assert "as 'latest'" in result.output

    def test_commit_nonexistent_prompt(self):
        """Test commit with nonexistent prompt"""
        self.runner.invoke(cli, ["init"])

        result = self.runner.invoke(cli, ["commit", "nonexistent", "--message", "test"])
        assert result.exit_code == 0
        assert "Error committing" in result.output


class TestEdgeCases:
    def setup_method(self):
        """Setup temporary directory for tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = Path.cwd()
        Path(self.temp_dir).chmod(0o755)
        import os

        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Cleanup temporary directory"""
        import os

        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)

    def test_corrupted_yaml_file(self):
        """Test handling of corrupted YAML files"""
        from promptversion import PromptVersion

        # Create valid structure
        Path("prompts").mkdir()
        Path(".promptversion").mkdir()

        # Create corrupted YAML
        with open("prompts/corrupted.yaml", "w") as f:
            f.write("invalid: yaml: content: [\n")

        pv = PromptVersion()
        with pytest.raises(Exception):  # Should raise YAML parsing error
            pv.get("corrupted")

    def test_missing_promptversion_directory(self):
        """Test behavior when .promptversion directory is missing"""
        from promptversion import VersionManager

        # This should create the directory automatically
        vm = VersionManager()
        assert Path(".promptversion").exists()
        assert vm.config_file.exists()

    def test_unicode_and_special_characters(self):
        """Test prompts with unicode and special characters"""
        from promptversion import PromptVersion

        pv = PromptVersion()

        # Create prompt with unicode
        template = (
            "Hello {{name}}! 你好 {{chinese_name}}! Emoji: 🚀 Special chars: @#$%^&*()"
        )
        variables = {
            "name": {"default": "World", "type": "string"},
            "chinese_name": {"default": "世界", "type": "string"},
        }

        prompt = pv.create_prompt("unicode_test", template, variables)

        # Test rendering
        result = pv.render("unicode_test", {"name": "Alice", "chinese_name": "爱丽丝"})
        assert "Hello Alice!" in result
        assert "你好 爱丽丝!" in result
        assert "🚀" in result

    def test_very_large_prompt(self):
        """Test handling of very large prompts"""
        from promptversion import PromptVersion

        pv = PromptVersion()

        # Create large template (10KB)
        large_template = (
            "This is a very long prompt. " * 500 + "Final message: {{message}}"
        )

        prompt = pv.create_prompt(
            "large_prompt",
            large_template,
            {"message": {"default": "Hello", "type": "string"}},
        )

        # Should handle large prompts fine
        result = pv.render("large_prompt", {"message": "Large prompt works!"})
        assert "Large prompt works!" in result
        assert len(result) > 10000

    def test_empty_variables(self):
        """Test prompts with no variables"""
        from promptversion import PromptVersion

        pv = PromptVersion()

        # Create prompt with no variables
        prompt = pv.create_prompt(
            "no_vars", "This is a static prompt with no variables."
        )

        # Should render fine
        result = pv.render("no_vars")
        assert result == "This is a static prompt with no variables."

    def test_nested_variables(self):
        """Test complex nested variable structures"""
        from promptversion import PromptVersion

        pv = PromptVersion()

        template = """
System: {{system_role}}
{% for item in items %}
- {{item.name}}: {{item.value}}
{% endfor %}
User: {{user_message}}
"""

        variables = {
            "system_role": {"default": "Assistant", "type": "string"},
            "items": {"default": [], "type": "list"},
            "user_message": {"default": "Hello", "type": "string"},
        }

        prompt = pv.create_prompt("nested_test", template, variables)

        # Test with complex data
        result = pv.render(
            "nested_test",
            {
                "system_role": "Expert",
                "items": [
                    {"name": "priority", "value": "high"},
                    {"name": "category", "value": "technical"},
                ],
                "user_message": "Help me debug",
            },
        )

        assert "System: Expert" in result
        assert "priority: high" in result
        assert "category: technical" in result
        assert "User: Help me debug" in result


class TestCaching:
    def setup_method(self):
        """Setup temporary directory for tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = Path.cwd()
        Path(self.temp_dir).chmod(0o755)
        import os

        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Cleanup temporary directory"""
        import os

        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)

    def test_caching_behavior(self):
        """Test that caching works correctly"""
        from promptversion import PromptVersion

        pv = PromptVersion()
        pv.create_prompt(
            "cache_test", "Template {{var}}", {"var": {"default": "value"}}
        )

        # First call should load from file
        prompt1 = pv.get("cache_test")

        # Second call should use cache
        prompt2 = pv.get("cache_test")

        # Should be same object (cached)
        assert prompt1 is prompt2

        # Cache should be cleared after creating new prompt
        pv.create_prompt("new_prompt", "New {{var}}")

        # This should reload from file
        prompt3 = pv.get("cache_test")
        assert prompt3 is not prompt1  # Cache was cleared
