from machine import ADC, Pin

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Pot:
    def __init__(self, pin):
        self.pot = ADC(pin)

    def read(self):
        self.result = int(map_range(self.pot.read_u16(), 50, 65535, 0, 100))
        if self.result < 0:
            self.result = 0
        if self.result > 100:
            self.result = 100
        return self.result