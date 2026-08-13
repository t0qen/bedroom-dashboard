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
def send_image(x, y, w, h, color, img_bytes):
    # 1. On envoie la commande texte
    send(f"drawImage({x},{y},{w},{h},{color})")
    
    # 2. On attend que la Xiao dise READY
    while True:
        if uart.any():
            reponse = uart.readline()
            if reponse and isinstance(reponse, bytes):
                texte = reponse.decode('utf-8').strip()
                if texte == "READY":
                    break
    
    # 3. On envoie les octets de l'image d'un coup
    uart.write(img_bytes)
    print("Image envoyée, en attente de validation...")
    
    # 4. On attend que la Xiao dise DONE (image bien reçue)
    while True:
        if uart.any():
            reponse = uart.readline()
            if reponse and isinstance(reponse, bytes):
                texte = reponse.decode('utf-8').strip()
                if texte == "DONE":
                    print("Image reçue par la Xiao !")
                    break
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

if __name__ == '__main__':
    send("clearScreen()") 
    send("fillScreen(1)") 
    print("logo")
    send("drawBinImage(/cat.bin, 0, 0, 296, 128, 2)")

    update()
