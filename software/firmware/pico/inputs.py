from machine import Pin, ADC
from time import ticks_ms

class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

        self.stable_state = False
        self.last_state = False
        self.debounce_time = 50
        self.last_change_time = 0
        self.global_state = None

    def is_pressed(self, time):
        read_state = not self.pin.value()
        if read_state != self.last_state:
            self.last_change_time = ticks_ms()
            self.last_state = read_state
        elif (time - self.last_change_time) >= self.debounce_time:
            if self.last_state != self.stable_state:
                self.stable_state = self.last_state
                if self.stable_state:
                    self.global_state = "PRESSED"
                else:
                    self.global_state = "RELEASED"
        if self.global_state is not None:
            state = self.global_state
            self.global_state = None
            return state
        
        return None

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Pot:
    def __init__(self, pin):
        self.pot = ADC(pin)

    def read(self):
        self.result = int(map_range(self.pot.read_u16(), 50, 65300, 0, 100))
        
        if self.result < 0:
            self.result = 0
        if self.result > 100:
            self.result = 100
        return self.result
    
    def read_raw(self):
        return self.pot.read_u16()

