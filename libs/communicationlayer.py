import socket
from threading import Thread
import threading
import json

class ServerSocket:
    def __init__(self, server_queue, host=socket.gethostbyname(socket.gethostname()) , port=64219):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.ack_received = threading.Event()
        self.server_queue = server_queue
        
        self.ack_received.set()

        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        def send_data():
            while True:
                try:
                    #waiting for the ACK from the client before sending data
                    while not self.ack_received.is_set():
                        pass
                    # If the server queue is not empty, send data to the client
                    if not self.server_queue.empty():    
                        row_data = self.server_queue.get()
                        json_data = json.dumps(row_data).encode('utf-8')
                        client_socket.send(json_data)
                        print(f"[SENT] {json_data}", flush=True)
                        self.ack_received.clear()   
                except Exception as e:
                    print(f"Error sending data: {e}", flush=True)
                    break        
            client_socket.close()

        def recv_ack():
            while True:
                try:
                    msg = client_socket.recv(1024).decode("utf-8")
                    if msg.strip() == "ACK":
                        print("ACK received", flush=True)
                        # Set the event to indicate ACK was received
                        self.ack_received.set()
                except Exception as e:
                    print(f"Error receiving ACK: {e}", flush=True)
                    break            
            client_socket.close()

        send_thread = Thread(target=send_data)  
        recv_thread = Thread(target=recv_ack)
        send_thread.start()
        recv_thread.start()
        send_thread.join()
        recv_thread.join()
        client_socket.close()
        print("Client disconnected")

class ClientSocket:
    def __init__(self, client_queue, host=socket.gethostbyname(socket.gethostname()), port=64219):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_queue = client_queue
        print(f"Connected to server at {self.host}:{self.port}")
        self.data_received = threading.Event()

    def start(self):
        Thread(target=self.recv_data).start()
        Thread(target=self.send_ack).start()

    def recv_data(self):
        while True:
            try:    
                msg = self.client_socket.recv(1024).decode("utf-8")
                if msg:
                    row_data = json.loads(msg)
                    print(f"[RECEIVED] {msg}", flush=True)
                    self.client_queue.put(list(row_data))
                    # Set the event to indicate data was received
                    self.data_received.set()  
            except Exception as e:
                print(f"Error receiving data: {e}", flush=True)
                break
        self.client_socket.close()

    def send_ack(self):
        while True:
            try:
                # Wait until data is received before sending ACK
                while not self.data_received.is_set():
                    pass
                self.client_socket.send("ACK".encode('utf-8'))  # Send ACK back to server
                print("ACK sent", flush=True)
                self.data_received.clear()  
            except Exception as e:
                print(f"Error sending ACK: {e}", flush=True)
                break    
        self.client_socket.close()
    
