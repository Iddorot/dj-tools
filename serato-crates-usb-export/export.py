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

    cmd = [
        "serato_usb_export",
        "--drive", drive,
        "--crate_matcher",
    ] + crates + [f'--root_crate={root_crate}']

    print("\nRunning command:")
    print(" ".join(cmd), "\n")

    subprocess.run(cmd, check=True)

def copy_serato_folder(drive):
    # Build C:\Users\[Your Username]\Music\_Serato_ explicitly
    username = os.environ.get("USERNAME") or Path.home().name
    serato_folder = Path(f"C:/Users/{username}/Music/_Serato_")

    if not serato_folder.exists():
        print(f"❌ Could not find Serato folder at {serato_folder}")
        return

    # Validate USB root
    usb_root = Path(f"{drive.upper()}:\\")
    if not usb_root.exists():
        print(f"❌ Drive {usb_root} not found. Check the letter and try again.")
        return

    dest = usb_root / "_Serato_"
    print(f"Copying {serato_folder} → {dest} ...")

    # Replace existing copy on the USB
    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(serato_folder, dest)
    print("✅ Serato folder copied successfully.")

if __name__ == "__main__":
    # Root crate name is REQUIRED
    root_crate = input("What is the root crate name? (required): ").strip()
    if not root_crate:
        print("❌ Root crate name is required. Exiting.")
        raise SystemExit(1)

    # USB drive with default
    drive = input("Where is your USB drive? (default: d): ").strip() or "d"

    # 1) Export crates to USB
    run_export(drive=drive, root_crate=root_crate)

    # 2) Copy _Serato_ folder to USB
    copy_serato_folder(drive)
