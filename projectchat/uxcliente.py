import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClienteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente de Chat")

        self.chat_text = scrolledtext.ScrolledText(root, height=15, width=40)
        self.chat_text.pack(pady=10)

        self.entry_message = tk.Entry(root, width=30)
        self.entry_message.pack(pady=10)

        self.send_button = tk.Button(root, text="Enviar", command=self.enviar_mensaje)
        self.send_button.pack(pady=10)

        self.ip_servidor = tk.Entry(root, width=15)
        self.ip_servidor.insert(0, "127.0.0.1")  # IP predeterminada
        self.ip_servidor.pack(pady=10)

        self.connect_button = tk.Button(root, text="Conectar", command=self.conectar)
        self.connect_button.pack(pady=10)

        self.socket_cliente = None
        self.nombre = ""

    def conectar(self):
        ip_servidor = self.ip_servidor.get()
        puerto_servidor = 5555

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((ip_servidor, puerto_servidor))

        self.nombre = tk.simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        self.socket_cliente.send(self.nombre.encode())

        hilo_envio = threading.Thread(target=self.enviar_mensajes)
        hilo_recepcion = threading.Thread(target=self.recibir_mensajes)

        hilo_envio.start()
        hilo_recepcion.start()

    def enviar_mensaje(self):
        mensaje = self.entry_message.get()
        self.socket_cliente.send(mensaje.encode())
        self.entry_message.delete(0, tk.END)

    def recibir_mensajes(self):
        while True:
            try:
                data = self.socket_cliente.recv(1024)
                if not data:
                    break
                mensaje = data.decode()
                self.chat_text.insert(tk.END, mensaje + "\n")
                self.chat_text.yview(tk.END)
            except ConnectionResetError:
                break

def main():
    root = tk.Tk()
    cliente_gui = ClienteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
