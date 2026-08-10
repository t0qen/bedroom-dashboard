from machine import Pin6
class Button:
    def __init__(self, pin, callback):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)