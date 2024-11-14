# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from dotenv import load_dotenv

from dsaSLN.routing import websocket_urlpatterns

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DSA.settings')

application = ProtocolTypeRouter({
    # For HTTP requests, use Django's ASGI application
    "http": get_asgi_application(),

    # For WebSocket requests, use Channels' routing mechanism
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                 websocket_urlpatterns 
                
            )
        )
    ),
})
