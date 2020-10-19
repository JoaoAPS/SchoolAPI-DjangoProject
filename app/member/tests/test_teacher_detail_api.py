from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.serializers import TeacherDetailSerializer
from classroom.serializers import ClassroomListSerializer
from core.utils import sample_teacher, sample_classroom, sample_user


def teacher_detail_url(teacher_id):
    return reverse('member:teacher-detail', args=[teacher_id])


class TeacherDetailApiPublicTests(TestCase):
    """Test the teacher detail api for public tests"""

    def setUp(self):
        self.client = APIClient()
        self.teacher = sample_teacher()

    def test_teacher_detail_unauthenticated_negative(self):
        """Test an unauthenticated request cannot retrieve teacher detail"""
        res = self.client.get(teacher_detail_url(self.teacher.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TeacherDetailApiPositiveTests(TestCase):
    """Test the teacher detail api for successful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.classroom1 = sample_classroom(name="Class1")
        self.classroom2 = sample_classroom(name="Class2")
        self.teacher = sample_teacher(fullname="The Teacher")
        self.teacher.classes.add(self.classroom1)
        self.teacher.classes.add(self.classroom2)

    def test_teacher_detail_positive(self):
        res = self.client.get(teacher_detail_url(self.teacher.id))
        serializer = TeacherDetailSerializer(self.teacher)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertIn('bank_agency', res.data.keys())
        self.assertIn('bank_account', res.data.keys())
        self.assertIn('monthly_payment', res.data.keys())
        self.assertIn(
            ClassroomListSerializer(self.classroom1).data,
            res.data['classes']
        )
        self.assertIn(
            ClassroomListSerializer(self.classroom2).data,
            res.data['classes']
        )


class TeacherDetailApiNegativeTests(TestCase):
    """Test the teacher detail api for unsuccessful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.classroom1 = sample_classroom(name="Class1")
        self.teacher = sample_teacher(fullname="The Teacher")
        self.teacher.classes.add(self.classroom1)

    def test_teacher_detail_unexisting_id_negative(self):
        """Test requesting detail of an unexisting teacher fails"""
        res = self.client.get(teacher_detail_url(99999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
