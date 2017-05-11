from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from microservice.views import FileUploadApiView

router = SimpleRouter()

urlpatterns = [
    url(r'^api/1.0/upload/$', FileUploadApiView.as_view(), name="upload_media"),
]
# router.urls
