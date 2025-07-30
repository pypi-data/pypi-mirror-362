class Button:
    def __init__(self, text):
        self.text = text
    
    def __call__(self, func):
        self.func = func