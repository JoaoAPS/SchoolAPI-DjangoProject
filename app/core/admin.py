from django.contrib import admin

from member.models import Member, Student, Teacher
from grade.models import Grade
from classroom.models import Classroom


admin.site.register(Member)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Classroom)
