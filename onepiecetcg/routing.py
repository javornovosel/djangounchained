from django.urls import re_path, include
#from draft.routing import websocket_urlpatterns as draft_up
import draft.routing
websocket_urlpatterns = [
	re_path(r'^', include(draft.routing.websocket_urlpatterns))
]