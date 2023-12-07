import socket
import threading

def handle_client(client_socket, client_address):
    try:
        nombre = client_socket.recv(1024).decode('utf-8')
        print(f"Conexión establecida desde {client_address}. Nombre: {nombre}")

        while True:
            mensaje = client_socket.recv(1024).decode('utf-8')
            if not mensaje:
                print(f"{nombre} se ha desconectado.")
                break

            print(f"{nombre} dice: {mensaje}")
            send_to_all(f"{nombre}: {mensaje}", client_socket)

    except socket.error as e:
        print(f"Error de conexión con {nombre}: {e}")
    finally:
        client_socket.close()

def send_to_all(message, sender_socket):
    for client in clients.copy():
        try:
            if client != sender_socket:
                client.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error al enviar mensaje a un cliente: {e}")
            clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_ip = socket.gethostbyname(socket.gethostname())
port = 5555
server.bind((local_ip, port))
server.listen(5)

print(f"Servidor iniciado en {local_ip}:{port}. Esperando conexiones...")

clients = []

while True:
    client_socket, addr = server.accept()
    print(f"Conexión establecida desde {addr}")

    clients.append(client_socket)

    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()
