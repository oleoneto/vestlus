from rest_framework import routers

"""
Your router endpoints are automatically added to the urlpatterns in urls.py for this app.
To make your app's urls available to the entire project, include your app urls in the urlpatterns for your project:

In your project's urls.py file:

from django.urls import include, path
urlpatterns = [
   # Other paths like admin and login stuff...
   path('social', include('.social.urls'))
]
"""

router = routers.SimpleRouter(trailing_slash=False)
