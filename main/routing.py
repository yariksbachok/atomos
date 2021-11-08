from django.db.models import signals
from django.urls import re_path

from .consumers import *
from .signals import message_notification

websocket_urlpatterns = [
    re_path(r'chat/(?P<to_user>\d+)/$', ChatConsumer.as_asgi()),
    re_path('notifications', NotificationConsumer.as_asgi()),
    re_path('setOnline', SetOnline.as_asgi()),
]


signals.post_save.connect(message_notification, sender=message)
