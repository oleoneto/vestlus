# urlpatterns for vestlus
from django.urls import include, path
from .viewsets.router import router

app_name = 'vestlus'

urlpatterns = [
   path('', include(router.urls)),
]
