# urlpatterns for leh_chat
from .views.routes import routes
from django.urls import path
from django.shortcuts import redirect

app_name = 'vestlus'


urlpatterns = [] + routes
