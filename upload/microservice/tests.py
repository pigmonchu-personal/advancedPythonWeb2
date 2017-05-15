from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from rest_framework.reverse import reverse


class UploadApiTests(TestCase):

    def test_url_upload_without_file_error(self):
        client = Client()
        response = client.post(reverse("upload_media"))
        print(response)
        self.assertEqual(response.status_code, 400)

    def test_url_upload_with_incorrect_file_type(self):
# http://blog.hayleyanderson.us/2015/07/18/validating-file-types-in-django/

        client = Client()
        data = {
            'file':  SimpleUploadedFile("post.pdf", "pdf_document".encode(), content_type="application/pdf")
        }
        response = client.post(reverse("upload_media"), data, format="raw")
        print(response)
        self.assertEqual(response.status_code, 400)

    def test_url_upload_with_correct_file_type(self):
# http://blog.hayleyanderson.us/2015/07/18/validating-file-types-in-django/

        client = Client()
        data = {
            'file':  SimpleUploadedFile("post.png", "png_document".encode(), content_type="image/png")
        }
        response = client.post(reverse("upload_media"), data, format="raw")
        print(response)
        self.assertEqual(response.status_code, 201)

