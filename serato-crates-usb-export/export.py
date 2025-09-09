import os
import io
import subprocess
from contextlib import redirect_stdout
from serato_tools.crate import Crate

def get_crate_paths():
    buf = io.StringIO()
    with redirect_stdout(buf):
        Crate.list_dir()
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

def run_export(drive="d", root_crate="Ido's Music"):
    crates = format_crates()

    cmd = [
        "serato_usb_export",
        "--drive", drive,
        "--crate_matcher",
    ] + crates + [f'--root_crate={root_crate}']

    print("Running:", " ".join(cmd))

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    run_export()
