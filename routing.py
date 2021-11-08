from channels.routing import route
from channels.routing import ProtocolTypeRouter, URLRouter
from main.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})