from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from member.serializers import StudentDetailSerializer
from core.utils import \
    sample_student, sample_grade, sample_classroom, sample_user

from .student_urls import student_detail_url


class StudentDetailApiPositiveTests(TestCase):
    """Test the student detail api for successul requests"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.grade = sample_grade()
        self.classroom = sample_classroom()

        self.student = sample_student(fullname='Le Studant', grade=self.grade)
        self.student.classes.add(self.classroom)

        self.serializer = StudentDetailSerializer(self.student)

    def test_detail_view_positive(self):
        """Test successfully retriving the student detail view"""
        res = self.client.get(student_detail_url(self.student.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)


class StudentDetailApiNegativeTests(TestCase):
    """Test the student detail api for unsuccessful requests"""

    def test_unauthenticated_request_forbidden(self):
        """Test an authenticated request does not retrieve student detail"""
        student = sample_student()
        res = APIClient().get(student_detail_url(student.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_view_non_existing_id(self):
        """Test a student deatil request with non-existing id"""
        user = sample_user()
        client = APIClient()
        client.force_authenticate(user)
        res = client.get(student_detail_url(999))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
