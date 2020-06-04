from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from ...models import Channel, GroupMessage


class ChannelTestCase(APITestCase):
    # The client used to connect to the API
    client = APIClient()

    def setUp(self):
        """
        Prepare database and client.
        """

        # API endpoint
        self.namespace = '/v1/channels'

    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.alice = get_user_model().objects.create(id=10, username="alice", email="alice@example.org")
        cls.bob = get_user_model().objects.create(id=20, username="bob", email="bob@example.org")

        # Create channels
        cls.alice_channel = Channel.objects.create(name='Private Group by Alice', owner=cls.alice)
        cls.bob_channel = Channel.objects.create(name='Private Group by Bob', owner=cls.bob)
        cls.public_channel = Channel.objects.create(name='Public Group by Bob', owner=cls.bob, is_private=False)

        # Create messages in channels
        GroupMessage.objects.create(sender=cls.alice, channel=cls.alice_channel, content='I am Alice!')
        GroupMessage.objects.create(sender=cls.bob, channel=cls.bob_channel, content='I am Bob!')
        GroupMessage.objects.create(sender=cls.bob, channel=cls.public_channel, content='Public Forum')

    def tearDown(self):
        try:
            with transaction.atomic():
                Channel.objects.all().delete()
                GroupMessage.objects.all().delete()
                get_user_model().objects.all().delete()
        except transaction.Error:
            pass

    ####################################################
    # Require authentication
    def test_must_authenticate_to_read_channel(self):
        res = self.client.get(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_must_authenticate_to_create_channel(self):
        res = self.client.post(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    ####################################################
    # Allowed operations: Channel
    def test_create_private_channel(self):
        self.client.force_authenticate(user=self.alice)

        res = self.client.post(self.namespace, data={'name': 'My Channel'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'My Channel')
        self.assertEqual(res.data['owner'], self.alice.id)
        self.assertEqual(res.data['is_private'], True)

    def test_create_public_channel(self):
        self.client.force_authenticate(user=self.alice)

        res = self.client.post(self.namespace, data={'name': 'My Channel', 'is_private': False})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'My Channel')
        self.assertEqual(res.data['owner'], self.alice.id)
        self.assertEqual(res.data['is_private'], False)

    def test_retrieve_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.alice_channel.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['owner'], self.alice.id)
        self.assertEqual(res.data['id'], self.alice_channel.id)

    def test_list_channel(self):
        self.client.force_authenticate(user=self.alice)
        res = self.client.get(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.alice_channel.id}'
        res = self.client.patch(url, data={'name': 'Personal Channel'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.alice_channel.id)
        self.assertEqual(res.data['name'], 'Personal Channel')

    def test_delete_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.alice_channel.id}'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    ####################################################
    # Allowed operations: Channel Messages
    def test_read_messages_on_my_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.alice_channel.id}/messages'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_read_messages_on_public_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.public_channel.id}/messages'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['channel'], self.public_channel.id)
        self.assertEqual(res.data['results'][0]['sender'], self.bob.id)

    ####################################################
    # Handle memberships
    def test_bob_can_add_alice(self):
        self.client.force_authenticate(user=self.bob)

        url = self.namespace + f'/{self.bob_channel.id}/members'
        res = self.client.post(url, data={'user': self.alice.id})

        self.assertEqual(res.data['user'], self.alice.id)
        self.assertEqual(res.data['invited_by'], self.bob.id)

    def test_bob_can_add_alice_as_admin(self):
        self.client.force_authenticate(user=self.bob)

        url = self.namespace + f'/{self.bob_channel.id}/members'
        res = self.client.post(url, data={'user': self.alice.id, 'is_admin': True})

        self.assertEqual(res.data['user'], self.alice.id)
        self.assertEqual(res.data['invited_by'], self.bob.id)
        self.assertEqual(res.data['is_admin'], True)

    def test_alice_can_post_to_a_public_channel(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.public_channel.id}/messages'
        res = self.client.post(url, data={'content': 'I can post on this public channel!'})
        self.assertEqual(res.data['channel'], self.public_channel.id)

    ####################################################
    # Forbidden operations
    def test_prevent_bob_from_retrieving_alices_channel(self):
        self.client.force_authenticate(user=self.bob)

        url = self.namespace + f'/{self.alice_channel.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_prevent_bob_from_updating_alices_channel(self):
        self.client.force_authenticate(user=self.bob)

        url = self.namespace + f'/{self.alice_channel.id}'
        res = self.client.patch(url, data={'name': 'Updated Channel'})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
