from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Student
from member.serializers import StudentListSerializer# , StudentDetailSerializer
from core.utils import \
    sample_student_payload, sample_student, sample_grade, sample_classroom


STUDENT_LIST_URL = reverse('member:student-list')


def student_detail_url(student_id):
    return reverse('member:student-detail', args=[student_id])


def sample_user():
    return get_user_model().objects.create(
        username='Test User',
        password='TestPass'
    )
