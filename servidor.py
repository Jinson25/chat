import socket
import threading

def handle_client(client_socket, client_address):
    try:
        # Obtener el nombre del cliente
        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"Conexión establecida desde {client_address}. Nombre: {client_name}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"{client_name} dice: {message}")

            broadcast(f"{message}")

    except socket.error as e:
        print(f"{client_name} se ha desconectado.")
    finally:
        client_socket.close()
        clients.remove(client_socket)

def broadcast(message):
    for client in clients.copy():
        try:
            client.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error al enviar mensaje a un cliente: {e}")
            clients.remove(client)

# Configuración del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_ip = socket.gethostbyname(socket.gethostname())  # Cambié la función para obtener la IP local
port = 12345
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
