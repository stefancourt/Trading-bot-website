from django.urls import path

from .views import aitrade_view

urlpatterns = [
    path('', aitrade_view, name="aitrade")
]
