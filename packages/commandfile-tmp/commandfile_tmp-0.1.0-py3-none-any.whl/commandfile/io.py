from pathlib import Path

import yaml

from commandfile.model import Commandfile


def write_cmdfile_yaml(cmdfile: Commandfile, path: Path):
    """Write a Commandfile object to a YAML file."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(cmdfile.model_dump(), f)
