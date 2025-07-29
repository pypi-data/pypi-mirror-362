# A Terminal Calendar Task App: TasCal

A lightweight terminal-based calendar app for writing and managing date-specific notes — powered by Python's `curses` module.

No mouse. No cloud. No distractions.

---

## Features

- Interactive calendar interface (arrow key navigation)
- Add multiple notes to any date
- Modify or delete individual notes
- Past dates are locked (read-only)
- Local-only data storage (`notes.json`)
- Runs in any Unix-like terminal (Linux, macOS, WSL, SSH, etc.)

---

## Why?

Most calendar and notes apps are over-engineered, visually bloated, and tethered to cloud ecosystems. This app is:

- Minimal
- Private
- Fast
- Ideal for developers, sysadmins, and minimalists

Use it in your terminal. On your laptop. On your server. On your Raspberry Pi.

---

## How It Works

- Notes are stored per date in `notes.json`
- You can add, modify, and delete individual notes
- Each date can contain **multiple notes**
- Terminal UI highlights today and the selected day

### Controls

| Key        | Action                          |
|------------|---------------------------------|
| Arrow keys | Navigate the calendar           |
| `a`        | Add a note to selected date     |
| `m`        | Modify a specific note          |
| `d`        | Delete a specific note          |
| `q`        | Quit the app                    |

---

## Installation

### 1. Pip

```bash
pip install tascal
```

### 2. (Optional) GitHub Repo 

```bash
git clone https://github.com/bearenbey/tascal.git
cd tascal/tascal
python3 cli.py

# or

git clone https://github.com/bearenbey/tascal.git
cd tascal
pip install .
```
---

## Data Format

All notes are saved in a local `notes.json` file in this format:

```json
{
  "2025-07-02": ["Doctor at 10am", "Lunch with Sam"],
  "2025-07-05": ["Send invoices"]
}
```

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
