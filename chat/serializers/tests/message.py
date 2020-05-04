from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from ...models import PrivateMessage


class MessageTestCase(APITestCase):

    # The client used to connect to the API
    client = APIClient()

    def setUp(self):
        """
        Prepare database and client.
        """

        # API endpoint
        self.namespace = '/v1/messages'

    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.alice = get_user_model().objects.create(id=10, username="alice", email="alice@example.org")
        cls.bob = get_user_model().objects.create(id=20, username="bob", email="bob@example.org")

        # Create messages
        cls.message1 = PrivateMessage.objects.create(sender=cls.alice, content="1 to 1")
        cls.message2 = PrivateMessage.objects.create(sender=cls.bob, content="2 to 2")
        cls.message3 = PrivateMessage.objects.create(sender=cls.bob, receiver=cls.alice, content="2 to 1")

    def tearDown(self):
        try:
            with transaction.atomic():
                PrivateMessage.objects.all().delete()
                get_user_model().objects.all().delete()
        except transaction.Error:
            pass

    ####################################################
    # Require authentication
    def test_must_authenticate_to_read_messages(self):
        res = self.client.get(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_must_authenticate_to_create_messages(self):
        res = self.client.post(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    ####################################################
    # Allowed operations
    def test_create_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace
        res = self.client.post(url, data={'content': 'Message'})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['sender'], self.alice.id)
        self.assertEqual(res.data['receiver'], None)

    def test_list_messages(self):
        self.client.force_authenticate(user=self.alice)

        res = self.client.get(self.namespace)

        # All messages for or by this user
        messages = [mine for mine in res.data['results']
                    if mine['sender'] == self.alice.id
                    or mine['receiver'] == self.alice.id]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], messages)  # Ensure user is in all messages

    def test_list_personal_notes(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/notes'
        res = self.client.get(url)

        # All messages for or by alice
        messages = [mine for mine in res.data['results']
                    if mine['sender'] == self.alice.id and
                    (mine['receiver'] == self.alice.id or mine['receiver'] is None)]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], messages)

    def test_read_message_sent_by_alice(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message1.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['sender'], self.alice.id)
        self.assertEqual(res.data['receiver'], None)
        self.assertEqual(res.data['content'], '1 to 1')

    def test_read_message_sent_to_alice(self):
        self.client.force_authenticate(user=self.bob)

        url = self.namespace + f'/{self.message3.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['sender'], self.bob.id)
        self.assertEqual(res.data['receiver'], self.alice.id)
        self.assertEqual(res.data['content'], '2 to 1')

    def test_update_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message1.id}'
        res = self.client.patch(url, data={'content': 'Updated message'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # Should return 202 Accepted
        self.assertEqual(res.data['content'], 'Updated message')

    def test_delete_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message1.id}'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    ####################################################
    # Forbidden operations
    def test_forbid_alice_from_reading_bobs_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message2.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_forbid_alice_from_updating_bobs_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message2.id}'
        res = self.client.patch(url, data={'content': 'Updated message'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_forbid_alice_from_deleting_bobs_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.message2.id}'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
