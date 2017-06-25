from rest_framework.routers import SimpleRouter

from microservice.views import FileUploadViewSet

router = SimpleRouter()

<<<<<<< HEAD
router.register(u'api/microservice/upload', FileUploadViewSet)
=======
router.register(u'api/1.0/upload', FileUploadViewSet)
>>>>>>> develop

urlpatterns = router.urls

