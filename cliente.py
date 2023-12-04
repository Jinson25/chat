import socket
import threading
import sys

def receive_messages():
    global client_socket, user_name

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')

            sender_name, _, _ = message.partition(':')

            if sender_name.strip() != user_name.strip():
                print(message)

    except socket.error as e:
        print(f"Error al recibir mensajes del servidor: {e}")
        print("Se ha perdido la conexión con el servidor. Intentando reconectar.")

        client_socket.close()

        user_name = input("Ingrese su nombre: ")
        server_ip = input("Ingrese la dirección IP del servidor: ")

        if not server_ip:
            server_ip = discover_server_ip()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((server_ip, 12345))
            client_socket.send(user_name.encode('utf-8'))

            client_ip, client_port = client_socket.getsockname()
            print(f"Conectado al servidor en {server_ip}:{client_port} como {user_name}")

            receive_thread = threading.Thread(target=receive_messages)
            receive_thread.start()

        except socket.error as e:
            print(f"Error al reconectar con el servidor: {e}")
            print("Asegúrate de que la dirección IP y el puerto del servidor sean correctos.")
            sys.exit()

def discover_server_ip():
    multicast_group = '224.0.0.1'
    port = 54321

    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    discovery_socket.settimeout(1)
    discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    try:
        discovery_socket.sendto(b'DISCOVER_SERVER', (multicast_group, port))
        data, _ = discovery_socket.recvfrom(1024)
        server_ip = data.decode('utf-8').strip()
        print(f"Servidor encontrado en la dirección IP: {server_ip}")
        return server_ip

    except socket.timeout:
        print("No se ha encontrado ningún servidor en la red. Ingresa la dirección IP manualmente.")
        return input("Ingrese la dirección IP del servidor: ")

    finally:
        discovery_socket.close()

user_name = input("Ingrese su nombre: ")
server_ip = input("Ingrese la dirección IP del servidor: ")

if not server_ip:
    server_ip = discover_server_ip()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, 12345))
    client_socket.send(user_name.encode('utf-8'))

    client_ip, client_port = client_socket.getsockname()
    print(f"Conectado al servidor en {server_ip}:{client_port} como {user_name}")

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        message = input("Ingrese un mensaje:")
        if message.lower() == 'exit':
            break
        client_socket.send(f"{user_name}: {message}".encode('utf-8'))

except socket.error as e:
    print(f"Error al conectar con el servidor: {e}")
    print("Asegúrate de que la dirección IP y el puerto del servidor sean correctos.")
    sys.exit()

finally:
    client_socket.close()
