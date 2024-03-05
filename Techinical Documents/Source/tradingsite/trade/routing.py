from django.urls import path

from .consumers import GraphConsumer

trade_ws_urlpatterns = [
    path('ws/trade/', GraphConsumer.as_asgi())
]