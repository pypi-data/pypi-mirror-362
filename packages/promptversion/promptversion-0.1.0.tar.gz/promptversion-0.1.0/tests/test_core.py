"""
Tests for core PromptVersion functionality
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from promptversion.core import PromptVersion, Prompt


class TestPrompt:
    def test_prompt_creation(self):
        """Test basic prompt creation"""
        prompt = Prompt(
            name="test",
            version="1.0.0",
            template="Hello {{name}}!",
            variables={"name": {"default": "World", "type": "string"}},
            description="Test prompt",
        )

        assert prompt.name == "test"
        assert prompt.version == "1.0.0"
        assert "name" in prompt.variables

    def test_prompt_rendering(self):
        """Test prompt rendering with variables"""
        prompt = Prompt(
            name="test",
            version="1.0.0",
            template="Hello {{name}}! You are {{age}} years old.",
            variables={
                "name": {"default": "World", "type": "string"},
                "age": {"default": 25, "type": "integer"},
            },
        )

        # Test with defaults
        result = prompt.render()
        assert "Hello World!" in result
        assert "25 years old" in result

        # Test with overrides
        result = prompt.render({"name": "Alice", "age": 30})
        assert "Hello Alice!" in result
        assert "30 years old" in result

    def test_prompt_missing_variables(self):
        """Test error when required variables are missing"""
        prompt = Prompt(
            name="test",
            version="1.0.0",
            template="Hello {{name}}! {{required_var}}",
            variables={"name": {"default": "World"}},
        )

        with pytest.raises(ValueError, match="Missing required variables"):
            prompt.render()


class TestPromptVersion:
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

    def test_initialization(self):
        """Test PromptVersion initialization"""
        pv = PromptVersion()
        assert pv.prompts_dir.name == "prompts"
        assert pv.config_dir.name == ".promptversion"
        assert pv.prompts_dir.exists()
        assert pv.config_dir.exists()

    def test_create_prompt(self):
        """Test creating a new prompt"""
        pv = PromptVersion()

        prompt = pv.create_prompt(
            "test_prompt",
            "Hello {{name}}!",
            {"name": {"default": "World", "type": "string"}},
            "Test description",
        )

        assert prompt.name == "test_prompt"
        assert prompt.version == "0.1.0"
        assert (pv.prompts_dir / "test_prompt.yaml").exists()

    def test_get_prompt(self):
        """Test retrieving a prompt"""
        pv = PromptVersion()

        # Create a prompt first
        pv.create_prompt("test", "Hello {{name}}!", {"name": {"default": "World"}})

        # Retrieve it
        prompt = pv.get("test")
        assert prompt.name == "test"
        assert prompt.template == "Hello {{name}}!"

    def test_render_convenience(self):
        """Test convenience render method"""
        pv = PromptVersion()

        pv.create_prompt("test", "Hello {{name}}!", {"name": {"default": "World"}})

        result = pv.render("test", {"name": "Alice"})
        assert "Hello Alice!" in result

    def test_list_prompts(self):
        """Test listing prompts"""
        pv = PromptVersion()

        pv.create_prompt("prompt1", "Template 1")
        pv.create_prompt("prompt2", "Template 2")

        prompts = pv.list_prompts()
        assert "prompt1" in prompts
        assert "prompt2" in prompts
        assert len(prompts) == 2
