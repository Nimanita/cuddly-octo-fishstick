from django.urls import re_path
from editor.consumers import InteractiveExecConsumer

websocket_urlpatterns = [
    re_path(r'^ws/interactive/$', InteractiveExecConsumer.as_asgi()),
]
