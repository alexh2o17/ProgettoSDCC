import pprint
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import pymongo
from pymongo import MongoClient
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
        json_file = json.loads(post_body)
        action = json_file['command']
        print action
        if action == 'login':
            client_user = json_file['user']
            client_password = json_file['pass']
            client = MongoClient('localhost', 27017)
            db = client['admin']
            collection = db['foo']
            query_result = collection.find_one({"user": client_user, "password": client_password})
            print self.client_address
            if query_result is None:
                print "Mando 401"
                self.send_response(401, message="false")
                self.end_headers()
            else:
                print 'Mando 200'
                self.send_response(200)
                self.end_headers()
        elif action == 'new_user':
            client_user = json_file['user']
            client_password = json_file['pass']
            client = MongoClient('localhost', 27017)
            db = client['admin']
            collection = db['foo']
            collection.insert_one({"user": client_user, "password": client_password})





    def do_PUT(self):
        print 'Add Waiting Room'
        content_len = int(self.headers.getheader('content-length', 0))
        put_body = self.rfile.read(content_len)
        gamers.append(['cis','cia'])
        gamers.append(['nico','asads'])
        self.send_response(200)
        print gamers
        print put_body
        print 'Sto nella PUT'
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

    global gamers
    gamers=[]

    #try:
    server = HTTPServer(('localhost', port_number), MyHandler)
    # server.socket = ssl.wrap_socket(server.socket, server_side = True, certfile = curdir+sep+'server.crt', keyfile = curdir+sep+'server.key')
    print 'Started httpserver on port ', port_number
    server.serve_forever()

    #except: KeyboardInterrupt()
    print "Server has been closed"
    server.socket.close()

main()
