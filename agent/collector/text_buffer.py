class TextBuffer:
    def __init__(self):
        self.buffer = ""

    def add_character(self, character):
        self.buffer += character

    def finish_word(self):
        text = self.buffer
        self.buffer = ""
        return text