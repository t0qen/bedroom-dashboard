import apps, display, inputs, leds, remote_hack, xiao, buzzer
import time

epaper = xiao.Display()

led_a = leds.Led(6)
led_b = leds.Led(7)
led_c = leds.Led(8)

buzz = buzzer.Buzzer(5)

led_rgb = leds.RGBLed(13, 12, 11)

def clean():
    led_a.off()
    led_b.off()
    led_c.off()
    led_rgb.off()

buzz.bip()

try:
    while True:
        time.sleep(0.001)
        now = time.ticks_ms()
        buzz.update(now)

    
except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()

