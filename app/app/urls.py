from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grades/', include('grade.urls')),
    path('classrooms/', include('classroom.urls')),
    path('members/', include('member.urls')),
]
