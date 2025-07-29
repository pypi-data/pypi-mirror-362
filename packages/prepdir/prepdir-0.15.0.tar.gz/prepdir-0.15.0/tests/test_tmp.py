import json
import logging
import os
import pytest
import yaml
from io import StringIO
from unittest.mock import patch, MagicMock
from pathlib import Path
from dynaconf import Dynaconf
from prepdir.config import (
    load_config,
    check_namespace_value,
    init_config,
    check_config_format,
    get_bundled_config,
    is_resource,
)
from prepdir import prepdir_logging

# Set up logger
logger = logging.getLogger("prepdir.config")


# Custom handler to capture log records in a list
class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)

    def flush(self):
        pass


@pytest.fixture
def clean_cwd(tmp_path):
    """Change working directory to a clean temporary path to avoid loading real configs."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)


@pytest.fixture
def sample_config_content():
    """Provide sample configuration content."""
    return {
        "EXCLUDE": {
            "DIRECTORIES": [".gitdir", "__pycache__dir"],
            "FILES": ["*.myexttodisclude", "*.mylog"],
        },
        "REPLACEMENT_UUID": "12345678-1234-1234-4321-4321432143214321",
        "SCRUB_HYPHENATED_UUIDS": True,
        "SCRUB_HYPHENLESS_UUIDS": False,
    }


@pytest.fixture
def expected_bundled_config_content():
    """Sample of expected values in src/prepdir/config.yaml"""
    return {
        "DEFAULT_EXTENSIONS": [],
        "EXCLUDE": {
            "DIRECTORIES": [".git", "__pycache__"],
            "FILES": ["*.pyc", "*.log"],
        },
        "DEFAULT_OUTPUT_FILE": "prepped_dir.txt",
        "REPLACEMENT_UUID": "00000000-0000-0000-0000-000000000000",
        "SCRUB_HYPHENATED_UUIDS": True,
        "SCRUB_HYPHENLESS_UUIDS": True,
    }


@pytest.fixture
def clean_logger():
    """Clean logger setup and teardown with a ListHandler to capture log records."""
    logger.handlers.clear()
    prepdir_logging.configure_logging(logger, level=logging.DEBUG)

    # Add ListHandler to capture log records
    list_handler = ListHandler()
    list_handler.setLevel(logging.DEBUG)
    logger.addHandler(list_handler)

    yield logger

    # Clean up
    logger.removeHandler(list_handler)
    list_handler.close()
    logger.handlers.clear()


def test_load_config_no_files_no_bundled(clean_cwd, clean_logger):
    """Test load_config when no files are found and bundled config is skipped (lines 195-196)."""
    with patch.dict(os.environ, {"PREPDIR_SKIP_CONFIG_FILE_LOAD": "true", "PREPDIR_SKIP_BUNDLED_CONFIG_LOAD": "true"}):
        config = load_config("prepdir", quiet=True)
        assert config.get("exclude.directories", []) == []
        assert config.get("exclude.files", []) == []
        assert any(
            "No custom, home, local, or bundled config files found" in record.message
            for record in clean_logger.handlers[-1].records
        )


def test_load_config_temp_file_cleanup_failure(clean_cwd, clean_logger):
    """Test load_config temporary file cleanup failure (lines 220-222)."""
    with patch.dict(os.environ, {"PREPDIR_SKIP_CONFIG_FILE_LOAD": "true", "PREPDIR_SKIP_BUNDLED_CONFIG_LOAD": "false"}):
        with patch("pathlib.Path.unlink", side_effect=OSError("Cannot delete")):
            config = load_config("prepdir", quiet=True)
            assert isinstance(config, Dynaconf)
            assert any(
                "Failed to remove temporary bundled config" in record.message
                for record in clean_logger.handlers[-1].records
            )


def test_init_config_create_failure(clean_cwd, clean_logger):
    """Test init_config file creation failure (lines 229-231)."""
    config_path = clean_cwd / ".prepdir" / "config.yaml"
    with patch("pathlib.Path.write_text", side_effect=OSError("Permission denied")):
        with pytest.raises(SystemExit, match="Error: Failed to create config file"):
            init_config("prepdir", str(config_path), force=True)
        assert any("Failed to create config file" in record.message for record in clean_logger.handlers[-1].records)


def test_load_config_no_home_no_local(clean_cwd, clean_logger):
    """Test load_config when no home or local config exists (lines 167, 169-170)."""
    home_dir = clean_cwd / "home"
    home_dir.mkdir()
    with patch.dict(
        os.environ,
        {"HOME": str(home_dir), "PREPDIR_SKIP_CONFIG_FILE_LOAD": "false", "PREPDIR_SKIP_BUNDLED_CONFIG_LOAD": "true"},
    ):
        config = load_config("prepdir", quiet=True)
        assert config.get("exclude.directories", []) == []
        assert any("No home config found at" in record.message for record in clean_logger.handlers[-1].records)
        assert any("No local config found at" in record.message for record in clean_logger.handlers[-1].records)


def test_version_load_failure(clean_logger):
    """Test version load failure in config.py (lines 15-16)."""
    with patch("importlib.metadata.version", side_effect=Exception("Version load failed")):
        import importlib
        import sys

        if "prepdir.config" in sys.modules:
            del sys.modules["prepdir.config"]
        import prepdir.config

        assert prepdir.config.__version__ == "0.0.0"
        assert any("Failed to load package version" in record.message for record in clean_logger.handlers[-1].records)


def test_is_resource_exception(clean_logger):
    """Test is_resource exception handling (line 47)."""
    with patch("importlib.resources.files", side_effect=TypeError("Invalid resource")):
        assert not is_resource("prepdir", "config.yaml")


def test_load_config_debug_log(clean_cwd, clean_logger):
    """Test load_config debug log (line 129)."""
    with patch.dict(os.environ, {"PREPDIR_SKIP_CONFIG_FILE_LOAD": "true", "PREPDIR_SKIP_BUNDLED_CONFIG_LOAD": "true"}):
        config = load_config("prepdir", quiet=True)
        assert any(
            "Loading config with namespace='prepdir'" in record.message for record in clean_logger.handlers[-1].records
        )
