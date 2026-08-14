from machine import Pin, PWM


# Source - https://stackoverflow.com/a/70659904
# Posted by CrazyChucky, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-14, License - CC BY-SA 4.0
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


class Led:
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
        self.led_r.duty_u16(map_range(r, 0, 100, 0, 65535))
        self.led_g.duty_u16(map_range(g, 0, 100, 0, 65535))
        self.led_b.duty_u16(map_range(b, 0, 100, 0, 65535))
    
    def off(self):
        self.led_r.duty_u16(0)
        self.led_g.duty_u16(0)
        self.led_b.duty_u16(0)

    def set_mode(self, mode):   
        self.off()
        self.current_mode = mode

    def update(self, current_time):
        if self.current_mode == "think":
            pass
        elif self.current_mode == "waiting": 
            pass
        else:
            pass
