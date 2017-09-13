import pprint
import time
import pymongo
from pymongo import MongoClient
import SocketServer
import socket
import ssl
import requests
import json
from flask import Flask,json,request,Response
import threading
import boto3
from boto3.dynamodb.conditions import Key, Attr


# Initialize the Flask application
app = Flask(__name__)

#dynamoDB
dynamodbs = boto3.resource('dynamodb')
table = dynamodbs.Table('LoginTable')
clientDynamo = boto3.client('dynamodb')




class ServerRouteThread(threading.Thread):
    def init(self):
        super(ServerRouteThread, self).__init__()
        print "new ServerRoute"

    def run(self):
        route_gamer()
#
# class MyHandler(BaseHTTPRequestHandler):
#     def do_HEAD(self):
#         print "send header"
#         self.send_response(200, 'OK')
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         return
#
#     def do_GET(self):
#
#         if self.path == "/login.html":
#             try:
#                 self.do_HEAD()
#                 f = open('/home/famiglia/Scrivania/Progetto_SDCC/SDCC_20170622/login.html', 'r+')
#                 self.wfile.write(f.read())
#                 f.close()
#                 return
#             except IOError:
#                 # se non viene trovato il file, il shttps://.python.org/2/tutorial/inputoutput.htmlerver risponde con il codice di errore 404
#                 self.send_error(404, 'File Not Found: %s' % self.path)
#         else:
#             try:
#                 # f = open(curdir + sep + 'index.html', 'rb')
#                 # self.wfile.write(f.read())
#                 # f.close()
#                 return
#             except IOError:
#                 self.send_error(404, 'File Not Found: %s' % self.path)

    # def do_POST(self):
    #     print 'POST ricevuta'
    #     content_len = int(self.headers.getheader('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     print post_body
    #     json_file = json.loads(post_body)
    #     action = json_file['command']
    #     print action
    #     if action == 'login':
    #         client_user = json_file['user']
    #         client_password = json_file['pass']
    #         client = MongoClient('localhost', 27017)
    #         db = client['testDB']
    #         collection = db['foo']
    #         query_result = collection.find_one({"user": client_user, "password": client_password})
    #         print self.client_address
    #         if query_result is None:
    #             print "Mando 401"
    #             self.send_response(401, message="false")
    #             self.end_headers()
    #         else:
    #             print 'Mando 200'
    #             self.send_response(200)
    #             self.end_headers()
    #     elif action == 'new_user':
    #         client_user = json_file['user']
    #         client_password = json_file['pass']
    #         client = MongoClient('localhost', 27017)
    #         db = client['testDB']
    #         collection = db['foo']
    #         collection.insert_one({"user": client_user, "password": client_password})





    # def do_PUT(self):
    #     print 'Add Waiting Room'
    #     content_len = int(self.headers.getheader('content-length', 0))
    #     put_body = self.rfile.read(content_len)
    #     gamers.append(put_body)
    #     self.send_response(200)
    #     print gamers
    #     self.end_headers()
    #     if len(gamers) >= 1:
    #         route_gamer(self)
    #
    # def do_AUTHHEAD(self):
    #     print "send header"
    #     self.send_response(401)
    #     self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
    #     self.send_header('Content-type', 'text/html')
    #     self.end_headers()


@app.route('/login', methods=['POST'])
def user_login():
    print 'POST ricevuta'
    content_len = int(request.headers.get('content-length', 0))
    post_body = request.data
    print post_body
    # post_body = request.rfile.read(content_len)
    # print post_body
    json_file = json.loads(post_body)
    action = json_file['command']
    print action
    if action == 'login':
        client_user = json_file['user']
        client_password = json_file['pass']
        # client = MongoClient('localhost', 27017)
        # db = client['admin']
        # collection = db['foo']
        query_result = table.query(
            KeyConditionExpression=Key('Username').eq(client_user),
            FilterExpression= Attr('Password').eq(client_password)
        )
        # query_result = collection.find_one({"user": client_user, "password": client_password})
        print query_result
        result= query_result['Items']
        if result.__len__() == 0:
            print "Mando 401"
            return Response(response="false",status=401)
            # self.send_response(401, message="false")
            # self.end_headers()
        else:
            print 'Mando 200'
            return Response(status=200)
            # self.send_response(200)
            # self.end_headers()
    elif action == 'new_user':
        client_user = json_file['user']
        client_password = json_file['pass']
        # client = MongoClient('localhost', 27017)
        # db = client['admin']
        # collection = db['foo']
        # collection.insert_one({"user": client_user, "password": client_password})
        result = table.put_item(
            Item={
                'Username' : client_user,
                'Password' : client_password
            }
        )
        res = result['ResponseMetadata']
        if res['HTTPStatusCode'] == 200:
            print "Create Success"
            return Response(status=200)
        else:
            print "non bene"
            return Response(status=401)


@app.route('/newgame',methods=['POST'])
def new_game():
    print 'Add Waiting Room'
    # content_len = int(self.headers.getheader('content-length', 0))
    content_len = int(request.headers.get('content-length', 0))
    post_body = request.data
    # put_body = self.rfile.read(content_len)
    gamers.append(post_body)
    # self.send_response(200)
    r = Response(status=200)

    print gamers
    if len(gamers) == 4:
        serverThr= ServerRouteThread()
        serverThr.start()
    elif len(gamers) >= 0:
        r = Response(status=500)
        print "aosa"
    return r




def route_gamer():
    print "routing"
    for i in gamers:
        print i
        # filex = json.loads(i)
        # print filex["user"]
        # address= filex["addr"]
        # address= self.client_address
        # print address[1]
        # port = str(address[1])
        # add= "http://"+address[0]+":"+port
        # print add
        server_address = ('127.0.0.1', 8181)

        sock = socket.socket()
        nemo= True
        while nemo:

            try:
                sock.connect(server_address)

            except IOError:
                print('IOError in Socket...')
                break
                continue

            time.sleep(2)
            try:
                print "conn server ok"
                message= "'{\"message\":\"This is the message\"}'"
                m = sock.sendall(message)
                print m

                # gamers.remove(i)
                print "messaggio inviato"
                nemo = False
            finally:
                #     # fine della connessione, continua col ciclo while
                print('#########################################')
                print('###                                   ###')
                print('###        Closing  Connection        ###')
                print('###                                   ###')
                print('#########################################')
                sock.shutdown(1)
                sock.close()

            continue

        print("Closing Connection...")
        return
        # sock.shutdown(1)
        # sock.close()
        # add = "http://127.0.0.1:49454"
        # payload= {'route': 'userasa', 'index': 'ccccc'}
        # headers = {'content_length': 'payload_len', 'content-type': 'application/json', 'Connection': 'close'}
        # x = requests.post(add,json=payload, headers=headers)
        # print x


def main():
    host = 'localhost'
    port_number = 8080
    print time.asctime(), "Server Starts - %s:%s" % (host, port_number)

    global gamers
    gamers=[]

    #try:
    # server = HTTPServer(('localhost', port_number), MyHandler)

    server = app.run(host, port_number)
    # server.socket = ssl.wrap_socket(server.socket, server_side = True, certfile = curdir+sep+'server.crt', keyfile = curdir+sep+'server.key')
    print 'Started httpserver on port ', port_number
    server.serve_forever()

    #except: KeyboardInterrupt()
    print "Server has been closed"
    server.socket.close()

main()
