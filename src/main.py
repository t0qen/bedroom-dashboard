import apps, inputs, leds, remote_hack, xiao, buzzer, home_assistant
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

pot = inputs.Pot(28)



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

# test()


# def test2():
#     while True:
#         time.sleep(0.01)
#         now = time.ticks_ms()
        

        # for i in range(100):

        #     led_rgb.set_color(0, i, int(i / 2))
        #     time.sleep_ms(2)
        # for i in range(100):
        #     led_rgb.set_color(0, abs(i - 100) , int(abs(i - 100) / 2))
        #     time.sleep_ms(7)

        # step = 20

        # for i in range(step):
        #     led_rgb.set_color(i, 0, abs(i - step))
        #     time.sleep_ms(20)
        # for i in range(step):
        #     led_rgb.set_color(abs(i - step), i , 0)
        #     time.sleep_ms(20) 
        # for i in range(step):
        #     led_rgb.set_color(0, abs(i - step), i)
        #     time.sleep_ms(20) 

        # for i in range(step):
        #     led_rgb.set_color(i, i, i)
        #     time.sleep_ms(20)
        # for i in range(step):
        #     led_rgb.set_color(abs(i - step), abs(i - step), step)
        #     time.sleep_ms(10)   
        # for i in range(step):
        #     led_rgb.set_color(0, 0, abs(i - step))
        #     time.sleep_ms(20)

        # for i in range(33):
        #     led_rgb.set_color(abs(i - 33), abs(i - 33), abs(i - 33))
        #     time.sleep_ms(10)
                        

# test2()

current_global_state = "MENU"
last_menu_state = None
current_menu_state = "LIGHTS"



try:
    while True:
        # global
        time.sleep(0.01)
        now = time.ticks_ms()

        buzz.update(now)
        epaper.update(now)
        remote.update(now)
        led_rgb.update(now)

        # print(current_menu_state)

        # inputs
        current_btn_bck_state = button_bck.is_pressed(now)
        current_btn_frw_state = button_frw.is_pressed(now)
        current_btn_hme_state = button_hme.is_pressed(now)
        current_pot_value = pot.read()

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

                if current_menu_state ==  "LIGHTS":
                    current_menu_state = "SOCKETS"
                elif current_menu_state == "SOCKETS":
                    current_menu_state = "RADIO"
                elif current_menu_state == "RADIO":
                    current_menu_state = "LIGHTS"

            elif current_btn_hme_state == "RELEASED":

                current_global_state = current_menu_state

        # display
        if current_global_state == "MENU":
            if current_menu_state != last_menu_state:
                # print("update")
                if current_menu_state =="LIGHTS":
                    led_rgb.set_mode("menu_lights")
                    epaper.show_image("menu_light_b", "menu_light_r")
                elif current_menu_state =="SOCKETS":
                    led_rgb.set_mode("menu_sockets")
                    epaper.show_image("menu_socket_b", "menu_socket_r")
                elif current_menu_state == "RADIO":
                    led_rgb.set_mode("menu_radio")
                    epaper.show_image("menu_radio_b", "menu_radio_r")

        last_menu_state = current_menu_state


except KeyboardInterrupt:
    print("[main.py] IMPORTANT: asked for stop the main program")

finally:
    clean()
