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
import datetime
import random


# Initialize the Flask application
app = Flask(__name__)

#dynamoDB
dynamodbs = boto3.resource('dynamodb')
table = dynamodbs.Table('GameTable')
elb = boto3.client('elb')
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
lock=threading.Lock()


#ServerID
serverID = "Server1"


# @app.route('/game:gameid', methods='POST')

@app.route('/generate', methods=['POST'])
def newGame():
    # content_len = int(request.headers.get('content-length', 0))
    client = {}
    post_body = request.data
    json_file = json.loads(post_body)
    client_user=json_file['user']
    client['userID'] = client_user
    instance_list= []
    nemo = True
    set = 0

    payload = {'n': round(random.randrange(1000, 100000)/10)*10}
    headers = {'content_length': 'payload_len', 'content-type': 'application/json'}
    r = requests.post('http://ec2-54-93-119-88.eu-central-1.compute.amazonaws.com:8080/generate', json=payload, timeout = None)
    print r.text
    time.sleep(2)

    return Response(status=200)


    while nemo:
        query_result = table.scan(
            FilterExpression=Attr('state').eq('Created')
        )
        result = query_result['Items']
        print result
        if result.__len__()==0:
            gameid = str(time.time()) + serverID
            result = table.put_item(
                Item={
                    'gameID': gameid,
                    'client1': client,
                    'client2': None,
                    'client3': None,
                    'client4': None,
                    'state' : 'Created'
                }
            )
            set = 1
            nemo = False
        else:
            game = result[0]
            gameid = game.get('gameID')
            #tenta di prendere il lock
            if lock.acquire():
                print 'sono nel locco'
                nemo = False
                client1 = game.get('client1')
                client2 = game.get('client2')
                client3 = game.get('client3')
                client4 = game.get('client4')
                print client2
                print client3
                instance_list.append(client1.get('instanceID'))
                if client2 == None:
                    client['userID'] = client_user
                    set = 2
                else:
                    instance_list.append(client2['instanceID'])

                if client3 == None and set == 0:
                    client['userID'] = client_user
                    set = 3
                elif client3 != None:
                    instance_list.append(client3.get('instanceID'))

                if client4 == None and set == 0:
                    client['userID'] = client_user
                    set = 4
                elif client4 != None:
                    instance_list.append(client4.get('instanceID'))


                table.update_item(
                    Key={
                        'gameID': gameid,
                    },
                    UpdateExpression='SET client%d' % set +' = :val%d' %set,
                    ExpressionAttributeValues={
                        ':val%d' % set : client
                    }
                )
                lock.release()

    instances = ec2.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        }])

    print instances

    metrics = cloudwatch.list_metrics(Namespace='AWS/EC2')
    metric_result = {}

    metricDict = []


    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            id = instance['InstanceId']
            dnsName = instance['PublicDnsName']
            print id
            if id not in instance_list:
                metric_result['id'] = id
                metric_result['DnsName'] = dnsName
                for metric in metrics:
                    cw_response = cloudwatch.get_metric_statistics(
                        Period=300,
                        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                        EndTime=datetime.datetime.utcnow(),
                        MetricName='CPUUtilization',
                        Namespace='AWS/EC2',
                        Statistics=['Average'],
                        Dimensions=[{'Name': 'InstanceId', 'Value': id}]
                    )

                    cw_response['metric_name'] = metric
                    cw_response['instance_id'] = id
                    cw = cw_response.get('Datapoints')
                    if cw is not None:
                        av = cw[1]['Average']

                metric_result['average'] = float(av)
                # metricDict.append(cw_response)

                for metric in metrics:
                    cw_response = cloudwatch.get_metric_statistics(
                        Period=300,
                        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                        EndTime=datetime.datetime.utcnow(),
                        MetricName='NetworkIn',
                        Namespace='AWS/EC2',
                        Statistics=['Average'],
                        Dimensions=[{'Name': 'InstanceId', 'Value': id}]
                    )

                    cw_response['metric_name'] = metric
                    cw_response['instance_id'] = id
                    av = cw_response['Datapoints'][1]['Average']

                metric_result['average']= float(metric_result.get('average')) + float(av)
                metricDict.append(metric_result)
                # metricDict.append(cw_response)
    print metricDict
    min = 10000
    minDNS= None
    minID = None
    for metric in metricDict:
        if metric['average'] < min:
            min = metric['average']
            minDNS= metric['DnsName']
            minID = metric['id']

    client['DnsName'] = minDNS
    client['instanceID'] = minID

    payload ='Ao mi dai due porte?'
    headers = {'content_length': 'payload_len', 'content-type': 'application/json'}
    r = requests.post('http://ec2-54-93-119-88.eu-central-1.compute.amazonaws.com:8080', json=payload, headers=headers)

    print 'val%d' % set
    print gameid

    table.update_item(
        Key={
            'gameID': gameid,
        },
        UpdateExpression='SET client%d' % set + ' = :val',
        ExpressionAttributeValues={
            ':val': client
        }
    )
    return Response(response=json.dumps(client), status=200)


    # health = load_balancer.get_instance_health()



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
