from nicegui import ui

class Button:
    def __init__(self, label, on_click=None):
        self.button = ui.button(label)
        if on_click:
            self.button.on('click', on_click)

    def set_label(self, label):
        self.button.text = label

    def on_click(self, callback):
        self.button.on('click', callback)

class Text:
    def __init__(self, content, size='md', color='default'):
        size_map = {'sm': 'small', 'md': 'medium', 'lg': 'large', 'xl': 'xlarge'}
        css_size = size_map.get(size, 'medium')
        css_color = color if color != 'default' else 'black'
        self.label = ui.label(content).classes(f'text-{css_size} text-{css_color}')