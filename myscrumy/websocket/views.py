from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage, Connection
import json
import boto3

# Create your views here.
@csrf_exempt
def test(request):
    return JsonResponse( {'message':'Hello Daud'}, status=200, safe=False)


def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads( body_unicode )


@csrf_exempt
def connect(request):
    body = _parse_body( request.body )
    connection_id = body['connectionId']
    Connection.objects.create( connection_id=connection_id )
    return JsonResponse('connect successfully', status=200, safe=False)


@csrf_exempt
def disconnect(request):
    body = _parse_body( request.body )
    connection_id = body['connectionId']
    Connection.objects.get( connection_id=connection_id).delete()
    return JsonResponse('disconnect successfully', status=200, safe=False )


def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi',
    endpoint_url= 'https://ho60s07eke.execute-api.us-east-2.amazonaws.com/test/',
    region_name= 'us-east-2',
    aws_access_key_id= '',
    aws_secret_access_key= '')
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))


@csrf_exempt
def send_message(request):
    body = _parse_body( request.body )
    chat_message = ChatMessage.objects.create( username=body['body']['username'],
    message=body['body']['message'], timestamp=body['body']['timestamp'])
    connections = [i.connection_id for i in Connection.objects.all()]
    body={'username': chat_message.username, 'message':chat_message.message, 
    'timestamp':chat_message.timestamp}
    data = {'messages':[body]}
    for connection in connections:
        _send_to_connection( connection, data)
    return JsonResponse( 'successfully sent', status=200, safe=False )


@csrf_exempt
def get_recent_messages(request):
    body = _parse_body( request.body )
    connectionId = body['connectionId']
    connection_id = Connection.objects.get(connection_id=connection_id).connection_id
    messages = list((ChatMessage.objects.get().order_by("pk")))
    if len(messages) > 5:
        data = {'messages':[{'username':chat_message.username, 'message':chat_message.message, 
        'timestamp':chat_message.timestam} for chat_message in messages[-5:]]}
    else:
        data = {'messages':[{'username':chat_message.username, 'message':chat_message.message, 
        'timestamp':chat_message.timestam} for chat_message in messages]}
    _send_to_connection(connection_id, data)
    return JsonResponse('successfully sent', status=200, safe=False)