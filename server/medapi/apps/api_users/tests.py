from django.test import TestCase, Client
from django.urls import reverse

client = Client()


class UserViewTest(TestCase):
    def setUp(self):
        client.login()

    def tearDown(self):
        pass
