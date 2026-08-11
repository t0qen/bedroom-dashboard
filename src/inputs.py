from machine import Pin
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

        return self.global_state

