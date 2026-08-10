from machine import Pin, PWM

class RGB_led:
    def __init__(self, pin_r, pin_g, pin_b):
        self.led_r = PWM(Pin(pin_r))
        self.led_r.freq(5000)
        self.led_g = PWM(Pin(pin_g))
        self.led_g.freq(5000)
        self.led_b = PWM(Pin(pin_b))
        self.led_b.freq(5000)

    def update(self, r, g, b):
        self.led_r.duty_u16(r)
        self.led_g.duty_u16(g)
        self.led_b.duty_u16(b)