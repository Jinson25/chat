import socket
import threading

def enviar_mensajes(client_socket):
    while True:
        mensaje = input("Mensaje: ")
        client_socket.send(mensaje.encode())

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())
        except ConnectionResetError:
            break

def main():
    ip_servidor = input("Ingresa la IP del servidor: ")
    puerto_servidor = 5555

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((ip_servidor, puerto_servidor))

    nombre = input("Ingresa tu nombre: ")
    socket_cliente.send(nombre.encode())

    hilo_envio = threading.Thread(target=enviar_mensajes, args=(socket_cliente,))
    hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(socket_cliente,))

    hilo_envio.start()
    hilo_recepcion.start()

if __name__ == "__main__":
    main()