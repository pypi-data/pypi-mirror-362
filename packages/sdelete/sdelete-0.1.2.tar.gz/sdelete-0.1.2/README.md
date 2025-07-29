# sdelete

A terminal-based Python app to securely delete files and folders — with multi-select, simulation mode, overwrite-before-delete logic, and hidden file toggle. Built with `ncurses` for minimal UI and maximum control.

---

## Features

- Terminal UI with scrollable file browser  
- Secure deletion: overwrites files with random data before removal  
- Multi-select with `SPACE`  
- Hidden file toggle with `h`  
- Simulation mode (dry run without deleting anything)  
- Logs every action (`deleted_files.log`)  
- Root checks for protected paths like `/`, `/root`, `/etc`

---

## Installation

Install via `pip`:

```bash
pip install sdelete
```

Or GitHub:

```bash
git clone https://github.com/bearenbey/sdelete.git
cd sdelete
pip install .
```

---

## Usage

```bash
sdelete
```

This opens a terminal UI starting in your home directory.

---

## Key Bindings

| Key        | Action                             |
|------------|------------------------------------|
| `↑ / ↓`    | Navigate up and down               |
| `ENTER`    | Enter directory                    |
| `SPACE`    | Select/deselect item               |
| `d`        | Delete selected (or simulate)      |
| `h`        | Toggle hidden files (dotfiles)     |
| `q`        | Quit                               |

When pressing `d`, you'll be asked whether to run in simulation mode. If you say "yes", it will preview all deletion actions without modifying any files. A scrollable log is shown.

---

## How It Works

- Selected files are securely overwritten using three passes of random data.
- Files are deleted afterward.
- Directories are recursively deleted if empty.
- System paths like `/`, `/root`, `/etc` are protected unless running as root.
- All actions (real or simulated) are logged to `deleted_files.log`.

---

## When to Use It

- Cleaning up local environments (e.g. `.env`, API keys, temp logs)
- Securely deleting before archiving or transferring systems
- Gaining visibility before removing deeply nested files or folders
- Practicing cautious cleanup in CI, devops, or personal scripts

---

## Requirements

- Python 3.8+
- Unix/macOS terminal with `curses` support

---

## Notes

This project does not use external binaries like `shred` or `srm`.  
It is written in pure Python for portability and safety.

---

## License

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.

You should have received a copy of the GNU General Public License  
along with this program. If not, see <https://www.gnu.org/licenses/>.

© 2025 Eren Öğrül [termapp@pm.me](mailto:termapp@pm.me)