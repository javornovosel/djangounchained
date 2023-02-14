from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	#re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
	#re_path(r'ws/draft/lobby/$', consumers.ChatConsumer.as_asgi()),
	re_path(r'ws/draft/lobby/(?P<room_name>\w+)/$', consumers.ChatroomConsumer.as_asgi())
]