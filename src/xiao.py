from machine import UART, Pin
import time

xiao_finished = True

class Display:
    def __init__(self) -> None:
        self.uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

        self.uart_any = False
        self.uart_incoming_data = bytearray()
        self.uart.irq(self._uart_handler, 64, True)

        self.command_queue = []
        self.last_image = []
        self.image_queue = []
        self.uart.write("clearScreen()\n")
        time.sleep(0.01)
        self.uart.write("fillScreen(1)\n") 
        time.sleep(0.01)

    def _uart_handler(self, uart_obj):
        self.uart_any = True

    def send(self, cmd):
        if not self.command_queue or cmd != self.command_queue[-1]:
            self.command_queue.append(cmd)
            print(f"[xiao.py] INFO: command '{cmd}' has been added to queue")
        else:
            print(f"[xiao.py] WARNING: command '{cmd}' has already been added to queue")

    def show_image(self, img_b, img_r, x=0, y=0, w=296, h=128, c=0):
        if img_r != self.last_image: # FIXME # TODO
            self.image_queue = [img_b, img_r, x, y, w, h, c]
            print(f"[xiao.py] INFO: image '{img_b, img_r}' has been added to queue")
        else:
            print(f"[xiao.py] WARNING: image '{img_b, img_r}' has already been added to queue")


    def update(self, current_time):
        global xiao_finished

        if self.uart_any:
            print("[xiao.py] IMPORTANT: detected incoming message on uart ")
            self.uart_any = False
            if self.uart.any():
                message = self.uart.readline()
                if message and isinstance(message, bytes):
                    fromat_message = message.decode('utf-8').strip()
                    print(f"[xiao.py] IMPORTANT: the message received from uart is '{fromat_message}'")
                    if fromat_message == "DONE":
                        print(f"[xiao.py] IMPORTANT: the message received from uart confirmed that xiao finished displaying")
                        xiao_finished = True

        if xiao_finished:
            if self.image_queue:
                self.uart.write("clearScreen()\n")
                time.sleep(0.01)
                self.uart.write("fillScreen(1)\n")
                time.sleep(0.01)

                if self.image_queue[1] == None:
                    cmd = f"drawBinImage(/{self.image_queue[0]}.bin, {self.image_queue[2]}, {self.image_queue[3]}, {self.image_queue[4]}, {self.image_queue[5]}, {self.image_queue[6]})\n"
                    print("[xiao.py] INFO: 2 colors mode")
                else:
                    cmd = f"draw3ColorImage(/{self.image_queue[0]}.bin, /{self.image_queue[1]}.bin, {self.image_queue[2]}, {self.image_queue[3]}, {self.image_queue[4]}, {self.image_queue[5]})\n"
                    print("[xiao.py] INFO: 3 colors mode")

                self.uart.write(cmd)
                time.sleep(0.01)
                self.uart.write("display()\n")
                xiao_finished = False
                self.last_image = self.image_queue[1] 
                self.image_queue = [] 
                print("[xiao.py] INFO: imaged sended to xiao")

            elif self.command_queue:
                self.uart.write("clearScreen()\n")
                time.sleep(0.01)
                self.uart.write("fillScreen(1)\n")
                time.sleep(0.01)
                for i in self.command_queue:
                    self.uart.write(i + "\n")
                    time.sleep(0.01)
                self.uart.write("display()\n")
                xiao_finished = False
                self.command_queue = []
                print("[xiao.py] INFO: commands sended to xiao")


