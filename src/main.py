import apps, display, inputs, leds, remote_hack, xiao, buzzer, pot
import time

epaper = xiao.Display()

led_a = leds.Led(6)
led_b = leds.Led(7)
led_c = leds.Led(8)

buzz = buzzer.Buzzer(5)

led_rgb = leds.RGBLed(13, 12, 11)

pot_a = pot.Pot(26)
pot_b = pot.Pot(27)

def clean():
    led_a.off()
    led_b.off()
    led_c.off()
    led_rgb.off()


try:
    while True:
        time.sleep(0.01)
        now = time.ticks_ms()

        print("a: " + str(pot_a.read()))
        print("b: " + str(pot_b.read()))

        buzz.update(now)

    
except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()

