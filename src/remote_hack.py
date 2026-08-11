from machine import Pin

class Remote:
    def __init__(self, pin_a, pin_b, pin_c, pin_off):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pin_c = pin_c
        self.pin_off = pin_off

        self.button_a = Pin(self.pin_a, Pin.OUT)
        self.button_b = Pin(self.pin_b, Pin.OUT)
        self.button_c = Pin(self.pin_c, Pin.OUT)
        self.button_off = Pin(self.pin_off, Pin.OUT)

    def press(self, button):
        if button == "a":
            self.button_a.value(1)
            self.button_a.value(0)
        elif button == "b":
            self.button_b.value(1)
            self.button_b.value(0)
        elif button == "c":
            self.button_c.value(1)
            self.button_c.value(0)
        elif button == "off":
            self.button_off.value(1)
            self.button_off.value(0)

    def keep_only(self, button):
        if button == "a":
            self.button_off.value(0)
            self.button_a.value(1)
        elif button == "b":
            self.button_off.value(0)
            self.button_b.value(1)
        elif button == "c":
            self.button_off.value(0)
            self.button_c.value(1)
            