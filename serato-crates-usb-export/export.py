import os
import io
import shutil
import subprocess
from pathlib import Path
from contextlib import redirect_stdout
from serato_tools.crate import Crate


def get_crate_paths():
    buf = io.StringIO()
    with redirect_stdout(buf):
        Crate.list_dir()  # prints paths, returns None
    out = buf.getvalue().strip()
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def format_crates():
    formatted = []
    for path in get_crate_paths():
        name = os.path.basename(path)
        if name.endswith(".crate"):
            name = name[:-6]
        name = name.replace("%%", " ")
        formatted.append(f"*{name}*")
    # filter out Recorded
    return [c for c in formatted if c.lower() != "*recorded*"]


def run_export(drive, root_crate):
    crates = format_crates()

    # Build the command arguments (no quotes in actual args)
    cmd = (
        [
            "serato_usb_export",
            "--drive",
            drive,
            "--crate_matcher",
        ]
        + crates
        + [f"--root_crate={root_crate}"]
    )

    # Print a shell-like representation with root_crate wrapped in quotes
    print("\nRunning command:")
    display_cmd = (
        [
            "serato_usb_export",
            "--drive",
            drive,
            "--crate_matcher",
        ]
        + crates
        + [f'--root_crate="{root_crate}"']
    )
    print(" ".join(display_cmd), "\n")

    # Execute the command
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    # Root crate name is REQUIRED; keep prompting until provided
    while True:
        root_crate = input("What is the root crate name? (required): ").strip()
        if root_crate:
            break
        print("Please enter a non-empty root crate name.")

    # USB drive with default
    drive = input("Where is your USB drive? (default: d): ").strip() or "d"

    run_export(drive=drive, root_crate=root_crate)
