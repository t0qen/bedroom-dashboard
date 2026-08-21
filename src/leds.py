from machine import Pin, PWM
import inputs

class Led:
    def __init__(self, pin):
        self.pin = pin
        self.led = PWM(Pin(self.pin, Pin.OUT))
        self.led.freq(5000)

    def on(self):
        self.led.duty_u16(65535)

    def value(self, val):
        self.led.duty_u16(int(inputs.map_range(val, 0, 100, 0, 65535)))
    def off(self):
        self.led.duty_u16(0)


class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.led_r = PWM(Pin(pin_r))
        self.led_r.freq(5000)
        self.led_g = PWM(Pin(pin_g))
        self.led_g.freq(5000)
        self.led_b = PWM(Pin(pin_b))
        self.led_b.freq(5000)

        self.current_mode = None
        self.new_mode = False
        self.counter = 0
        self.phase = []
        self.prev_colors = []
        self.last_millis = 0

    def set_color(self, r, g, b):
        if self.prev_colors != [r, g, b]:
            self.led_r.duty_u16(int(inputs.map_range(r, 0, 100, 0, 65535)))
            self.led_g.duty_u16(int(inputs.map_range(g, 0, 100, 0, 65535)))
            self.led_b.duty_u16(int(inputs.map_range(b, 0, 100, 0, 65535)))

        self.prev_colors = [r, g, b]

    def off(self):
        self.led_r.duty_u16(0)
        self.led_g.duty_u16(0)
        self.led_b.duty_u16(0)

    def set_mode(self, mode):
        
        if mode != self.current_mode:
            self.off()
            self.current_mode = mode
            self.new_mode = True
            self.counter = 0
            print(f"[leds.py] INFO: new mode: '{self.current_mode}'")

    def update(self, current_time):
        if self.current_mode == "LIGHTS":
            if self.new_mode:
                self.new_mode = False
                # mode setup

                step = 20
                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[val, val, step] for val in range(step - 1, -1, -1)]
                phase3 = [[0, 0, val] for val in range(step - 1, -1, -1)]
                self.phase = phase1 + phase2 + phase3

            if current_time - self.last_millis >= 30:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "SOCKETS":
            if self.new_mode:
                self.new_mode = False
                # mode setup

                step = 20
                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[val, step, val] for val in range(step - 1, -1, -1)]
                phase3 = [[0, val, 0] for val in range(step - 1, -1, -1)]
                self.phase = phase1 + phase2 + phase3

            if current_time - self.last_millis >= 30:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "RADIO":
            if self.new_mode:
                self.new_mode = False
                # mode setup
                step = 20

                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[step, val, val] for val in range(step - 1, -1, -1)]
                phase3 = [[val, 0, 0] for val in range(step - 1, -1, -1)]
                self.phase = phase1 + phase2 + phase3

            if current_time - self.last_millis >= 30:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "LIGHTS_1":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[val, val, val] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 50:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "LIGHTS_2":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[val, val, val] for val in range(step - 1, -1, -1)]
                phase3 = [[val, val, 0] for val in range(step + 1)]
                phase4 = [[val, val, 0] for val in range(step - 1, -1, -1)]
                self.phase = phase1 + phase2 + phase3 + phase4

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "LIGHTS_3":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[val, val, 0] for val in range(step + 1)]
                phase2 = [[val, val, 0] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "LIGHTS_4":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[val, val, val] for val in range(step + 1)]
                phase2 = [[val, val, val] for val in range(step - 1, -1, -1)]
                phase3 = [[val, val, 0] for val in range(step + 1)]
                phase4 = [[val, val, 0] for val in range(step - 1, -1, -1)]
                self.phase = phase1 + phase2 + phase3 + phase4

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "LIGHTS_5":
            pass

        elif self.current_mode == "LIGHTS_6" or self.current_mode == "LIGHTS_7":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[val, val, 0] for val in range(step + 1)]
                phase2 = [[val, val, 0] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time


        elif self.current_mode == "LIGHTS_8":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[step, step, 0] for val in range(step + 1)]
                phase2 = [[0, 0, 0] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time


        elif self.current_mode == "SOCKETS_1":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[step, 0, step] for val in range(step + 1)]
                phase2 = [[val, 0, val] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "SOCKETS_2" or self.current_mode == "SOCKETS_3":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[0, step, step] for val in range(step + 1)]
                phase2 = [[0, val, val] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time

        elif self.current_mode == "SOCKETS_4" or self.current_mode == "SOCKETS_5":
            if self.new_mode:
                self.new_mode = False

                step = 20
                phase1 = [[step/2, 0, step] for val in range(step + 1)]
                phase2 = [[abs(val/2), 0, val] for val in range(step - 1, -1, -1)]

                self.phase = phase1 + phase2

            if current_time - self.last_millis >= 20:
                self.set_color(
                    self.phase[self.counter][0],
                    self.phase[self.counter][1],
                    self.phase[self.counter][2],
                )
                self.counter += 1
                if self.counter >= len(self.phase):
                    self.counter = 0

                    self.last_millis = current_time
            

