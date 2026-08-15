
class Device:
    LUMIERE_SALON = "light.ampoule_atelier"
    LUMIERE_CHAMBRE = "light.chambre"
    PRISE_BUREAU = "switch.prise_bureau"

class HomeAssistant:
    def __init__(self, uart):
        # On récupère l'objet UART déjà configuré dans ton main.py
        self.uart = uart

    def _send(self, command):
        # On ajoute un '\n' car le code C++ fait un readStringUntil('\n')
        self.uart.write(command + "\n")

    def turn_on(self, device):
        self._send(f"HA_ON({device})")

    def turn_off(self, device):
        self._send(f"HA_OFF({device})")

    def toggle(self, device):
        self._send(f"HA_TOGGLE({device})")

    def set_brightness(self, device, brightness_pct):
        # HA attend une valeur de 0 à 255
        brightness_val = int((brightness_pct / 100) * 255)
        self._send(f"HA_BRIGHT({device}, {brightness_val})")