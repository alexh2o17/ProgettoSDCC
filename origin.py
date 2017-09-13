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
table = dynamodbs.Table('GameTable')

#ServerID
serverID = "Server1"


# @app.route('/game:gameid', methods='POST')

@app.route('/generate', methods='POST')
def newGame(self):
    # content_len = int(request.headers.get('content-length', 0))
    post_body = request.data
    json_file = json.loads(post_body)
    client_user=json_file['Username']
    query_result = table.scan(
        FilterExpression=Attr('state').eq('Created')
    )
    result = query_result['Items']
    if result.__len__()==0:
        gameid = time.time() + serverID
        result = table.put_item(
            Item={
                'gameID': gameid,
                'client1': client_user
            }
        )
    else:
        game = result[0];
        gameid = game['gameid']
        client1 = game['client1']
        client2 = game['client2']
        client3 = game['client3']
        client4 = game['client4']
        if(client2 == None):
            client2 = client_user
        elif(client3 == None):
            client3 = client_user
        elif(client4 == None):
            client4 = client_user
        table.update_item(
            Key={
                'gameid': gameid,
            },
            UpdateExpression='SET client1 = :val1 AND client2 = :val2 AND client3 = :val3 client4 = :val4',
            ExpressionAttributeValues={
                ':val1': client1,
                ':val2': client2,
                ':val3': client3,
                ':val4': client4
            }
        )



def main():
    host = 'localhost'
    port_number = 8181
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
