from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from ...models import Channel
from ...models import GroupMessage


class GroupMessageTestCase(APITestCase):

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
        # Retrieve users
        cls.alice = get_user_model().objects.create(id=10, username="alice", email="alice@example.org")
        cls.bob = get_user_model().objects.create(id=20, username="bob", email="bob@example.org")

        # Create channel
        cls.channel = Channel.objects.create(owner=cls.alice, name='My Private Channel')

        # Create group_messages
        cls.first_message = GroupMessage.objects.create(channel=cls.channel, sender=cls.alice, content='First message')
        cls.second_message = GroupMessage.objects.create(channel=cls.channel, sender=cls.alice, content='Second message')
        cls.third_message = GroupMessage.objects.create(channel=cls.channel, sender=cls.alice, content='Third message')

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
    def test_must_authenticate_to_read_group_messages(self):
        res = self.client.get(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_must_authenticate_to_create_group_messages(self):
        res = self.client.post(self.namespace)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    ####################################################
    # Allowed operations
    def test_create_group_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.channel.id}/messages'
        res = self.client.post(url, data={'content': 'I am here now!'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list_group_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.channel.id}/messages'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['sender'], self.alice.id)
        self.assertEqual(res.data['results'][0]['channel'], self.channel.id)

    def test_retrieve_group_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.channel.id}/messages/{self.first_message.id}'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['sender'], self.alice.id)
        self.assertEqual(res.data['channel'], self.channel.id)

    def test_update_group_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.channel.id}/messages/{self.first_message.id}'
        res = self.client.patch(url, data={'content': 'Updated Message'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)  # should return 202 Accepted
        self.assertEqual(res.data['sender'], self.alice.id)
        self.assertEqual(res.data['channel'], self.channel.id)

    def test_delete_group_message(self):
        self.client.force_authenticate(user=self.alice)

        url = self.namespace + f'/{self.channel.id}/messages/{self.first_message.id}'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
