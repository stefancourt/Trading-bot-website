from django.urls import path

from .consumers import GraphConsumer

ai_ws_urlpatterns = [
    path('ws/ai-trade/', GraphConsumer.as_asgi())
]