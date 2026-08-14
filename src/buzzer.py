from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))
        self.current_mode = None
        self.mode_started_time = None

    def tone(self, freq, delay):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(30000)
        time.sleep_ms(delay)
        self.buzzer.duty_u16(0)

    def bip(self, freq=3000, delay=500):
        if not self.current_mode:
            print("[buzzer.py] INFO: bip mode requested")
            self.current_mode = ["bip", freq, delay]
        else:
            print("[buzzer.py] WANRING: a mode already started")

    def update(self, current_time):
        if self.current_mode:
            if not self.mode_started_time:
                if self.current_mode[0] == "bip":
                    self.buzzer.freq(self.current_mode[1])
                    self.buzzer.duty_u16(30000)
                    self.mode_started_time = current_time
                    print("[buzzer.py] INFO: bip mode started")
            if self.mode_started_time:
                if current_time - self.mode_started_time  > self.current_mode[2]:
                    print("[buzzer.py] INFO: mode finished")
                    self.buzzer.duty_u16(0)