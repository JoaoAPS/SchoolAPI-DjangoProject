from django.db import models
from django.utils.translation import gettext_lazy as _

from grade.models import Grade
from classroom.models import Classroom


class Member(models.Model):
    """A generic member of the school"""
    _sex_choices = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]

    fullname = models.CharField(max_length=100)
    id_doc = models.CharField(max_length=50, unique=True)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1, choices=_sex_choices)
    monthly_payment = models.DecimalField(decimal_places=2, max_digits=8)
    active = models.BooleanField(default=True)
    register_date = models.DateField(auto_now_add=True)
    departure_date = models.DateField(null=True, default=None)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    @property
    def firstname(self):
        return self.fullname.split(' ')[0]

    def __str__(self):
        return self.fullname


class Student(Member):
    """A student of the school"""
    grade = models.ForeignKey(
        Grade,
        null=True,
        on_delete=models.SET_NULL,
        related_name='students',
    )
    guardian1 = models.CharField(max_length=100)
    guardian2 = models.CharField(max_length=100, blank=True)
    classes = models.ManyToManyField(Classroom, related_name='students')


class Teacher(Member):
    """A teacher of the school"""
    _academic_level_choices = [
        ('Gr', 'Graduate'),
        ('Ms', 'Master'),
        ('Dr', 'Docter'),
    ]

    academic_level = models.CharField(
        max_length=2,
        choices=_academic_level_choices
    )
    bank_agency = models.PositiveIntegerField()
    bank_account = models.PositiveIntegerField()
    classes = models.ManyToManyField(Classroom, related_name='teachers')
