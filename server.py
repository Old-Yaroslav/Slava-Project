from Socket import Socket
import asyncio
from tkinter import *

tk = Tk()


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        self.users = []

    def set_up(self):
        self.socket.bind(('localhost', 1234))

        self.socket.listen(5)
        self.socket.setblocking(False)
        print("Server is listening...")

    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)

    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                print(data.decode("utf-8"))
                await self.send_data(data)
            except ConnectionResetError:
                print("Пользователь покинул чат")
                self.users.remove(listened_socket)
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"User {address[0]} connected!")

            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())



"""
lbl = Label(tk, text="Server is listening...")
lbl.grid(column=0, row=0)
tk.title('Server')
tk.geometry('400x150')

log = Text(tk)

def loopproc():
    s.setblocking(False)

    try:
        bdata = s.recv(2048)
        data = bdata.decode()
        log.insert(END, data+ '\n')
    except:
        tk.after(1, loopproc)
        return

    tk.after(1,loopproc)
    return


tk.after(1, loopproc)
tk.mainloop()
"""

if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()

