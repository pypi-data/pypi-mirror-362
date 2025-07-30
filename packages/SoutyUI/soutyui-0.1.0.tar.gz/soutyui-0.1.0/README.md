# SoutyUI

A futuristic UI framework for Python — simpler and more fun than PyQt and NiceGUI.

## Example

```python
import SoutyUI as ui

app = ui.App(title="Souty Demo")

@ui.app.page("/")
def home():
    ui.Text("Welcome to SoutyUI", size="xl", color="primary")
    ui.Button("Click Me!", on_click=lambda: print("You clicked it!"))

ui.app.run()
```
