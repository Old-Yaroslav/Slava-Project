from Socket import Socket
import asyncio
from os import system
from Encryption import Encryptor
from datetime import datetime
from tkinter import *

tk = Tk()


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""
        self.encryptor = Encryptor()

    def set_up(self):
        try:
            self.socket.connect(
                ('localhost', 1234)
            )
        except ConnectionRefusedError:
            print("Сервер спит, не будите")
            exit(0)

        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            clean_data = self.encryptor.decrypt(data.decode("utf-8"))

            self.messages += f"{datetime.now().date()}: {clean_data}\n"

            system("cls")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            data = await self.main_loop.run_in_executor(None, input)
            encrypted_data = self.encryptor.encrypt(data)

            await self.main_loop.sock_sendall(self.socket, encrypted_data.encode("utf-8"))

    async def main(self):
        await asyncio.gather(

            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())

        )


"""
lbl = Label(tk)
text = StringVar()
name = StringVar()
name.set('')
text.set('')
tk.title('Chat')
tk.geometry('400x300')

log = Text(tk)
nick = Entry(tk, textvariable=name)
msg = Entry(tk, textvariable=text)
msg.pack(side='bottom', fill='x', expand='true')
nick.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both', expand='true')
def loopproc():
    client.setblocking(False)

    try:
        bdata = client.recv(2048)
        data = bdata.decode()
        log.insert(END, data+ '\n')
    except:
        tk.after(1, loopproc)
        return

    tk.after(1,loopproc)
    return

def sendproc(event):
    data = '{name}:{text}'.format(name=name.get(), text=text.get())
    bdata = data.encode()
    sock.sendto(bdata, ('255.255.255.255', 11719))
    text.set('')

msg.bind('<Return>', sendproc)
tk.after(1, loopproc)
tk.mainloop()
"""

if __name__ == '__main__':
    client = Client()
    client.set_up()

    client.start()

