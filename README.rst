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

5. Visit http://127.0.0.1:8000/chat/ to use the app. You should have the following urls added to your url schemes::

    http://127.0.0.1:8000/chat/
    http://127.0.0.1:8000/chat/channels/
    http://127.0.0.1:8000/chat/channels/new/
    http://127.0.0.1:8000/chat/channels/<slug:slug>
    http://127.0.0.1:8000/chat/channels/<slug:channel>/messages/<slug:slug>/delete
    http://127.0.0.1:8000/chat/channels/<slug:slug>/delete
    http://127.0.0.1:8000/chat/channels/<slug:slug>/messages/new/
    http://127.0.0.1:8000/chat/memberships/
    http://127.0.0.1:8000/chat/memberships/<slug:slug>
    http://127.0.0.1:8000/chat/memberships/<slug:slug>/new/
    http://127.0.0.1:8000/chat/messages/
    http://127.0.0.1:8000/chat/messages/<slug:slug>
    http://127.0.0.1:8000/chat/messages/<slug:slug>/delete

5.1. If you've included the api urls as well, you can visit the endpoints by visiting::

    http://127.0.0.1:8000/api/channels
    http://127.0.0.1:8000/api/channels/<pk>
    http://127.0.0.1:8000/api/channels/<uuid>
    http://127.0.0.1:8000/api/channels/<pk>/messages
    http://127.0.0.1:8000/api/channels/<uuid>/messages
    http://127.0.0.1:8000/api/channels/me
    http://127.0.0.1:8000/api/group-messages
    http://127.0.0.1:8000/api/group-messages/<pk>
    http://127.0.0.1:8000/api/memberships
    http://127.0.0.1:8000/api/memberships/<uuid>
    http://127.0.0.1:8000/api/messages
    http://127.0.0.1:8000/api/messages/<pk>
    http://127.0.0.1:8000/api/messages/notes

Dependencies
------------

Use of "vestlus" requires `django-polymorphic`, `django-crispy-forms`, `django-restframework`, and `django-haystack`.
Those apps will need to be installed in the `INSTALLED_APPS` tuple of your django project.

Functionality
-------------

The app is split into three main models: `channel <vestlus/models/channel.py>`_,
`membership <vestlus/models/membership.py>`_, and `message <vestlus/models/message.py>`_.

Memberships allows users to join, leave, and administer channels. Owners and admins can manage channel memberships.

"haystack" is used to handle searching across channels and messages.