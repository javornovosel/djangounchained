"""
ASGI config for onepiecetcg project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import draft.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onepiecetcg.settings')

application = ProtocolTypeRouter({
	'http' : get_asgi_application(),
	'websocket': AuthMiddlewareStack(
		URLRouter(
			draft.routing.websocket_urlpatterns 
			#if you want to add more routings from other applications use + x.routing.websocket_urlpatterns
		))
})
