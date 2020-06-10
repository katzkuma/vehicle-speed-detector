from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import website.routing

application = ProtocolTypeRouter({
  # correspond the list of url to channels package
  'websocket': AuthMiddlewareStack(
    URLRouter(
      website.routing.websocket_urlpatterns
    )
  ),
})