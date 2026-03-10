import socket

# --- Server settings ---
HOST = ''           # Listen on ALL interfaces (important!)
PORT = 55555        # Our chosen port

# Step 1: Create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

# Step 2: Bind it to address + port
server_socket.bind((HOST, PORT))
print(f"Socket bound to port {PORT}")

# Step 3: Start listening (backlog = max queued connections)
server_socket.listen(1)
print(f"Server is now listening on port {PORT}...")

# Step 4: Wait for a client to connect
print("Waiting for a connection...")
client_socket, client_address = server_socket.accept()
print(f"Connected by client: {client_address}")

# Step 5: Receive data from client (up to 1024 bytes)
data = client_socket.recv(1024)
if data:
    message = data.decode('utf-8')
    print(f"Received from client: {message}")

    # Step 6: Send a reply
    reply = f"Hello from Raspberry Pi! You said: {message}"
    client_socket.sendall(reply.encode('utf-8'))
    print("Reply sent")

# Step 7: Close connection
client_socket.close()
print("Connection closed")

# Optional: close server socket too (for this simple version)
server_socket.close()
print("Server shut down")
