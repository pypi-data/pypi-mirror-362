from nicegui import ui

def set_theme(theme):
    if theme in ('light', 'dark'):
        ui.colors(theme=theme)
    else:
        print(f'Theme {theme} not supported.')