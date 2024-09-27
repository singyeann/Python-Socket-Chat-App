import socket

PORT = 5050
SERVER = "localhost"  
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"[CONNECTED] Connected to server at {SERVER}:{PORT}")
        return client
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return None

def start():
    connection = connect()
    if connection is None:
        return  # Exit if connection couldn't be established
    
    try:
        while True:
            # Receiving messages from the server
            msg = connection.recv(1024).decode(FORMAT)
            
            if msg:
                print(msg)
                
                # Check if server sent a disconnect message
                if msg == DISCONNECT_MESSAGE:
                    print("[SERVER DISCONNECTED] Server has closed the connection.")
                    break
            else:
                # Handle cases where the connection might drop
                print("[CONNECTION LOST] Connection to server was lost.")
                break
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        connection.close()
        print("[DISCONNECTED] Client disconnected from the server.")

start()
