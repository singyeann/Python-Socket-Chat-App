import socket
import time

PORT = 5050
SERVER = "localhost"  

ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    """Establish a socket connection to the server."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"[CONNECTED] Connected to server at {SERVER}:{PORT}")
        return client
    except socket.error as e:
        print(f"[ERROR] Could not connect to the server: {e}")
        return None


def send(client, msg):
    """Send a message to the server, encoded in UTF-8 format."""
    try:
        message = msg.encode(FORMAT)
        client.send(message)
        print(f"[SENT] {msg}")
    except socket.error as e:
        print(f"[ERROR] Failed to send message: {e}")


def start():
    """Starts the client application, handling message input and sending."""
    answer = input('Would you like to connect (yes/no)? ').lower()
    if answer != 'yes':
        print("Exiting...")
        return

    connection = connect()
    
    if not connection:
        return  # Exit if connection failed
    
    try:
        while True:
            msg = input("Message (q for quit): ")
            
            # If the user types 'q', disconnect from the server
            if msg.lower() == 'q':
                break
            
            send(connection, msg)
        
        # Send a disconnect message and close the connection
        send(connection, DISCONNECT_MESSAGE)
        print('Disconnecting...')
        time.sleep(1)  # Small delay for graceful closure
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        connection.close()
        print("[DISCONNECTED] Client disconnected from the server.")

start()
