from django.test import TestCase
import os

# Create your tests here.


class EnvironmentVariablesTests(TestCase):
    def test_client_secret_exists(self):
        assert os.environ['DMB_CLIENT_SECRET']

    def test_client_id_exists(self):
        assert os.environ['DMB_CLENT_ID']

    def test_name_exists(self):
        assert os.environ['DMB_NAME']

    def test_default_delay_exists(self):
        val = os.environ['DMB_DEFAULT_DELAY']
        assert val
        assert int(val)

    def test_url_exists(self):
        assert os.environ['DMB_URL']