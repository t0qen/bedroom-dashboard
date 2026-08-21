import time

import buzzer
import home_assistant
import inputs
import leds
import remote_hack
import xiao

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

pot = inputs.Pot(28)
last_pot_value = pot.read()
last_stabilized_pot_value = pot.read()
last_pot_stabilization = time.ticks_ms()


def clean():
    led_a.off()
    led_b.off()
    led_c.off()
    led_rgb.off()


def test():
    led_rgb.set_color(100, 0, 0)
    time.sleep(1)
    led_rgb.set_color(0, 100, 0)
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
        print("pot: " + str(pot.read()))
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
    epaper.show_image("logo", img_r=None)

    buzz.bip()


DISPLAY_TRANSLATION = {  # for matching current global state to what to show on e ink display
    ("MENU", "LIGHTS"): ("menu_light_b", "menu_light_r"),
    ("MENU", "SOCKETS"): ("menu_socket_b", "menu_socket_r"),
    ("MENU", "RADIO"): ("menu_radio_b", "menu_radio_r"),
    ("LIGHTS", 1): ("submenu_light_b", "submenu_light_r_1"),
    ("LIGHTS", 2): ("submenu_light_b", "submenu_light_r_1"),
    ("LIGHTS", 3): ("submenu_light_b", "submenu_light_r_2"),
    ("LIGHTS", 4): ("submenu_light_b", "submenu_light_r_2"),
    ("LIGHTS", 5): ("submenu_light_b", "submenu_light_r_2"),
    ("LIGHTS", 6): ("submenu_light_b", "submenu_light_r_3"),
    ("LIGHTS", 7): ("submenu_light_b", "submenu_light_r_4"),
    ("LIGHTS", 8): ("submenu_light_b", "submenu_light_r_5"),
    ("SOCKETS", 1): ("submenu_socket_b", "submenu_socket_r_1"),
    ("SOCKETS", 2): ("submenu_socket_b", "submenu_socket_r_2"),
    ("SOCKETS", 3): ("submenu_socket_b", "submenu_socket_r_3"),
    ("SOCKETS", 4): ("submenu_socket_b", "submenu_socket_r_4"),
    ("SOCKETS", 5): ("submenu_socket_b", "submenu_socket_r_5"),
    ("RADIO", 1): ("submenu_radio_b", "submenu_radio_r_1"),
}

current_global_state = "MENU"
last_global_state = current_global_state
last_menu_state = None
current_menu_state = "LIGHTS"
is_active = False
displayed_menu_state = None
last_activity_time = time.ticks_ms()
pot_changed = False
lights_submenu_counter = 1
sockets_submenu_counter = 1
radio_submenu_counter = 1
current_key = None
last_key = None

