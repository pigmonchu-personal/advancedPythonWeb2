
from django.test import TestCase, Client

class UploadApiTests(TestCase):

    def test_url_upload_exists(self):
        client = Client()
        response = client.post("http://localhost:8000/api/1.0/upload")
        self.assertEqual(response.status_code, 200)