# Django Vestlus

**vestlus** is a django chat app with support for private and public channels.

![PyPI - License](https://img.shields.io/pypi/l/vestlus)
![PyPI - Version](https://img.shields.io/pypi/v/vestlus)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vestlus)
![Github - Issues](https://img.shields.io/github/issues/lehvitus/vestlus)
![PyPI - Downloads](https://img.shields.io/pypi/dm/vestlus)

#### Dependencies
Use of **vestlus** requires:
- `django-polymorphic`: used to handle inheritance between message models.
- `django-crispy-forms`: used for better formatting of forms in templates.
- `django-restframework`: used to provide REST api support.
- `django-haystack`: used to handle searching across channels and messages.

Those apps will need to be installed in the ``INSTALLED_APPS`` tuple of your django project.


#### Models
The app is split into three main models:
- [channel](vestlus/models/channel.py): channels allow for group conversations. Any message sent to a channel
is visible to every member of the channel. Channels can be either public or private.
- [membership](vestlus/models/membership.py): memberships allow users to join, leave, and administer channels.
Owners and admins can manage channel memberships.
- [message](vestlus/models/message.py): all messages are private (self to self); private (shared with somebody else); or 


#### Installation
1. Add **vestlus** to your `INSTALLED_APPS` setting like this::
```python
    INSTALLED_APPS = [
        # other apps...
        'vestlus',
    ]
```

Alternatively, you can also add this app like so::
```python
    INSTALLED_APPS = [
        # other apps...
        'vestlus.apps.VestlusConfig',
    ]
```

2. Include the polls URLconf in your project urls.py like this::
```python
    path('chat/', include('vestlus.urls', namespace='vestlus')),
```

2.1. Optionally, you can also add the api endpoints in your project urls.py like so::
```python
    path('api/', include('vestlus.api', namespace='vestlus_api')),
```

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)
   to start a add chat groups and messages (you'll need the Admin app enabled).

5. Visit [`http://127.0.0.1:8000/chat/`](http://127.0.0.1:8000/admin/) to use the app. You should have the following urls added to your url schemes::
```
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
```

5.1. If you've included the api urls as well, you can visit the endpoints by visiting::
```
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
```

## License
**vestlus** is [BSD-Licensed](LICENSE.md).

------

Built with [django-clite](https://github.com/oleoneto/django-clite).

Developed and maintained by [Leo Neto](https://github.com/oleoneto)
