from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('connect/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('send_message/', views.send_message, name='send message'),
    path('get_recent_messages/', views.get_recent_messages, name='get recent messages'),
]

#unsafe:wss://ho60s07eke.execute-api.us-east-2.amazonaws.com/test  -> websocket url
#https://ho60s07eke.execute-api.us-east-2.amazonaws.com/test/@connections  -> connection url
#wscat testing -> wscat -c wss://ho60s07eke.execute-api.us-east-2.amazonaws.com/test

# wscat -c wss://ho60s07eke.execute-api.us-east-2.amazonaws.com
# {"action":"sendMessage", "username":"Rose","content":"Hello all”","timestamp":"4:00 PM"}
# {"action": "getRecentMessages"}