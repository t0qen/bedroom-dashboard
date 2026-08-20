
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

    def set_color(self, device, r, g, b):
        self._send(f"HA_COLOR({device}, {r}, {g}, {b})")

    def set_color_temp(self, device, kelvin):
        self._send(f"HA_TEMP({device}, {kelvin})")