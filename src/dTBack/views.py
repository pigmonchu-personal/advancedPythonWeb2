from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_proxy.views import ProxyView


class UploadAPIProxyView(ProxyView):
    proxy_host = settings.MICROSERVICES.get("UploadMicroService")
    source = "api/1.0/upload/"
    authentication_classes = (IsAuthenticated,)