from django.test import TestCase
from django.contrib.auth import get_user_model
from ..message import Message
from ..message import PrivateMessage


class MessageTestCase(TestCase):
    def setUp(self):
        self.alice = get_user_model().objects.create(id=10, username="alice", email="alice@example.org")
        self.bob = get_user_model().objects.create(id=55, username="bob", email="bob@example.org")

    def test_send_private_message(self):
        PrivateMessage.objects.create(
            sender=self.alice,
            recipient=self.bob,
            content='Hi friend!'
        )
        self.assertEqual(Message.objects.last(), PrivateMessage.objects.last())

    def test_save_private_note_without_recipient(self):
        message = PrivateMessage.objects.create(
            sender=self.alice,
            content='Note to self'
        )
        self.assertEqual(message.recipient, None)

    def test_save_private_note_with_recipient(self):
        message = PrivateMessage.objects.create(
            sender=self.alice,
            recipient=self.alice,
            content='Note to self'
        )
        self.assertEqual(message.recipient, message.sender)
