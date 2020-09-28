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
    return JsonResponse('message': 'disconnect successfully', status=200, safe=False )


def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi',
    endpoint_url= 'https://ho60s07eke.execute-api.us-east-2.amazonaws.com/test/',
    region_name= 'us-east-2',
    aws_access_key_id= '',
    aws_secret_access_key= '')
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))


@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)['body']
    message = ChatMessage(username=body['username'], message=body['content'], timestamp=body['timestamp'])
    message.save()
    connections = Connection.objects.all()
    data = {'messages': [body]}

    for connected in connections:
        _send_to_connection(connected.connection_id, data)

    return HttpResponse('done', status=200)



@csrf_exempt
def get_recent_messages(request):
    messages = ChatMessage.objects.order_by('-id')
    chats = []

    for message in messages:
        chats.append({
            'username': message.username,
            'message': message.message,
            'timestamp': message.timestamp })

    data = {'messages': chats}

    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connection = Connection.objects.get(connection_id=connection_id)
    _send_to_connection(connection.connection_id, data)
