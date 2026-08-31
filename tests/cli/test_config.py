"""Tests for ConfigManager persistence."""

import logging
import os

import pytest

from hyperextract.cli.config import ConfigManager

# Fixture-only dummy; never a real key from the environment.
_FAKE_API_KEY = "sk-test"

_POSIX_ONLY = pytest.mark.skipif(
    os.name == "nt",
    reason="POSIX file modes are not enforced on Windows",
)


def test_save_creates_custom_parent_dir(tmp_path):
    """_save() must create the parent of a custom config_path, not the default dir."""
    cfg_path = tmp_path / "nested" / "dir" / "config.toml"  # parent doesn't exist yet

    mgr = ConfigManager(cfg_path)
    mgr.set_llm(provider="openai", model="gpt-4o-mini", api_key="sk-x")

    assert cfg_path.exists()

    # Round-trips back through a fresh manager.
    reloaded = ConfigManager(cfg_path)
    assert reloaded.llm.model == "gpt-4o-mini"


@_POSIX_ONLY
def test_save_sets_owner_only_permissions(tmp_path):
    cfg_path = tmp_path / "config.toml"
    mgr = ConfigManager(cfg_path)
    mgr.set_llm(provider="openai", model="gpt-4o-mini", api_key=_FAKE_API_KEY)

    assert cfg_path.stat().st_mode & 0o777 == 0o600


@_POSIX_ONLY
def test_save_tightens_existing_world_readable_file(tmp_path):
    cfg_path = tmp_path / "config.toml"
    cfg_path.write_text(
        '[llm]\nprovider = "openai"\nmodel = "gpt-4o-mini"\n'
        f'api_key = "{_FAKE_API_KEY}"\nbase_url = ""\n',
        encoding="utf-8",
    )
    cfg_path.chmod(0o644)
    assert cfg_path.stat().st_mode & 0o777 == 0o644

    mgr = ConfigManager(cfg_path)
    mgr.set_llm(provider="openai", api_key=_FAKE_API_KEY)

    assert cfg_path.stat().st_mode & 0o777 == 0o600


@_POSIX_ONLY
def test_load_warns_when_config_is_group_or_world_readable(tmp_path, caplog):
    cfg_path = tmp_path / "config.toml"
    cfg_path.write_text(
        '[llm]\nprovider = "openai"\nmodel = "gpt-4o-mini"\n'
        f'api_key = "{_FAKE_API_KEY}"\nbase_url = ""\n',
        encoding="utf-8",
    )
    cfg_path.chmod(0o644)

    with caplog.at_level(logging.WARNING, logger="hyperextract.cli.config"):
        ConfigManager(cfg_path)

    assert caplog.records
    assert any("0600" in record.getMessage() for record in caplog.records)
    assert _FAKE_API_KEY not in caplog.text
