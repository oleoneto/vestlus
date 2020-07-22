# urlpatterns for vestlus
from django.urls import path
from django.shortcuts import redirect
from .views.routes import routes

app_name = 'vestlus'


urlpatterns = [] + routes
