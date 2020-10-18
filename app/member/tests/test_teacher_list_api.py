from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Teacher
from member.serializers import TeacherListSerializer
from core.utils import sample_teacher, sample_classroom, sample_user


TEACHER_LIST_URL = reverse('member:teacher-list')


class TeacherListPublicTests(TestCase):
    """Test the teacher list api for public requests"""

    def test_teacher_list_unauthenticated_negatice(self):
        """Test an unauthenticated request cannot retrieve teachers list"""
        res = APIClient().get(TEACHER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TeacherListPositiveTests(TestCase):
    """Test the teacher list api for successful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.classroom1 = sample_classroom()
        self.classroom2 = sample_classroom()
        self.classroom3 = sample_classroom()

        self.teacher1 = sample_teacher(
            fullname="Teacher 1",
            academic_level='Gr'
        )
        self.teacher2 = sample_teacher(
            fullname="Teacher 2",
            academic_level='Ms'
        )
        self.teacher3 = sample_teacher(
            fullname="Teacher 3",
            academic_level='Dr'
        )
        self.teacher4 = sample_teacher(
            fullname="Teacher 4",
            academic_level='Dr',
        )
        self.teacher5 = sample_teacher(
            fullname="Teacher 5",
            academic_level='Ms',
            active=False
        )

        self.teacher1.classes.add(self.classroom1)
        self.teacher2.classes.add(self.classroom2)
        self.teacher3.classes.add(self.classroom3)
        self.teacher5.classes.add(self.classroom1)

    def test_teacher_list_unfiltered_positive(self):
        """Test successfully retrieving teacher list with no filtering"""
        res = self.client.get(TEACHER_LIST_URL)
        serializer = TeacherListSerializer(
            Teacher.get_active().order_by('fullname'),
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_list_show_inactive_posivite(self):
        """Test successfully retrieving teacher list including inactives"""
        res = self.client.get(TEACHER_LIST_URL, {'show_inactive': '1'})
        serializer = TeacherListSerializer(
            Teacher.objects.all().order_by('fullname'),
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_list_filter_academic_level_positive(self):
        """Test successfully listing teachers filtered by academic level"""
        res = self.client.get(
            TEACHER_LIST_URL,
            {'academic_level': 'Gr,Dr'}
        )
        serializer = TeacherListSerializer(
            [self.teacher1, self.teacher3, self.teacher4],
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_list_filter_classes_positive(self):
        """Test successfully listing teachers filtered by classes"""
        res = self.client.get(
            TEACHER_LIST_URL,
            {'classes': f'{self.classroom1.id},{self.classroom3.id}'}
        )
        serializer = TeacherListSerializer(
            [self.teacher1, self.teacher3],
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_list_multiple_filters_positive(self):
        """Test successfully listing teacher with multiple filters"""
        res = self.client.get(TEACHER_LIST_URL, {
            'show_inactive': '1',
            'academic_level': 'Ms',
            'classes': f'{self.classroom1.id}'
        })
        serializer = TeacherListSerializer([self.teacher5], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class TeacherListApiNegativeTests(TestCase):
    """Test the teacher list api for unsuccessful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        sample_teacher()
        sample_teacher()
        sample_teacher(active=False)

        self.serializer = TeacherListSerializer(
            Teacher.get_active(),
            many=True
        )

    def test_teacher_list_invalid_show_inactive_negative(self):
        """Test passing an invalid show_inactive get parameter does nothing"""
        res = self.client.get(TEACHER_LIST_URL, {'show_inactive': 'abc'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_teacher_list_invalid_classes_negative(self):
        """Test passing an invalid show_inactive get parameter does nothing"""
        res = self.client.get(TEACHER_LIST_URL, {'classes': '1,4.2'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

        res = self.client.get(TEACHER_LIST_URL, {'classes': 'abc'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)
