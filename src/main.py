import display, inputs, leds, sprites, remote_hack, apps
import time

button_prev = inputs.Button(14)
button_next = inputs.Button(13)
button_home = inputs.Button(16)

while True:
    time.sleep(0.001)
    now = time.ticks_ms()

    button_prev_state = button_prev.is_pressed(now)
    button_next_state = button_next.is_pressed(now)
    button_home_state = button_home.is_pressed(now)

    if button_prev_state == "PRESSED":
        print("Button PREV pressed")
    elif button_prev_state == "RELEASED":
        print("Button PREV released")
    
