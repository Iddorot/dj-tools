# Serato Crate Export Script

This script exports selected Serato crates to a USB drive using `serato_tools` and the `serato_usb_export` CLI. You choose the crates from an interactive tree in the terminal.

## Requirements

- Python 3.9+
- serato-tools (for crate handling)
- serato-usb-export (the CLI tool)
- windows-curses (Windows only, for the crate picker)

Install them with:

```bash
pip install serato-tools serato-usb-export
```

On Windows, also run:

```bash
pip install windows-curses
```

## Files

- `export.py` is the main script.
- `crate_picker.py` is the interactive crate tree. It must sit in the same folder as `export.py`.

## What the script does

1. Reads all available `.crate` files from your Serato library.
2. Filters out unwanted crates (e.g. `Recorded`).
3. Shows your crates as a tree so you can pick which ones to export.
4. Runs `serato_usb_export` with the selected crates, exporting them to your USB drive.

## Usage

1. Run the script:

```bash
python export.py
```

2. Pick your crates in the tree, then press **Enter**.
3. Enter the root crate name when prompted (required).
4. Enter the USB drive letter when prompted (press Enter for `D`).

The script prints the command it runs and reports when the `_Serato_` folder has been copied.

### Crate picker keys

| Key | Action |
| --- | --- |
| ↑ / ↓ (or `k` / `j`) | Move |
| PgUp / PgDn | Jump a page |
| Space | Tick or untick a crate and everything under it |
| → (or `l`) | Expand a crate |
| ← (or `h`) | Collapse a crate, or jump to its parent |
| `a` / `n` | Select all / none |
| `e` / `c` | Expand all / collapse all |
| Enter | Export the selection |
| `q` / Esc | Cancel |

A crate shows `[x]` when it and everything under it are selected, and `[~]` when only some of its subcrates are.

## Notes

- Ticking a parent crate exports all of its subcrates too.
- The script **excludes** the `Recorded` crate automatically.
- To skip more crates (e.g. `Serato Stems`), add their names in lowercase to `EXCLUDED_CRATES` at the top of `export.py`.
- You can try the picker on its own with `python crate_picker.py`. It reads crates from `~/Music/_Serato_/Subcrates` and prints what you selected.