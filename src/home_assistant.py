
class Device:
    LATELIER = "light.ampoule_atelier"
    LPRINCIPALE = "light.ampoule_principale"
    LBUREAU = "light.lampe_bureau"
    LLEDS = "light.leds_chambre"
    PPC = "switch.prise_pc"
    PGLOBALE = "switch.prise_study"
    PETAGERE = "switch.prise_etagere"

class HomeAssistant:
    def __init__(self, uart):
        self.uart = uart

        self.last_colors = []
        self.colors_queue = []
        self.last_colors_send = 0

    def _send(self, command):
        self.uart.write(command + "\n")

    def turn_on(self, device):
        self._send(f"HA_ON({device})")

    def turn_off(self, device):
        self._send(f"HA_OFF({device})")

    def toggle(self, device):
        self._send(f"HA_TOGGLE({device})")

    def set_brightness(self, device, brightness):
        if brightness > 255:
            brightness = 255
        if brightness < 0:
            brightness = 0
        self._send(f"HA_BRIGHT({device}, {brightness})")

    def set_color_temp(self, device, kelvin):
        self._send(f"HA_TEMP({device}, {kelvin})")

    def set_color(self, device, r, g, b):
        if self.last_colors != [r, g, b]:
            self.colors_queue = [r, g, b]

        self.last_colors = [r, g, b]

    def update(self, now):
        
        if self.colors_queue and now - self.last_colors_send >= 5000: # little exception for my rgb leds, we send colors only every 2s to not crash it
            print("[leds.py] INFO: sended rgb colors to home assistant")
            self.last_colors_send = now
            r = self.colors_queue[0]
            g = self.colors_queue[1]
            b = self.colors_queue[2]
            self._send(f"HA_COLOR({Device.LLEDS}, {r}, {g}, {b})")
            
            self.colors_queue = []