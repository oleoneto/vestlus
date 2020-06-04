==============
Django Vestlus
==============

`Django Vestlus` is a django chat app with support for private and public channels.

Quick start
-----------

1. Add "vestlus" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'vestlus',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('chat/', include('vestlus.urls', namespace='vestlus')),

2.1. Optionally, you can also add the api endpoints in your project urls.py like so::

    path('api/', include('vestlus.api', namespace='vestlus_api')),

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to start a add chat groups and messages (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/chat/ to use the app.

5.1. If you've included the api urls as well, you can visit the endpoints by visiting::

    https://127.0.0.1:8000/api/channels
    https://127.0.0.1:8000/api/channels/<pk>
    https://127.0.0.1:8000/api/channels/<pk>/messages
    https://127.0.0.1:8000/api/channels

Dependencies
------------

Use of "vestlus" requires `django-polymorphic`, `django-crispy-forms`, and `django-restframework`.
Those apps will need to be installed in the `INSTALLED_APPS` tuple of your django project.

Functionality
-------------

The app is split into three main models: `channel <vestlus/models/channel.py>`_,
`membership <vestlus/models/membership.py>`_, and `message <vestlus/models/message.py>`_.
