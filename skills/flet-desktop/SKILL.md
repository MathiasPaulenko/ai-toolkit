---
name: flet-desktop
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Desktop application development with Flet (Flutter-based Python). Covers UI layout, state management, navigation, file handling, packaging, and cross-platform distribution.
tags: [flet, python, desktop, flutter, gui, cross-platform, pyinstaller]
role: desktop-developer
model: any
trigger: When the user mentions Flet, desktop Python apps, Flutter Python, cross-platform GUI, or PyInstaller packaging.
---

# Flet Desktop

## 1. Project Setup

```bash
pip install flet
# For desktop packaging
pip install pyinstaller
```

```python
# main.py
import flet as ft

def main(page: ft.Page):
    page.title = "My Flet App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def on_click(e):
        page.add(ft.Text(f"Hello, {name_field.value}!"))

    name_field = ft.TextField(label="Your name", width=300)
    submit_btn = ft.ElevatedButton("Greet", on_click=on_click)

    page.add(
        ft.Column([
            ft.Text("Welcome", size=30, weight=ft.FontWeight.BOLD),
            name_field,
            submit_btn,
        ])
    )

ft.app(target=main)
```

## 2. Layout Widgets

| Widget | Purpose |
|--------|---------|
| `Row` | Horizontal layout |
| `Column` | Vertical layout |
| `Container` | Box with padding, margin, border |
| `Card` | Material card with elevation |
| `Tabs` | Tabbed navigation |
| `NavigationBar` | Bottom navigation |
| `ResponsiveRow` | Grid-based responsive layout |

```python
ft.ResponsiveRow([
    ft.Column([ft.Text("Sidebar")], col={"sm": 12, "md": 3}),
    ft.Column([ft.Text("Main")], col={"sm": 12, "md": 9}),
])
```

## 3. State Management

### Simple State (page-level)

```python
def main(page: ft.Page):
    counter = ft.Text("0", size=40)

    def increment(e):
        counter.value = str(int(counter.value) + 1)
        page.update()

    page.add(counter, ft.ElevatedButton("+", on_click=increment))
```

### Complex State (separate class)

```python
class AppState:
    def __init__(self):
        self.users = []
        self.selected_user = None

    def add_user(self, name: str):
        self.users.append({"id": len(self.users) + 1, "name": name})
```

## 4. Navigation

```python
from flet import Page, View, AppBar, ElevatedButton, Text

def main(page: Page):
    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [AppBar(title=Text("Home")),
                 ElevatedButton("Go to settings", on_click=lambda _: page.go("/settings"))]
            )
        )
        if page.route == "/settings":
            page.views.append(
                View(
                    "/settings",
                    [AppBar(title=Text("Settings")),
                     ElevatedButton("Back", on_click=lambda _: page.go("/"))]
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
```

## 5. File Handling

### File Picker

```python
import flet as ft
from flet import FilePicker, FilePickerResultEvent

def main(page: ft.Page):
    pick_files_dialog = FilePicker(on_result=lambda e: handle_files(e))
    page.overlay.append(pick_files_dialog)

    def handle_files(e: FilePickerResultEvent):
        if e.files:
            for f in e.files:
                page.add(ft.Text(f"Selected: {f.name} ({f.path})"))

    page.add(
        ft.ElevatedButton(
            "Pick files",
            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True)
        )
    )
```

### Save File

```python
save_dialog = FilePicker(on_result=lambda e: ...)
save_dialog.save_file(file_name="report.pdf")
```

## 6. Data Tables

```python
ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Name")),
        ft.DataColumn(ft.Text("Age"), numeric=True),
        ft.DataColumn(ft.Text("Role")),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Alice")),
                ft.DataCell(ft.Text("30")),
                ft.DataCell(ft.Text("Admin")),
            ]
        ),
    ],
)
```

## 7. Packaging

### PyInstaller (Windows/macOS/Linux)

```bash
pyinstaller --onefile --windowed main.py
```

### Flet Pack (Recommended)

```bash
flet pack main.py --name MyApp --icon icon.png
```

Options:
- `--name` — application name
- `--icon` — `.png` or `.ico`
- `--distpath` — output directory
- `--add-data` — bundle additional files

### macOS App Bundle

```bash
flet pack main.py --name MyApp --bundle-id com.example.myapp
```

## 8. Async Operations

```python
import asyncio
import aiohttp
import flet as ft

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def main(page: ft.Page):
    async def load_data(e):
        status.value = "Loading..."
        page.update()
        data = await fetch_data("https://api.example.com/data")
        status.value = f"Loaded {len(data)} items"
        page.update()

    status = ft.Text("Ready")
    page.add(status, ft.ElevatedButton("Load", on_click=load_data))

ft.app(target=main)
```

## 9. Platform-Specific Code

```python
import platform
import os

if platform.system() == "Windows":
    config_dir = os.path.expandvars(r"%LOCALAPPDATA%\MyApp")
elif platform.system() == "Darwin":
    config_dir = os.path.expanduser("~/Library/Application Support/MyApp")
else:
    config_dir = os.path.expanduser("~/.config/myapp")
```

## 10. Best Practices

- Use `page.update()` after state changes.
- Offload heavy work to threads/async to avoid UI freezing.
- Store user preferences in `page.client_storage`.
- Use `ResponsiveRow` for adaptable layouts.
- Test on target OS before release (rendering differences exist).
