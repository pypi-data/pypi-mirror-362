"""
Integration tests for version retrieval and end-to-end workflows
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from promptversion.core import PromptVersion
from promptversion.version_manager import VersionManager


class TestVersionRetrieval:
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

    def test_version_storage_and_retrieval(self):
        """Test complete version workflow"""
        pv = PromptVersion()
        vm = VersionManager()

        # Create initial prompt
        prompt = pv.create_prompt(
            "test_prompt",
            "Version 1: Hello {{name}}!",
            {"name": {"default": "World", "type": "string"}},
            "Test prompt",
        )

        # Commit first version
        prompt_data = {
            "name": "test_prompt",
            "version": "1.0.0",
            "template": "Version 1: Hello {{name}}!",
            "variables": {"name": {"default": "World", "type": "string"}},
            "description": "Test prompt",
        }
        vm.record_version(
            "test_prompt", "1.0.0", "Initial version", prompt_data=prompt_data
        )

        # Update prompt
        prompt_path = Path("prompts/test_prompt.yaml")
        new_data = {
            "name": "test_prompt",
            "version": "1.1.0",
            "template": "Version 2: Hi {{name}}! How are you?",
            "variables": {"name": {"default": "Friend", "type": "string"}},
            "description": "Updated test prompt",
        }

        with open(prompt_path, "w") as f:
            import yaml

            yaml.dump(new_data, f)

        # Commit second version
        vm.record_version(
            "test_prompt", "1.1.0", "Updated greeting", prompt_data=new_data
        )

        # Clear cache to force fresh load
        pv._cache.clear()

        # Test retrieving different versions
        current_prompt = pv.get("test_prompt")
        assert current_prompt.version == "1.1.0"
        assert "Version 2: Hi" in current_prompt.template

        # Test retrieving old version
        old_prompt = pv.get("test_prompt", version="1.0.0")
        assert old_prompt.version == "1.0.0"
        assert "Version 1: Hello" in old_prompt.template

        # Test rendering different versions
        current_render = pv.render("test_prompt", {"name": "Alice"})
        assert "Version 2: Hi Alice!" in current_render

        old_render = pv.render("test_prompt", {"name": "Alice"}, version="1.0.0")
        assert "Version 1: Hello Alice!" in old_render

    def test_nonexistent_version(self):
        """Test error handling for nonexistent versions"""
        pv = PromptVersion()
        pv.create_prompt("test", "Hello {{name}}!")

        with pytest.raises(ValueError, match="Version 9.9.9 not found"):
            pv.get("test", version="9.9.9")

    def test_prompt_not_found(self):
        """Test error handling for nonexistent prompts"""
        pv = PromptVersion()

        with pytest.raises(FileNotFoundError, match="Prompt 'nonexistent' not found"):
            pv.get("nonexistent")


class TestEndToEndWorkflow:
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

    def test_complete_workflow(self):
        """Test complete prompt lifecycle"""
        pv = PromptVersion()
        vm = VersionManager()

        # 1. Create prompt
        prompt = pv.create_prompt(
            "chatbot",
            "You are a {{personality}} assistant. Help with: {{task}}",
            {
                "personality": {"default": "helpful", "type": "string"},
                "task": {"default": "general questions", "type": "string"},
            },
            "A configurable chatbot prompt",
        )

        assert prompt.name == "chatbot"
        assert len(pv.list_prompts()) == 1

        # 2. Test rendering
        result = pv.render(
            "chatbot", {"personality": "friendly", "task": "customer support"}
        )
        assert "friendly assistant" in result
        assert "customer support" in result

        # 3. Create tag
        vm.create_tag("stable", "chatbot", "0.1.0")
        tags = vm.get_tags("chatbot")
        assert tags["stable"] == "0.1.0"

        # 4. Test tag resolution
        resolved = vm.resolve_version("chatbot", "stable")
        assert resolved == "0.1.0"

        # 5. Test version bumping
        new_version = vm.bump_version("0.1.0", "minor")
        assert new_version == "0.2.0"
