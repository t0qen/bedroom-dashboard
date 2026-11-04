from machine import Pin


class Remote:
    def __init__(
        self, pin_a, pin_b, pin_c, pin_off
    ):  # pim_a = bleu, pin b = jaune, pin c = orange, pin off = bblue long

        self.button_a = Pin(pin_a, Pin.OUT)
        self.button_b = Pin(pin_b, Pin.OUT)
        self.button_c = Pin(pin_c, Pin.OUT)
        self.button_off = Pin(pin_off, Pin.OUT)

        self.button_a.value(0)
        self.button_b.value(0)
        self.button_c.value(0)
        self.button_off.value(0)

        self.state = "WAITING"
        self.current_button = None
        self.time_start_impulsion = 0
        self.impulsion_time = 100

        self.queue = ""
        self.last_queue = ""

    def press(self, button):
        if self.last_queue != button:
            self.queue = button

        self.last_queue = button

    def update(self, time):
        if self.state == "WAITING":
            if self.queue:
                current_button_queue = self.queue
                if current_button_queue == "a":
                    self.button_a.value(1)
                    self.current_button = self.button_a
                elif current_button_queue == "b":
                    self.button_b.value(1)
                    self.current_button = self.button_b
                elif current_button_queue == "c":
                    self.button_c.value(1)
                    self.current_button = self.button_c
                elif current_button_queue == "off":
                    self.button_off.value(1)
                    self.current_button = self.button_off
                self.time_start_impulsion = time
                self.state = "IMPULSION"
                self.queue = ""

        elif self.state == "IMPULSION":
            if (time - self.time_start_impulsion) >= self.impulsion_time:
                if self.current_button is not None:
                    self.current_button.value(0)
                    self.current_button = None
                self.state = "WAITING"

    # def keep_only(self, button):
    #     if button == "a":
    #         self.button_off.value(0)
    #         self.button_a.value(1)
    #     elif button == "b":
    #         self.button_off.value(0)
    #         self.button_b.value(1)
    #     elif button == "c":
    #         self.button_off.value(0)
    #         self.button_c.value(1)
