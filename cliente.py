import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Cliente")
        self.master.geometry("700x500")  # Establecer un tamaño inicial

        # Colores
        color_fondo = "#FFD700"  # Amarillo
        color_chat = "#87CEFA"   # Azul claro
        color_lista_usuarios = "#98FB98"  # Verde claro

        # Elementos de la interfaz
        self.users_listbox = tk.Listbox(self.master, width=20, bg=color_lista_usuarios)
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=15, bg=color_chat)
        self.refresh_button = tk.Button(self.users_listbox, text="Refrescar", command=self.actualizar_usuarios, bg=color_fondo)  # Movido a la lista de usuarios
        self.input_entry = tk.Entry(self.chat_area, width=30)  # Movido fuera del área de chat
        self.send_button = tk.Button(self.chat_area, text="Enviar", command=self.enviar_mensaje, bg=color_fondo)  # Movido fuera del área de chat

        # Posicionamiento de elementos
        self.users_listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_area.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.refresh_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.send_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Configuración de la conexión y otros elementos
        self.configurar_conexion()

    def configurar_conexion(self):
        self.ip_servidor = simpledialog.askstring("IP del Servidor", "Ingresa la IP del servidor:")
        self.puerto_servidor = 5555

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((self.ip_servidor, self.puerto_servidor))

        self.nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        self.socket_cliente.send(self.nombre.encode())

        self.hilo_envio = threading.Thread(target=self.recibir_mensajes)
        self.hilo_envio.start()

    def enviar_mensaje(self):
        mensaje = self.input_entry.get()
        destinatario = self.users_listbox.get(tk.ACTIVE)
        if destinatario:
            self.chat_area.insert(tk.END, f"[Mensaje privado a {destinatario}]: {mensaje}\n")
            try:
                self.socket_cliente.send(f"@{destinatario} {mensaje}".encode())
            except socket.error:
                self.chat_area.insert(tk.END, "El servidor se ha cerrado o hay un problema de conexión.\n")
        else:
            self.chat_area.insert(tk.END, "Selecciona un destinatario para enviar un mensaje privado.\n")
        self.input_entry.delete(0, tk.END)

    def recibir_mensajes(self):
        while True:
            try:
                data = self.socket_cliente.recv(1024)
                if not data:
                    break
                mensaje_recibido = data.decode()
                if mensaje_recibido.startswith("LISTA_CONECTADOS:"):
                    self.actualizar_lista_usuarios(mensaje_recibido)
                else:
                    self.chat_area.insert(tk.END, f"{mensaje_recibido}\n")
                    self.chat_area.see(tk.END)
            except ConnectionResetError:
                self.chat_area.insert(tk.END, "El servidor se ha cerrado o hay un problema de conexión.\n")
                break

    def actualizar_lista_usuarios(self, mensaje):
        lista_usuarios = mensaje.split(":")[1].split(",")
        self.users_listbox.delete(0, tk.END)
        for usuario in lista_usuarios:
            self.users_listbox.insert(tk.END, usuario)

    def actualizar_usuarios(self):
        try:
            self.socket_cliente.send("#lista_clientes".encode())
        except socket.error:
            self.chat_area.insert(tk.END, "El servidor se ha cerrado o hay un problema de conexión.\n")

def main():
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
