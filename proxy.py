import socket
import threading

def proxy_thread(client_socket):
    # Define the target server and port
    target_host = "www.example.com"
    target_port = 80

    # Create a socket to connect to the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if not client_data:
            break

        # Send the received data to the target server
        target_socket.sendall(client_data)

        # Receive the response from the target server
        target_response = target_socket.recv(4096)

        # Send the response back to the client
        client_socket.sendall(target_response)

    # Close the sockets
    client_socket.close()
    target_socket.close()

def proxy_server():
    # Define the proxy server's IP address and port
    proxy_host = "localhost"
    proxy_port = 8888

    # Create a socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)

    print(f"Proxy server is listening on {proxy_host}:{proxy_port}")

    while True:
        # Accept client connections
        client_socket, client_address = proxy_socket.accept()

        print(f"Received connection from {client_address[0]}:{client_address[1]}")

        # Create a thread to handle the client request
        client_thread = threading.Thread(target=proxy_thread, args=(client_socket,))
        client_thread.start()

# Start the proxy server
proxy_server()
