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

1. Reads all available `.crate` files from your Serato library
2. Filters out unwanted crates (e.g. `*Recorded*`).
3. Runs `serato_usb_export` with the selected crates, exporting them to your USB drive.

## Usage

1. Run the script:

```bash
python export.py
```

2. Enter the root crate name when prompted (required).
3. Enter the USB drive letter when prompted (press Enter for `d`).

The script prints the command it runs and reports when the `_Serato_` folder has been copied.

## Notes


Notes
-----

- The script **excludes** the crate `*Recorded*` automatically.
- You can add more filters in the `format_crates()` function if needed (e.g. to skip `*Serato Stems*`).
