#!/usr/bin/env python3
"""Utility functions"""

import shutil
import os
from pathlib import Path
from importlib import util as import_util
import logging

LOGGER = logging.getLogger(__name__)


def get_packaged_config_dir():
    """
    Returns the path to the packaged config directory
    """
    spec = import_util.find_spec("tanat_cli_preset")

    if not spec or not spec.origin:
        raise ImportError("Package tanat_cli_preset not found")

    package_path = Path(spec.origin).parent
    config_path = package_path / "config"

    if not config_path.exists():
        raise ImportError("Config directory not found")

    return config_path


def copy_preset(dest, exist_ok=True, makedirs=True):
    """Copy package preset to destination while preserving directory structure"""
    src = get_packaged_config_dir()

    for root, _, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, relative_path)

        if makedirs:
            os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            if not exist_ok and os.path.exists(dest_file):
                raise FileExistsError(
                    f"File already exists: {dest_file}. "
                    "Use --exist-ok to overwrite existing files"
                )

            shutil.copy2(src_file, dest_file)
    LOGGER.info("Preset copied to %s", dest)
    return 0
