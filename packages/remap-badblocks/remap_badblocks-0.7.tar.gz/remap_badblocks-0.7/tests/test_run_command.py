import contextlib
import io
import tempfile
import threading
from time import sleep, time
from typing import Iterable, Optional, Union

import pytest

from remap_badblocks.src.utils._run_command import (pipe_lines_to_file,
                                                    run_command_realtime)


def test_run_command_realtime_success():
    """Test run_command_realtime with a successful command."""
    cmd = ["echo", "hello world"]
    output = list(run_command_realtime(cmd))
    assert output == ["hello world"]


def test_run_command_realtime_failure():
    """Test run_command_realtime with a failing command."""
    cmd = ["false"]  # `false` is a command that always exits with a non-zero status
    with pytest.raises(RuntimeError, match="Command failed with code 1"):
        list(run_command_realtime(cmd))


def test_run_command_is_captured_asyncronously():
    """Test that the command output is captured asynchronously."""
    # cmd writes hello world to stdout one line per second
    cmd = ["bash", "-c", "for i in {1..5}; do echo 'hello world $i'; sleep 1; done"]
    time_start = time()
    output: Iterable[str] = run_command_realtime(cmd)
    time_launched = time()

    assert time_launched - time_start < 1, "Command should be launched immediately"
    # Check that the output is captured asynchronously
    for i, line in enumerate(output):
        assert line.startswith("hello world")
        assert (
            time() - time_launched < i + 1
        ), "Output should be captured asynchronously"

    assert time() - time_start > 5, "Command should take at least 5 seconds to complete"


@pytest.mark.parametrize(
    "lines, expected_output",
    [
        ([12345, 67890, 54321, "prova"], "12345\n67890\n54321\nprova\n"),  # Normal case
        (
            ["0 6 linear /dev/sda 0", "6 6 linear /dev/sda 10"],
            "0 6 linear /dev/sda 0\n6 6 linear /dev/sda 10\n",
        ),  # DM table case
        ([""], "\n"),  # Empty input
        ([], ""),  # Empty list
    ],
)
def test_pipe_lines_to_file(lines: list[Union[str, int]], expected_output: str):
    # Create a temporary file for testing
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name

    # Save lines to the temporary file
    pipe_lines_to_file(lines, temp_file_name)

    # Read the contents of the file and check if it matches the expected output
    with open(temp_file_name, "r") as f:
        content = f.read()
        assert content == expected_output

    # Clean up the temporary file
    temp_file.close()


@pytest.mark.parametrize(
    "test_iter",
    [
        range(10),
        ["a", "b", "1234567", "prova"],
        "aeiou",
    ],
)
def test_pipe_lines_to_file_writes_realtime(test_iter: Iterable[Union[str, int]]):
    def generator(path: str):
        for i in test_iter:
            yield i
            sleep(0.5)
            with open(path, "r") as f:
                txt = f.read()
            assert str(i) in txt

    temp_file = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = temp_file.name

    lines = generator(temp_file_name)

    pipe_lines_to_file(lines, temp_file_name)

    temp_file.close()


def test_run_command_realtime_no_deadlock_with_lots_of_output():
    # This script prints lots of lines to both stdout and stderr very quickly
    # it fails if it times out

    result: dict[str, str] = {}

    def test_logic():
        test_cmd = [
            "python3",
            "-c",
            (
                "import sys\n"
                "for i in range(1000000):\n"
                "    print(f'stdout {i}')\n"
                "    print(f'stderr {i}', file=sys.stderr)"
            ),
        ]

        # redirect stderr to a local variable
        # to avoid printing to the console
        stderr_capture = io.StringIO()

        with contextlib.redirect_stderr(stderr_capture):
            stdout = "\n".join(run_command_realtime(test_cmd))
            stderr = stderr_capture.getvalue()

        result["stdout"] = stdout
        result["stderr"] = stderr

    # Run the test logic in a separate thread
    thread = threading.Thread(target=test_logic)
    thread.start()
    thread.join(timeout=5)  # Wait for the thread to finish

    assert not thread.is_alive(), "Thread should finish within 5 seconds"

    stdout, stderr = result["stdout"], result["stderr"]

    assert len(stdout) > 70000  # 64K is the average OS pipe size
    assert "stdout" in stdout
    assert "stderr" not in stdout
    assert len(stderr) > 70000  # 64K is the average OS pipe size
    assert "stderr" in stderr
    assert "stdout" not in stderr


@pytest.mark.parametrize(
    "stdin,command,expected_out",
    [
        ("Test string\nTest string", ["cat"], "Test string\nTest string"),
        ("Test string", ["cat"], "Test string"),
        ("Test string\n", ["cat"], "Test string"),
        ("a\n1\nb\n2\nc", ["grep", "b"], "b"),
        ("a\n1\nb\n2\nc", ["grep", "\\d"], "1\n2"),
    ],
)
def test_run_command_realtime_stdin(stdin: str, command: list[str], expected_out: str):
    out = "\n".join(run_command_realtime(command, stdin=stdin))
    assert out == expected_out


@pytest.mark.parametrize(
    "stdin,command",
    [
        ("", ["cat"]),
        (None, ["echo"]),
    ],
)
def test_run_command_realtime_deadlock_with_empty_stdout(
    stdin: Optional[str], command: list[str]
):
    o = list(run_command_realtime(command, stdin=stdin))

    assert (not o) or (o[0] == "")
