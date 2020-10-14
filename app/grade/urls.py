from rest_framework.routers import DefaultRouter

from .views import GradeApiViewSet

app_name = 'grade'
router = DefaultRouter()
router.register(r'', GradeApiViewSet)

urlpatterns = router.urls