try:
    while True:
        # global
        time.sleep(0.01)
        now = time.ticks_ms()

        buzz.update(now)
        epaper.update(now)
        remote.update(now)
        led_rgb.update(now)
        ha.update(now)

        # print(current_menu_state)

        # inputs
        current_btn_bck_state = button_bck.is_pressed(now)
        current_btn_frw_state = button_frw.is_pressed(now)
        current_btn_hme_state = button_hme.is_pressed(now)
        current_pot_value = pot.read()



       
        if (
            current_btn_bck_state == "PRESSED"
            or current_btn_frw_state == "PRESSED"
            or current_btn_hme_state == "PRESSED"
        ):
            print("on")
            led_c.on()

        is_active = False
        if (
            current_btn_bck_state == "RELEASED"
            or current_btn_frw_state == "RELEASED"
            or current_btn_hme_state == "RELEASED"
        ):
            led_c.off()
            is_active = True

        if abs(current_pot_value - last_pot_value) >= 10:
            is_active = True

        if is_active:
            last_activity_time = now

        # logic
        if current_global_state == "MENU":
            if current_btn_bck_state == "RELEASED":
                if current_menu_state == "LIGHTS":
                    current_menu_state = "RADIO"
                elif current_menu_state == "SOCKETS":
                    current_menu_state = "LIGHTS"
                elif current_menu_state == "RADIO":
                    current_menu_state = "SOCKETS"

            elif current_btn_frw_state == "RELEASED":
                if current_menu_state == "LIGHTS":
                    current_menu_state = "SOCKETS"
                elif current_menu_state == "SOCKETS":
                    current_menu_state = "RADIO"
                elif current_menu_state == "RADIO":
                    current_menu_state = "LIGHTS"

            elif current_btn_hme_state == "RELEASED":
                current_global_state = current_menu_state
                print(f"[main.py] IMPORTANT: entering '{current_menu_state}' submenu")

        else:
            if current_global_state == "LIGHTS":
                if current_btn_bck_state == "RELEASED":
                    lights_submenu_counter -= 1
                elif current_btn_frw_state == "RELEASED":
                    lights_submenu_counter += 1

                if lights_submenu_counter > 8:  # count each colors of every lights
                    lights_submenu_counter = 1
                if lights_submenu_counter < 1:  
                    lights_submenu_counter = 8 

                if abs(current_pot_value - last_stabilized_pot_value) >= 2:
                    last_stabilized_pot_value = current_pot_value
                    print("mov")
                    current_lights = None
                    if lights_submenu_counter == 1:
                        if current_pot_value <= 2:
                            ha.turn_off(home_assistant.Device.LATELIER)
                            led_a.off()
                        else:
                            ha.turn_on(home_assistant.Device.LATELIER)
                            led_a.value(current_pot_value)
                            ha.set_brightness(
                                home_assistant.Device.LATELIER,
                                int(
                                    inputs.map_range(current_pot_value, 0, 100, 0, 255)
                                ),
                            )

                    if lights_submenu_counter == 2:
                        ha.turn_on(home_assistant.Device.LATELIER)
                        ha.set_color_temp(
                            home_assistant.Device.LATELIER,
                            int(
                                inputs.map_range(current_pot_value, 0, 100, 6500, 2000)
                            ),
                        )

                    if lights_submenu_counter == 3:
                        if current_pot_value <= 2:
                            ha.turn_off(home_assistant.Device.LLEDS)
                            led_a.off()
                        else:
                            ha.turn_on(home_assistant.Device.LLEDS)
                            led_a.value(current_pot_value)
                            ha.set_brightness(
                                home_assistant.Device.LLEDS,
                                int(
                                    inputs.map_range(current_pot_value, 0, 100, 0, 255)
                                ),
                            )
                    if lights_submenu_counter == 4:
                        ha.turn_on(home_assistant.Device.LLEDS)
                        ha.set_color_temp(
                            home_assistant.Device.LLEDS,
                            int(
                                inputs.map_range(current_pot_value, 0, 100, 9000, 2500)
                            ),
                        )

                    if lights_submenu_counter == 5:
                        ha.turn_on(home_assistant.Device.LLEDS)
                        led_a.value(current_pot_value)

                        # pot_value = inputs.map_range(pot.read_raw(), 0, 65300, 0, 765)
                        # r = int(min(255, pot_value))
                        # g = int(min(255, pot_value-r))
                        # b = int(min(255, pot_value-(r+g)))
                        
                        pot_value = inputs.map_range(pot.read_raw(), 0, 65300, 0, 1535)
                        if pot_value < 256: # red to green
                            r = 255
                            b = pot_value
                            g = 0

                        elif pot_value < 512:
                            r = 511 - pot_value
                            b = 255
                            g = 0

                        elif pot_value < 768:
                            r = 0
                            b = 255
                            g =  pot_value - 511

                        elif pot_value < 1024:
                            r = 0
                            b = 1023 - pot_value
                            g = 255

                        elif pot_value < 1280:
                            r = pot_value - 1024;
                            b = 0;
                            g = 255;

                        else:
                            r = 255
                            b = 0
                            g = 1535 - pot_value
                        
                        r = int(r)
                        g = int(g)
                        b = int(b)
                        # print("-----")
                        # print(r)
                        # print(g)
                        # print(b)
                        # print("-----")

                        led_rgb.set_color(r, g, b)
                        ha.set_color(
                            home_assistant.Device.LLEDS,
                            r, g, b
                        )

                    if lights_submenu_counter == 6:
                        if current_pot_value <= 2:
                            ha.turn_off(home_assistant.Device.LBUREAU)
                            led_a.off()
                        else:
                            ha.turn_on(home_assistant.Device.LBUREAU)
                            led_a.value(current_pot_value)
                            ha.set_brightness(
                                home_assistant.Device.LBUREAU,
                                int(
                                    inputs.map_range(current_pot_value, 0, 100, 0, 255)
                                ),
                            )
                    if lights_submenu_counter == 7:
                        if current_pot_value <= 2:
                            ha.turn_off(home_assistant.Device.LPRINCIPALE)
                            led_a.off()
                        else:
                            ha.turn_on(home_assistant.Device.LPRINCIPALE)
                            led_a.value(current_pot_value)
                            ha.set_brightness(
                                home_assistant.Device.LPRINCIPALE,
                                int(
                                    inputs.map_range(current_pot_value, 0, 100, 0, 255)
                                ),
                            )
                    if lights_submenu_counter == 8:
                        if current_pot_value > 60:
                            remote.press("a")
                        else:
                            remote.press("off")

                    
                

            elif current_global_state == "SOCKETS":
                if current_btn_bck_state == "RELEASED":
                    sockets_submenu_counter -= 1
                elif current_btn_frw_state == "RELEASED":
                    sockets_submenu_counter += 1

                if sockets_submenu_counter > 5:
                    sockets_submenu_counter = 1

            elif current_global_state == "RADIO":
                pass

            if current_btn_hme_state == "RELEASED":
                current_global_state = "MENU"

        # display

        # always update rgb led

        if current_global_state == "MENU" and current_menu_state != last_menu_state:
            led_rgb.set_mode(f"{current_menu_state}")



        if current_global_state == "MENU":
            current_key = ("MENU", current_menu_state)
            
        elif current_global_state == "LIGHTS":
            current_key = ("LIGHTS", lights_submenu_counter)
            led_rgb.set_mode(f"LIGHTS_{lights_submenu_counter}")
        elif current_global_state == "SOCKETS":
            current_key = ("SOCKETS", sockets_submenu_counter)
            led_rgb.set_mode(f"SOCKETS_{lights_submenu_counter}")
        elif current_global_state == "RADIO":
            current_key = ("RADIO", 1)
            led_rgb.set_mode("RADIO")
        else:
            current_key = None

        if last_key != current_key:
            pass
        last_key = current_key

        # the e ink screen needs more code, because we cant send twice the same image (ai helped me a bit on this)
        if isinstance(last_activity_time, int) and now - last_activity_time >= 1000:
            led_a.off()

            target_images = DISPLAY_TRANSLATION.get(current_key)
            if target_images and displayed_menu_state != current_key:
                print("true")
                epaper.show_image(target_images[0], target_images[1])
                displayed_menu_state = current_key

        last_menu_state = current_menu_state
        last_pot_value = current_pot_value
        last_global_state = current_global_state

        if now - last_pot_stabilization > 1000:
            last_stabilized_pot_value = current_pot_value
            last_pot_stabilization = now

except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()
