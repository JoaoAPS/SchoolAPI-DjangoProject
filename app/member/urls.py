from rest_framework.routers import DefaultRouter

from member.views import StudentViewSet, TeacherViewSet


app_name = 'member'

router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)

urlpatterns = router.urls
