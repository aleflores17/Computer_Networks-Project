import socket
import sys
import threading
clients = []

def broadcast(message, sender_conn):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    clients.append(conn)
    try:
        while True:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"[Client {addr}] {message}")
            broadcast(f"[{addr}] {message}", conn)
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        clients.remove(conn)
        print(f"[-] Disconnected {addr}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <listen_port>")
        sys.exit(1)

    host = "0.0.0.0"
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
