import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()


def handle_client(conn, addr):
    """Handles individual client connection."""
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:  
                break
            if msg == DISCONNECT_MESSAGE:
                print(f"[DISCONNECT] {addr} has disconnected.")
                connected = False
            print(f"[{addr}] {msg}")
            with clients_lock:
                for c in clients:
                    if c != conn: 
                        try:
                            c.sendall(f"[{addr}] {msg}".encode(FORMAT))
                        except socket.error:
                            print(f"[ERROR] Failed to send message to a client.")

    except socket.error as e:
        print(f"[ERROR] Connection error with {addr}: {e}")
    
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
                print(f"[DISCONNECTED] {addr} removed from clients list.")
        conn.close()


def start():
    """Starts the server and listens for new connections."""
    print('[SERVER STARTED]! Listening for connections...')
    server.listen()

    try:
        while True:
            conn, addr = server.accept() 
            with clients_lock:
                clients.add(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN] Server is shutting down.")
    finally:
        server.close()

start()
