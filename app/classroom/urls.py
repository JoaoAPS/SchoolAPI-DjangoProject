from rest_framework.routers import DefaultRouter

from classroom.views import ClassroomViewSet


app_name = 'classroom'

router = DefaultRouter()
router.register('classrooms', ClassroomViewSet)

urlpatterns = router.urls
