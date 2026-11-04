class App:
    def __init__(self, name):
        self.name = name
        self.current_state = "START"

    def start(self):
        pass

    def get_events(self, event):
        pass

    def update(self, millis):
        pass

    def draw(self, display):
        pass

class Menu(App):
    def __init__(self, list):
        super().__init__("Menu")
        self.apps = list
        self.current_state = "START"