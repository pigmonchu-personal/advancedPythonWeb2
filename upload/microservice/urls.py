from rest_framework.routers import SimpleRouter

from microservice.views import FileUploadViewSet

router = SimpleRouter()

router.register(u'api/1.0/upload', FileUploadViewSet)

urlpatterns = router.urls

