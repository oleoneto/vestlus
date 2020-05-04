=============
Lehvitus Chat
=============

`Lehvitus chat` is a django chat app with support for private and public channels.

Quick start
-----------

1. Add "leh_chat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'leh_chat',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('chat/', include('leh_chat.urls')),

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to start a new chat (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/chat/ to use the app.