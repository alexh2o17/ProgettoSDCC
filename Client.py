import socket
import sys
import requests
import remi.gui as gui
from remi import start, App


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width = 500, height = 300)
        self.lbl = gui.Label('Murgia 2-3')
        self.lblName = gui.Label('Nome Utente')
        self.name= gui.Input('name')
        self.lblPwd = gui.Label('Password')
        self.pwd = gui.Input('password')
        self.bt = gui.Button('Login')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.lblName)
        container.append(self.name)
        container.append(self.lblPwd)
        container.append(self.pwd)
        container.append(self.bt)

        # returning the root widget
        return container



    # listener function
    def on_button_pressed(self, widget):
        payload = {'user': self.name.get_value(), 'pass': self.pwd.get_value()}
        print payload
        payload_len = len(payload)
        headers = {'content_length': 'payload_len', 'content-type': 'application/json', 'Connection': 'close'}
        r = requests.post('http://localhost:8080', json=payload, headers=headers)
        print r.headers
        self.lbl.set_text('Asensio 1-4!')

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



