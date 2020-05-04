# urlpatterns for leh_chat
from django.urls import include, path
from .viewsets.router import router
from .viewsets.channel import channels_router
from .viewsets.message import messages_router


urlpatterns = [
   path('', include(router.urls)),
   path('', include(channels_router.urls)),
   path('', include(messages_router.urls)),
]
