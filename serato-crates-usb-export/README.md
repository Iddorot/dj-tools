# Serato Crate Export Script

This script exports selected Serato crates to a USB drive using `serato_tools` and the `serato_usb_export` CLI, then copies the entire `_Serato_` folder to the same drive.

## Requirements

- Python 3.8+
- serato-tools (for crate handling)
- serato-usb-export (the CLI tool)

Install them with:

```bash
pip install serato-tools serato-usb-export
```

## What the script does

1. Reads all available `.crate` files from your Serato library (`Crate.list_dir()`).
2. Formats crate names into `*Crate Name*` format expected by `serato_usb_export`.
3. Filters out unwanted crates (e.g. `*Recorded*`).
4. Runs `serato_usb_export` with the selected crates, exporting them to your USB drive.
5. Copies the `_Serato_` folder from your user profile to the USB drive, replacing any existing copy.

## Usage

1. Run the script:

```bash
python export.py
```

2. Enter the root crate name when prompted (required).
3. Enter the USB drive letter when prompted (press Enter for `d`).

The script prints the command it runs and reports when the `_Serato_` folder has been copied.

## Notes

- The script excludes the crate `*Recorded*` automatically.
- To hard‑code defaults instead of interactive prompts, modify the `if __name__ == "__main__"` block.
