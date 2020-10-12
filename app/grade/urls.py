from rest_framework.routers import DefaultRouter

from .views import GradeApiViewSet

app_name = 'grades'
router = DefaultRouter()
router.register(r'grades', GradeApiViewSet)

urlpatterns = router.urls
