import io
import string
import subprocess
from contextlib import redirect_stdout
from pathlib import Path

from serato_tools.crate import Crate

from crate_picker import pick_crates

EXCLUDED_CRATES = {"recorded"}  # lowercase for case-insensitive comparison


def get_crate_paths() -> list[str]:
    """Return crate names from the local Serato library, e.g. 'Bodiem666%%#UKG%%2-Step'."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        Crate.list_dir()

    paths = []
    for line in buf.getvalue().splitlines():
        if not (line := line.strip()):
            continue
        name = Path(line).stem
        if name.lower() not in EXCLUDED_CRATES:
            paths.append(name)
    return paths


def to_matchers(crate_paths: list[str]) -> list[str]:
    """A parent's matcher also matches its subcrates, since their names contain it."""
    return [f"*{p.replace('%%', ' ')}*" for p in crate_paths]


def validate_drive(letter: str) -> str:
    """Uppercase and verify the drive exists, listing available drives if not."""
    letter = letter.upper()
    if not Path(f"{letter}:\\").exists():
        available = [l for l in string.ascii_uppercase if Path(f"{l}:\\").exists()]
        raise SystemExit(f"Drive {letter}: not found. Available drives: {', '.join(available)}")
    return letter


def run_export(drive: str, root_crate: str, crate_paths: list[str]) -> None:
    cmd = ["serato_usb_export", "--drive", drive, "--crate_matcher", *to_matchers(crate_paths),
           f"--root_crate={root_crate}"]

    print("\nRunning command:")
    print(" ".join(cmd), "\n")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    selected = pick_crates(get_crate_paths())
    if selected is None:
        raise SystemExit("Cancelled.")
    if not selected:
        raise SystemExit("No crates selected.")

    print("Exporting:", *(f"  {p.replace('%%', ' > ')}" for p in selected), sep="\n")

    while not (root_crate := input("\nRoot crate name (required): ").strip()):
        print("Please enter a non-empty root crate name.")

    drive = validate_drive(input("USB drive letter (default: D): ").strip() or "D")
    run_export(drive=drive, root_crate=root_crate, crate_paths=selected)