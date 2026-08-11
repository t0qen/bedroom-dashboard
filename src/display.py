from machine import Pin, SPI
import max7219

class Display:
    def __init__(self):
        self.spi = SPI(
            0,
            baudrate=10000000,
            polarity=1,
            phase=0,
            sck=Pin(2),
            mosi=Pin(3)
        )
        self.cs = Pin(5, Pin.OUT)
        self.display = max7219.Matrix8x8(self.spi, self.cs, 1)
        self.display.brightness(5)
        self.display.fill(0)
        self.display.show()

    def clear(self):
        self.display.fill(0)
        self.display.show()

    def draw_buffer(self, buffer):
        self.display.fill(0)
        for y in range(8):
            for x in range(8):
                if buffer[y][x]:
                    self.display.pixel(x, y, 1)
                else:
                    self.display.pixel(x, y, 0)
        self.display.show()
