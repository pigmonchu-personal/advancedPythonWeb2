# He creado esta vista como proxy de entrada para distribuir el tráfico
# Su única misión en ver si el usuario está autenticado
from rest_framework.permissions import IsAuthenticated
from rest_framework_proxy.views import ProxyView

from django.conf import settings


class UploadAPIProxyView(ProxyView):

    proxy_host = settings.MICROSERVICES.get('UploadMicroservice')
    source = "api/1.0/upload/" #Debería sustituirse por un service discovery
    authentication_classes = (IsAuthenticated, )


