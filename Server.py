from ServerHandler import Handler
import socketserver


class HomeServer:

    def __init__(self, localIP, port):
        self.localIP = localIP
        self.port = port

    def run(self):
        try:
            print("Building TCP Server...")
            httpd = socketserver.TCPServer((self.localIP, self.port), Handler)

        except OSError:
            print("This IP or port is not available -> {IP}:{port}".format(IP=self.localIP, port=self.port))
            exit()
        try:
            httpd.serve_forever()
            print('Server listening on {IP}:{port}'.format(IP=self.localIP, port=self.port))
        except KeyboardInterrupt:
            httpd.server_close()
            print("Manually exited.")
