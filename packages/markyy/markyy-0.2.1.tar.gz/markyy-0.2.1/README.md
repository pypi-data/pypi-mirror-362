# Marky

Marky is a minimal terminal-based Markdown editor built with Python 3 and `ncurses`. It offers a clean editing experience with live syntax highlighting, autosave, and in-terminal search — all inside your terminal window.

---

## Features

- Markdown syntax highlighting (headers, bold, italic, code, lists, links, etc.)
- Live character count in the footer
- Header/footer UI with consistent styling
- Autosave every 30 seconds with a `.bak` backup file
- Flash message confirmation after autosave
- In-editor search (`Ctrl+F`) with next (`Ctrl+N`) and previous (`Ctrl+P`) navigation
- Safe cursor and rendering logic (handles terminal resizing and wide characters)

---

## ⌨️ Keybindings

| Key Combo   | Action               |
|------------|----------------------|
| `Ctrl+S`   | Save file            |
| `Ctrl+F`   | Search               |
| `Ctrl+N`   | Next match           |
| `Ctrl+P`   | Previous match       |
| `Esc`      | Exit editor          |
| Arrow Keys | Navigate cursor      |

---

## Usage

You'll be prompted to enter a filename. If the file exists, it will be loaded. If not, a new file is created.

---

## Installation

### Install via pip

```bash
pip install markyy
```

### Or clone from GitHub

```bash
git clone https://github.com/bearenbey/marky.git
cd marky
pip install .
markyy
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

