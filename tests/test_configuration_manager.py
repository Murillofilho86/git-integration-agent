import json

import pytest

from core.configuration_manager import ConfigurationManager


@pytest.fixture(autouse=True)
def reset_singleton():
    # ConfigurationManager is a process-wide singleton that reads
    # ./config.json relative to the CWD -- each test needs a clean
    # instance pointed at its own tmp_path.
    ConfigurationManager._instance = None
    yield
    ConfigurationManager._instance = None


class TestConfigurationManager:

    def test_raises_when_config_json_missing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        with pytest.raises(RuntimeError, match="config.json"):
            ConfigurationManager()

    def test_get_claude_path_reads_flat_key(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "config.json").write_text(
            json.dumps({"claude_path": "/usr/local/bin/claude"})
        )

        config = ConfigurationManager()

        assert config.get_claude_path() == "/usr/local/bin/claude"

    def test_get_claude_path_raises_when_absent(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "config.json").write_text(json.dumps({}))

        config = ConfigurationManager()

        with pytest.raises(RuntimeError, match="claude_path"):
            config.get_claude_path()

    def test_get_workspace_root_defaults_to_workspace(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "config.json").write_text(
            json.dumps({"claude_path": "/usr/local/bin/claude"})
        )

        config = ConfigurationManager()

        assert config.get_workspace_root() == "workspace"

    def test_get_workspace_root_reads_custom_value(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "config.json").write_text(
            json.dumps({"claude_path": "/x", "workspace_root": "custom-workspace"})
        )

        config = ConfigurationManager()

        assert config.get_workspace_root() == "custom-workspace"

    def test_is_a_singleton(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "config.json").write_text(
            json.dumps({"claude_path": "/x"})
        )

        first = ConfigurationManager()
        second = ConfigurationManager()

        assert first is second
