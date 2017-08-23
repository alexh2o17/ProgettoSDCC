import socket
import sys
import requests
import remi.gui as gui
from remi import start, App
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print "send header"
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_POST(self):
        print "ciao"
        self.send_response(200, 'OK')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.container = gui.VBox(width = 500, height = 300)
        self.lbl = gui.Label('Murgia 2-3')
        self.lblName = gui.Label('Nome Utente')
        self.name= gui.Input('name')
        self.lblPwd = gui.Label('Password')
        self.pwd = gui.Input('password')
        self.bt = gui.Button('Login')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        self.container.append(self.lbl)
        self.container.append(self.lblName)
        self.container.append(self.name)
        self.container.append(self.lblPwd)
        self.container.append(self.pwd)
        self.container.append(self.bt)

        # returning the root widget
        return self.container


    # listener function
    def on_button_pressed(self, container):
        payload = {'user': self.name.get_value(), 'pass': self.pwd.get_value()}
        print payload
        payload_len = len(payload)
        headers = {'content_length': 'payload_len', 'content-type': 'application/json', 'Connection': 'close'}
        r = requests.post('http://localhost:8080', json=payload, headers=headers)
        print r.headers
        print r.status_code
        if r.status_code == 200:
            print 'Prepara la nuova pagina per il client'
            self.user = self.name.get_value()
            self.lbl.set_text(self.user)

            self.container.remove_child(self.lblName)
            self.container.remove_child(self.lblPwd)
            self.container.remove_child(self.name)
            self.container.remove_child(self.pwd)
            self.container.remove_child(self.bt)

            self.create = gui.Button('Play')
            self.create.set_on_click_listener(self.on_create_pressed)
            self.container.append(self.create)
        else:
            print 'Reinserisci le credenziali di accesso'
        # container.append(self.create)
        # # x = False
        # # while x is False:
        # response = self.rfile.read()
        # #     if response == ("false" or 'true'):
        # #         x = True
        # print response

    def on_create_pressed(self, widget):
        payload = {'user': self.user, 'addr': self.client_address}
        print payload
        headers = {'content_length': 'payload_len', 'content-type': 'application/json', 'Connection': 'close'}
        r = requests.put('http://localhost:8080', json=payload, headers=headers)
        print r.headers

# starts the webserver
start(MyApp, standalone="true")

# list_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# list_sock_addr = ('localhost', 10000)
# list_sock.bind(list_sock_addr)
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 8080)
# print 'Connecting to %s port %s' % server_address
# sock.connect(server_address)
# username = raw_input('Inserisci il tuo username ')
# password = raw_input('Inserisci la tua password ')
# payload = {'user': username, 'pass': password}
# payload_len = len(payload)
# headers = {'content_length': 'payload_len', 'content-type': 'application/json', 'Connection':'close'}
# r = requests.post('http://localhost:8080', json=payload, headers=headers)
# print r.headers
#r.raw.read(10)
#print 'Sto per chiudere la socket'
#sock.close()
#data = sock.recv(1024)
#print data
#print 'Richiesta inviata'



