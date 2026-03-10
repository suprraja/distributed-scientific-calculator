import socket
import json
from sympy import sympify, SympifyError
from tasks.matrix_task import multiply_matrices
from tasks.system_info import get_system_info
from tasks.prime_task import handle_prime_request

# Server settings
HOST = ''           # Listen on all interfaces
PORT = 55555

# Create and configure socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}... (press Ctrl+C to stop)")

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        # Receive data until newline or connection closes
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
            # Parse incoming JSON
            message_str = data.decode('utf-8').strip()
            message = json.loads(message_str)
            command = message.get("command")
            data_payload = message.get("data", {})

            print(f"Received command: {command}")
            print(f"Data: {data_payload}")

            # Command dispatcher
            if command == "echo":
                response = {
                    "status": "success",
                    "result": f"Echo from Pi: {data_payload.get('message', 'no message')}"
                }

            elif command == "get_system_info":
                result = get_system_info()
                if result.get("status") == "success":
                    response = {
                        "status": "success",
                        "result": result
                    }
                else:
                    response = result  # carries the error
            elif command == "multiply_matrices":
                matrix_a = data_payload.get("matrix_a")
                matrix_b = data_payload.get("matrix_b")
                if matrix_a is None or matrix_b is None:
                    response = {
                        "status": "error",
                        "message": "Missing matrix_a or matrix_b in data"
                    }
                else:
                    response = multiply_matrices(matrix_a, matrix_b)
            elif command == "compute_primes":
                response = handle_prime_request(data_payload)
            elif command == "calculate":
                expr = data_payload.get("expression", "")
                try:
                    result = sympify(expr).evalf()   # .evalf() forces floating-point evaluation
                    response = {
                             "status": "success",
                             "result": float(result),      # now always a float
                             "symbolic": str(sympify(expr)),  # keep original symbolic form if you want
                             "expression": expr
                                }
                except SympifyError as se:
                    response = {"status": "error", "message": f"Cannot parse expression: {str(se)}"}
                except Exception as e:
                    response = {"status": "error", "message": f"Evaluation failed: {str(e)}"}
            else:
                response = {
                    "status": "error",
                    "message": f"Unknown command: {command}"
                }

            # Send JSON response back
            json_response = json.dumps(response) + "\n"
            client_socket.sendall(json_response.encode('utf-8'))
            print("Response sent")

        except json.JSONDecodeError as e:
            error_response = {
                "status": "error",
                "message": f"Invalid JSON: {str(e)}"
            }
            client_socket.sendall((json.dumps(error_response) + "\n").encode('utf-8'))
            print("Invalid JSON received")

        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"Server error: {str(e)}"
            }
            client_socket.sendall((json.dumps(error_response) + "\n").encode('utf-8'))
            print(f"Handling error: {e}")

    finally:
        client_socket.close()
        print("Client connection closed")


# Main server loop
try:
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)

except KeyboardInterrupt:
    print("\nServer stopped by user (Ctrl+C)")

except Exception as e:
    print(f"Server crashed: {e}")

finally:
    server_socket.close()
    print("Server socket closed. Goodbye.")
