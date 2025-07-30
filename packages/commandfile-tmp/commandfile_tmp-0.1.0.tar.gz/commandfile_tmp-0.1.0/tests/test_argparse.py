from pathlib import Path

import pytest

from commandfile.argparse import CommandfileArgumentParser
from commandfile.io import write_cmdfile_yaml
from commandfile.model import Commandfile, Filelist, Parameter


@pytest.fixture
def commandfile_path(tmp_path: Path):
    return tmp_path / "commandfile.yaml"


def test_standard_arguments():
    parser = CommandfileArgumentParser()
    parser.add_argument("--some-arg", type=int)
    args = parser.parse_args(["--some-arg", "42"])
    assert args.some_arg == 42


def test_commandfile_parameter(commandfile_path: Path):
    cmdfile = Commandfile(
        header={},
        parameters=[Parameter(key="some-arg", value="42")],
        inputs=[],
        outputs=[],
    )
    write_cmdfile_yaml(cmdfile, commandfile_path)
    parser = CommandfileArgumentParser()
    parser.add_argument("--some-arg", type=int)
    args = parser.parse_args(["--commandfile", str(commandfile_path)])
    assert args.some_arg == 42


def test_commandfile_parameter_override(commandfile_path: Path):
    cmdfile = Commandfile(
        header={},
        parameters=[Parameter(key="some-arg", value="42")],
        inputs=[],
        outputs=[],
    )
    write_cmdfile_yaml(cmdfile, commandfile_path)
    parser = CommandfileArgumentParser()
    parser.add_argument("--some-arg", type=int)
    args = parser.parse_args(
        ["--commandfile", str(commandfile_path), "--some-arg", "100"]
    )
    assert args.some_arg == 100


def test_commandfile_filelist(commandfile_path: Path):
    cmdfile = Commandfile(
        header={},
        parameters=[],
        inputs=[
            Filelist(
                key="some-file-input",
                files=["file1.txt", "file2.txt"],
            ),
        ],
        outputs=[],
    )
    write_cmdfile_yaml(cmdfile, commandfile_path)
    parser = CommandfileArgumentParser()
    parser.add_argument("--some-file-input", type=str, nargs="+")
    args = parser.parse_args(["--commandfile", str(commandfile_path)])
    assert args.some_file_input == ["file1.txt", "file2.txt"]


def test_commandfile_empty_filelist(commandfile_path: Path):
    cmdfile = Commandfile(
        header={},
        parameters=[],
        inputs=[
            Filelist(
                key="some-file-input",
                files=[],
            ),
        ],
        outputs=[],
    )
    write_cmdfile_yaml(cmdfile, commandfile_path)
    parser = CommandfileArgumentParser()
    parser.add_argument("--some-file-input", type=str, nargs="*")
    args = parser.parse_args(["--commandfile", str(commandfile_path)])
    assert args.some_file_input == []
