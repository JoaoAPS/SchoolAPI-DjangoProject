from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Student
from core.utils import sample_student, sample_user


def student_detail_url(student_id):
    return reverse('member:student-detail', args=[student_id])


class StudentDeleteApiTests(TestCase):
    """Test the student delete api"""

    def setUp(self):
        self.student = sample_student()

    def test_unauthenticated_request_delete_negative(self):
        """Test an unauthenticated request cannot delete student object"""
        res = APIClient().delete(student_detail_url(self.student.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())

    def test_delete_negative(self):
        """Test the student object cannot be deleted via request"""
        client = APIClient()
        client.force_authenticate(sample_user())
        res = client.delete(student_detail_url(self.student.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())
