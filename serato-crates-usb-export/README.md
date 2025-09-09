Serato Crate Export Script
==========================

This script automates exporting selected Serato crates to a USB drive using `serato_tools` and the `serato_usb_export` CLI.

Requirements
------------

- Python 3.8+
- serato-tools (for crate handling)
- serato-usb-export (the CLI tool)

Install them with:

    pip install serato-tools serato-usb-export

What the script does
--------------------

1. Reads all available `.crate` files from your Serato library (`Crate.list_dir()`).
2. Formats crate names into `*Crate Name*` format expected by `serato_usb_export`.
3. Filters out unwanted crates (e.g. `*Recorded*`).
4. Runs `serato_usb_export` with the selected crates, exporting them to your USB drive.

Example command generated:

    serato_usb_export --drive d --crate_matcher *Bassline* *Techno Acid* *Techno High* ... --root_crate="Ido's Music"

Usage
-----

1. Save the script as `export.py` (or whatever name you prefer).
2. Plug in your USB drive (e.g. `D:`).
3. Run the script from PowerShell or CMD:

    python export.py

By default:
- USB drive is `d`
- Root crate is `"Ido's Music"`

Customization
-------------

You can change the defaults at the bottom of the script:

    if __name__ == "__main__":
        run_export(drive="e", root_crate="My USB Crate")

- Change `drive="d"` to match your USB drive letter.
- Change `root_crate="Ido's Music"` to your preferred root crate name.

Notes
-----

- The script **excludes** the crate `*Recorded*` automatically.
- You can add more filters in the `format_crates()` function if needed (e.g. to skip `*Serato Stems*`).
