import apps, display, inputs, leds, remote_hack, xiao, buzzer, pot, home_assistant
import time


epaper = xiao.Display()
ha = home_assistant.HomeAssistant(epaper.uart)

epaper.show_image("cat")

led_a = leds.Led(6)
led_b = leds.Led(7)
led_c = leds.Led(8)

remote = remote_hack.Remote(18, 19, 20, 21)

buzz = buzzer.Buzzer(5)

led_rgb = leds.RGBLed(13, 12, 11)

pot_a = pot.Pot(26)
pot_b = pot.Pot(27)

last_brightness_sent = -1

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
        epaper.update(now)

        # --- LOGIQUE HOME ASSISTANT ---
        brightness_pct = pot_a.read()
        
        if abs(brightness_pct - last_brightness_sent) >= 2:
            # L'envoi UART est instantané, ça n'impacte pas la file d'attente de l'écran
            ha.set_brightness(home_assistant.Device.LUMIERE_SALON, brightness_pct)
            last_brightness_sent = brightness_pct
    
except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()

