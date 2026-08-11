# example = [
#     "00000000",
#     "00000000",
#     "00000000",
#     "00000000",
#     "00000000",
#     "00000000",
#     "00000000",
#     "00000000"
# ]

class Sprites:
    def __init__(self):
        self.lamps = [
            "00000000",
            "00000000",
            "00100100",
            "10011001",
            "10011001",
            "00100100",
            "00000000",
            "00000000"
        ]

        self.buttons = [
            "00010000",
            "00001000",
            "00000100",
            "10111101",
            "10100001",
            "00010000",
            "00001000",
            "00000100"
        ]


    def get_sprite(self, name):
        if name == "lamps":
            return self.lamps
        elif name == "buttons":
            return self.buttons
        else:
            return None
