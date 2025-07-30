import subprocess
import sys
import threading
from pathlib import Path
from typing import IO, Iterable, Optional, Protocol, Union


class Stringifyiable(Protocol):
    """Protocol for objects that can be converted to a string."""

    def __str__(self) -> str:
        """Return the string representation of the object."""
        ...


def pipe_stderr_to_stream(pipe: IO[str], stream: IO[str]) -> None:
    for line in pipe:
        print(f"[stderr] {line.strip()}", file=stream)


def run_command_realtime(cmd: list[str], stdin: Optional[str] = None) -> Iterable[str]:
    """Run a command and yield its output line by line in real-time."""
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
    ) as process:
        if process.stdout is None:
            raise RuntimeError("Failed to capture stdout from the command.")

        if stdin is not None:
            if process.stdin is None:
                raise RuntimeError("Failed to pass stdin to command.")
            else:
                if not stdin.endswith("\n"):
                    stdin += "\n"
                process.stdin.write(stdin)
                process.stdin.close()

        # Start background stderr reader
        stderr_thread: Optional[threading.Thread] = None
        if process.stderr is not None:
            stderr_thread = threading.Thread(
                target=pipe_stderr_to_stream, args=(process.stderr, sys.stderr)
            )
            stderr_thread.start()

        for line in process.stdout:
            yield line.strip()

        process.wait()
        if stderr_thread is not None:
            stderr_thread.join()

        if process.returncode != 0:
            # Capture stderr if needed
            raise RuntimeError(f"Command failed with code {process.returncode}")


def pipe_lines_to_file(
    lines: Iterable[Stringifyiable], output_file: Union[str, Path, IO[str]]
) -> None:
    """Save the lines to the specified output file in real-time."""
    f: Optional[IO[str]] = None
    try:
        if not isinstance(output_file, IO):
            f = open(output_file, "w")
            output_file = f
        for line in lines:
            output_file.write(str(line) + "\n")
            output_file.flush()  # Ensure the content is written to the file immediately
    finally:
        if f is not None:
            f.close()
