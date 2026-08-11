from machine import Pin, PWM

class Leds:
    def __init__(self, pin):
        self.pin = pin
        self.led = Pin(self.pin, Pin.OUT)

    def on(self):
        self.led.value(1)

    def off(self):
        self.led.value(0)

class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.led_r = PWM(Pin(pin_r))
        self.led_r.freq(5000)
        self.led_g = PWM(Pin(pin_g))
        self.led_g.freq(5000)
        self.led_b = PWM(Pin(pin_b))
        self.led_b.freq(5000)

        self.current_mode = None

    def set_color(self, r, g, b):
        self.led_r.duty_u16(r)
        self.led_g.duty_u16(g)
        self.led_b.duty_u16(b)
    
    def off(self):
        self.led_r.duty_u16(0)
        self.led_g.duty_u16(0)
        self.led_b.duty_u16(0)

    def set_mode(self, mode):   
        self.off()
        self.current_mode = mode

    def update(self, time):
        if self.current_mode == "think":
            pass
        elif self.current_mode == "waiting": 
            pass
        else:
            pass
