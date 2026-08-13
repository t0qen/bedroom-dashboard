from machine import UART, Pin
import time



class Display:
    def __init__(self) -> None:
        self.uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

    def send(self,cmd):
        self.uart.write(cmd + "\n")
        time.sleep(0.01) 

    def update(self):
        send("display()")
        print("Attente de la fin d'affichage...")
        
        # La Pico écoute la Xiao et attend le mot "DONE"
        while True:
            if self.uart.any():
                reponse = self.uart.readline()
                
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

        send("setTextColor(0)")
        send("setTextSize(2)")
        send("setCursor(10, 10)")
        send("print(Coucou Maman, ceci est un ecran e-ink, cet-a-dire a encre electronique. Comme sur les liseuses.)")
    
        send("setTextColor(2)")
        send("setTextSize(1)")
        send("setCursor(10, 90)")
        send("print(Il peut afficher en rouge aussi)")
        update() 
