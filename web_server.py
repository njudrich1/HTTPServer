import socket

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000


class WebServer:
    def __init__(self, client_sock, client_address):
        self._client_address = client_address
        self._client_sock = client_sock
        self._response_complete = False
        self._DEBUG_HANDSHAKE_FLAG = False
        print("1")

    def run(self):
        while 1:
            if self._response_complete:
                print("break")
                break
            request = self._client_sock.recv(1024).decode()
            if request:             # DBG
                self.send_response()  # DBG
        self._client_sock.close()

    def send_response(self):
        response = 'HTTP/1.0 200 OK\n\nHello World'.encode("utf-8")
        self._client_sock.send(response)
        print("Response sent.")
        self._response_complete = True

    def close(self):
        self._close()

    def _close(self):
        self._client_sock.close()


def server_forever():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)
    while 1:
        try:
            client_connection, client_address = server_socket.accept()
            print(f"{client_connection}, {client_address}")
            web_server = WebServer(client_connection, client_address)
            web_server.run()
        except KeyboardInterrupt:
            web_server.close()
            server_socket.close()
            print("Server stopped.")
        except Exception as e:
            web_server.close()
            server_socket.close()
            print("Server stopped.")
            print(e)


if __name__ == "__main__":
    server_forever()
