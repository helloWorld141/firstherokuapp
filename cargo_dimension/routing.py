from channels.routing import route
from api.consumers import ws_connect, ws_disconnect, ws_receive


channel_routing = [
    route('websocket.connect', ws_connect, path=r"^/(?P<user>[a-zA-Z0-9_]+)/$"),
    route('websocket.disconnect', ws_disconnect, path=r'^/(?P<user>[a-zA-Z0-9_]+)/$'),
    route('websocket.receive', ws_receive, path=r'^/(?P<user>[a-zA-Z0-9_]+)/$')
]