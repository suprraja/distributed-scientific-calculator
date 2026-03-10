import socket
import json

HOST = ''
PORT = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}... (Ctrl+C to stop)")

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        # Receive data until newline or timeout
        data = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk
            if b'\n' in chunk:
                break

        if not data:
            print("Empty message received")
            return

        try:
            message = json.loads(data.decode('utf-8').strip())
            command = message.get("command")
            data_payload = message.get("data", {})

            print(f"Received command: {command}")
            print(f"Data: {data_payload}")

            # Simple command handling
            if command == "echo":
                response = {
                    "status": "success",
                    "result": f"Echo from Pi: {data_payload.get('message', 'no message')}"
                }
            else:
                response = {
                    "status": "error",
                    "message": f"Unknown command: {command}"
                }

            # Send JSON response
            json_response = json.dumps(response) + "\n"
            client_socket.sendall(json_response.encode('utf-8'))
            print("Response sent")

        except json.JSONDecodeError:
            response = {"status": "error", "message": "Invalid JSON"}
            client_socket.sendall((json.dumps(response) + "\n").encode('utf-8'))
            print("Invalid JSON received")

    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()
        print("Client connection closed")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)

except KeyboardInterrupt:
    print("\nServer stopped by user")

finally:
    server_socket.close()
    print("Server shut down")
