from nicegui import ui

class App:
    def __init__(self, title='SoutyUI App'):
        self.title = title
        self.pages = {}

    def page(self, path):
        def decorator(func):
            self.pages[path] = func
            ui.page(path)(func)
            return func
        return decorator

    def run(self):
        ui.run(title=self.title)