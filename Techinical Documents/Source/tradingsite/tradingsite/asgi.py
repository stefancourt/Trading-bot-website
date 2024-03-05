"""
ASGI config for tradingsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from aitrade.routing import ai_ws_urlpatterns
from trade.routing import trade_ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradingsite.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ai_ws_urlpatterns + trade_ws_urlpatterns
        )
    )
})
