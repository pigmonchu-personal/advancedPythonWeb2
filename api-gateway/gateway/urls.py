from django.conf.urls import url
from django.contrib import admin

from gateway.views import UploadAPIProxyView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'api/1.0/upload/$', UploadAPIProxyView.as_view(), name="upload_api"),
]
