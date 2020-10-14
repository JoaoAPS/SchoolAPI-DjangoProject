from rest_framework.routers import DefaultRouter

from member.views import StudentViewSet


app_name = 'member'

router = DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = router.urls
