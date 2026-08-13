# import display, inputs, leds, sprites, remote_hack, apps
# import time
# from machine import Pin

# button_prev = inputs.Button(14)
# button_next = inputs.Button(13)
# button_home = inputs.Button(16)

# remote = remote_hack.Remote(18, 19, 20, 21)

# led1 = leds.Leds(4)
# led2 = leds.Leds(6)
# led3 = leds.Leds(7)

# matrix = display.Display()
# matrix.clear()

# while True:
#     time.sleep(0.001)
#     now = time.ticks_ms()

#     remote.update(now)

#     button_prev_state = button_prev.is_pressed(now)
#     button_next_state = button_next.is_pressed(now)
#     button_home_state = button_home.is_pressed(now)

#     if button_prev_state == "PRESSED":
#         led1.on()
#         remote.press("a")
#         print("Button Prev Pressed")
#     elif button_prev_state == "RELEASED":
#         led1.off()
        
#         print("Button Prev Released")
#     if button_next_state == "PRESSED":
#         led2.on()
#         remote.press("b")
#         print("Button Next Pressed")
#     elif button_next_state == "RELEASED":
#         led2.off()
#         print("Button Next Released")
#     if button_home_state == "PRESSED":
#         led3.on()
#         remote.press("c")
#         print("Button Home Pressed")
#     elif button_home_state == "RELEASED":
#         led3.off()
#         print("Button Home Released")

from machine import UART, Pin
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

def send(cmd):
    uart.write(cmd + "\n")
    time.sleep(0.01) 

# Nouvelle fonction pour rafraîchir l'écran SANS bloquer la communication
def update():
    send("display()")
    print("Attente de la fin d'affichage...")
    
    # La Pico écoute la Xiao et attend le mot "DONE"
    while True:
        if uart.any():
            reponse = uart.readline()
            
            # On vérifie explicitement que c'est bien du binaire
            if reponse and isinstance(reponse, bytes):
                # On convertit le binaire en texte et on nettoie les espaces
                texte = reponse.decode('utf-8').strip()
                
                if texte == "DONE":
                    print("Ecran mis à jour !")
                    break
    time.sleep(0.1)

# --- EXEMPLE D'UTILISATION ---
if __name__ == '__main__':
    send("clearScreen()")  # Remplit le buffer de blanc (grâce à la modif ci-dessus)
    send("fillScreen(1)") 

    send("setTextColor(0)")
    send("setTextSize(2)")
    send("setCursor(10, 10)")
    send("print(Coucou Maman, ceci est un ecran e-ink, cet-a-dire a encre electronique. Comme sur les liseuses.)")
 
    send("setTextColor(2)")
    send("setTextSize(1)")
    send("setCursor(10, 90)")
    send("print(Il peut afficher en rouge aussi)")
    # Ici, la Pico s'arrête et attend sagement que l'e-paper finisse de clignoter
    update() 
