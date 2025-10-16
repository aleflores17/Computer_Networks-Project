import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                print("[-] Server closed the connection.")
                break
            print(f"\nServer: {message}")
        except ConnectionResetError:
            print("[-] Connection lost.")
            break
    sock.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    print(f"[+] Connected to server {server_ip}:{server_port}")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        try:
            message = input("You: ")
            sock.sendall(message.encode())
        except KeyboardInterrupt:
            print("\n[-] Exiting chat.")
            sock.close()
            break

if __name__ == "__main__":
    main()
