"""
 Implements a simple HTTP/1.0 Server
"""

import socket

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080


def handle_request(request):
    """Handles the HTTP request."""

    headers = request.split('\n')
    filename = headers[0].split()[1]
    if filename == '/':
        filename = '/main.py'

    try:
        content = open(filename[1:]).read()
        response = f'HTTP/1.0 200 OK\n\n{content}'
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    return response

def main():

    # Create socket
    #AF_INET: sets the host and port format
    #SOCK_STREAM: Sets the socket type
    #This creates a socket reference
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #configure the socket
    #SOL_SOCKET : sets socket option, not protocol options for all sockets
    #SO_REUSEADDR - reuse existing sockets for new requests
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Configures the socket to listen on the SERVER_HOST and SERVER_PORT
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    #enables the socket to accept connections
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        # From Python Docs: 
        # For best match with hardware and network realities, the value [passed to recv] should be a relatively small power of 2, for example, 4096
        #data comes across the network as bytes, not string, so they must be encoded back into strings
        request = client_connection.recv(4096).decode()
        print(f"client: {client_address} request:{request}")

        # Return an HTTP response
        response = handle_request(request)
        client_connection.sendall(response.encode())

        # Close connection
        client_connection.close()

    # Close socket
    server_socket.close()
    
if __name__ == "__main__":
    main()