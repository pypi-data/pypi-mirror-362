import os
import sys

from .config_parser import Config
from .config_writer import write_config
from types import SimpleNamespace
from typing import Optional, List

__all__ = ["parse_config", "write_config"]

def parse_config(config_paths: Optional[List[str]] = None) -> SimpleNamespace:
    """Retrieve the application configuration, including YAML, JSON, TOML, and .env content.

    Args:
        config_paths: Optional list of paths to project-specific config files.

    Returns:
        SimpleNamespace: A namespace object with config and env values accessible via dot notation.
    """
    if getattr(sys, 'frozen', False):
        # If running as an EXE
        run_dir = os.path.dirname(sys.executable)

        # Change directory to executable root.
        os.chdir(run_dir)

    if config_paths:
        Config().reload(config_paths)

    return Config().get()
