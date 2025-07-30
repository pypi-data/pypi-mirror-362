"""
Tests for version management functionality
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from promptversion.version_manager import VersionManager


class TestVersionManager:
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
        """Test VersionManager initialization"""
        vm = VersionManager()
        assert vm.config_dir.exists()
        assert vm.versions_file.exists()
        assert vm.tags_file.exists()
        assert vm.config_file.exists()

    def test_version_bumping(self):
        """Test semantic version bumping"""
        vm = VersionManager()

        # Test patch bump
        assert vm.bump_version("1.0.0", "patch") == "1.0.1"
        assert vm.bump_version("1.2.3", "patch") == "1.2.4"

        # Test minor bump
        assert vm.bump_version("1.0.0", "minor") == "1.1.0"
        assert vm.bump_version("1.2.3", "minor") == "1.3.0"

        # Test major bump
        assert vm.bump_version("1.0.0", "major") == "2.0.0"
        assert vm.bump_version("1.2.3", "major") == "2.0.0"

    def test_invalid_version_format(self):
        """Test error handling for invalid version formats"""
        vm = VersionManager()

        with pytest.raises(ValueError, match="Invalid version format"):
            vm.bump_version("invalid", "patch")

    def test_record_version(self):
        """Test recording new versions"""
        vm = VersionManager()

        vm.record_version("test_prompt", "1.0.0", "Initial version", "test_author")

        versions = vm.get_versions("test_prompt")
        assert "1.0.0" in versions["versions"]
        assert versions["current"] == "1.0.0"
        assert versions["versions"]["1.0.0"]["message"] == "Initial version"
        assert versions["versions"]["1.0.0"]["author"] == "test_author"

    def test_multiple_versions(self):
        """Test recording multiple versions"""
        vm = VersionManager()

        vm.record_version("test_prompt", "1.0.0", "Initial version")
        vm.record_version("test_prompt", "1.1.0", "Added feature")
        vm.record_version("test_prompt", "1.1.1", "Bug fix")

        versions = vm.get_versions("test_prompt")
        assert len(versions["versions"]) == 3
        assert versions["current"] == "1.1.1"

    def test_tags(self):
        """Test tag creation and retrieval"""
        vm = VersionManager()

        # Create some versions first
        vm.record_version("test_prompt", "1.0.0", "Initial")
        vm.record_version("test_prompt", "1.1.0", "Feature")

        # Create tags
        vm.create_tag("stable", "test_prompt", "1.0.0")
        vm.create_tag("latest", "test_prompt", "1.1.0")

        tags = vm.get_tags("test_prompt")
        assert tags["stable"] == "1.0.0"
        assert tags["latest"] == "1.1.0"

    def test_version_resolution(self):
        """Test resolving versions and tags"""
        vm = VersionManager()

        vm.record_version("test_prompt", "1.0.0", "Initial")
        vm.create_tag("stable", "test_prompt", "1.0.0")

        # Test version number resolution
        assert vm.resolve_version("test_prompt", "1.0.0") == "1.0.0"

        # Test tag resolution
        assert vm.resolve_version("test_prompt", "stable") == "1.0.0"

        # Test invalid version/tag
        with pytest.raises(ValueError, match="Unknown version or tag"):
            vm.resolve_version("test_prompt", "nonexistent")
