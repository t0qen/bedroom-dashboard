import apps, inputs, leds, remote_hack, xiao, buzzer, pot, home_assistant
import time


epaper = xiao.Display()
ha = home_assistant.HomeAssistant(epaper.uart)

led_a = leds.Led(6)
led_b = leds.Led(7)
led_c = leds.Led(8)

button_bck = inputs.Button(3)
button_frw = inputs.Button(4)
button_hme = inputs.Button(2)

remote = remote_hack.Remote(18, 20, 21, 19)

buzz = buzzer.Buzzer(5)

led_rgb = leds.RGBLed(11, 13, 12)

pot_a = pot.Pot(26)
pot_b = pot.Pot(27)


def clean():
    led_a.off()
    led_b.off()
    led_c.off()
    led_rgb.off()

def test():
    led_rgb.set_color(100,0, 0)
    time.sleep(1)
    led_rgb.set_color(0,100, 0)
    time.sleep(1)
    led_rgb.set_color(0, 0, 100)
    time.sleep(1)
    led_rgb.set_color(50, 50, 50)
    time.sleep(1)
    led_rgb.off()

    led_a.on()
    time.sleep(1)
    led_b.on()
    time.sleep(1)
    led_c.on()
    time.sleep(1)
    led_a.off()
    led_b.off()
    led_c.off()

    

    i = 0
    while i < 200:
        print("pot a: " + str(pot_a.read()))
        print("pot b: " + str(pot_b.read()))
        i += 1
        time.sleep(0.1)

    i = 0
    while i < 200:
        now = time.ticks_ms()
        print("btn back: " + str(button_bck.is_pressed(now)))
        print("btn frw: " + str(button_frw.is_pressed(now)))
        print("btn home: " + str(button_hme.is_pressed(now)))
        i += 1
        time.sleep(0.1)

    
    remote.press("c")
    epaper.show_image("logo")

    buzz.bip()

test()

try:
    while True:
        time.sleep(0.01)
        now = time.ticks_ms()

        buzz.update(now)
        epaper.update(now)
        remote.update(now)

except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()

