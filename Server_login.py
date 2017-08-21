from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import SocketServer
import socket
import ssl
import requests
import json


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print "send header"
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_GET(self):

        if self.path == "/login.html":
            try:
                self.do_HEAD()
                f = open('/home/famiglia/Scrivania/Progetto_SDCC/SDCC_20170622/login.html', 'r+')
                self.wfile.write(f.read())
                f.close()
                return
            except IOError:
                # se non viene trovato il file, il shttps://.python.org/2/tutorial/inputoutput.htmlerver risponde con il codice di errore 404
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            try:
                # f = open(curdir + sep + 'index.html', 'rb')
                # self.wfile.write(f.read())
                # f.close()
                return
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        print 'POST ricevuta'
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = ('localhost', 10000)
        # sock.connect(server_address)
        # sock.sendall('Ciao, sono il server')
        self.send_response(200)
        print 'Risposta partita'
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()


def main():
    host = 'localhost'
    port_number = 8080
    print time.asctime(), "Server Starts - %s:%s" % (host, port_number)

    #try:
    server = HTTPServer(('localhost', port_number), MyHandler)
    # server.socket = ssl.wrap_socket(server.socket, server_side = True, certfile = curdir+sep+'server.crt', keyfile = curdir+sep+'server.key')
    print 'Started httpserver on port ', port_number
    server.serve_forever()

    #except: KeyboardInterrupt
    #print "Server has been closed"
    server.socket.close()

main()
