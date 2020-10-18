from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Student
from member.serializers import StudentListSerializer
from core.utils import \
    sample_student, sample_grade, sample_classroom, sample_user


STUDENT_LIST_URL = reverse('member:student-list')


class StudentListApiPositiveTests(TestCase):
    """Test the student list api for successfull requests"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.grade1 = sample_grade()
        self.grade2 = sample_grade()
        self.grade3 = sample_grade()
        self.classroom1 = sample_classroom()
        self.classroom2 = sample_classroom()
        self.classroom3 = sample_classroom()

        self.student1 = sample_student(
            fullname='John Default',
            grade=self.grade1,
        )
        self.student2 = sample_student(
            fullname='Jane Jeans',
            grade=self.grade2
        )
        self.student3 = sample_student(
            fullname='Dave Derik',
            active=False,
            grade=self.grade2
        )
        self.student4 = sample_student(
            fullname='Johna Default',
            grade=self.grade1
        )
        self.student5 = sample_student(
            fullname='Leon Daqui',
            grade=self.grade3
        )

        self.student1.classes.add(self.classroom2)
        self.student2.classes.add(self.classroom1)
        self.student3.classes.add(self.classroom2)
        self.student4.classes.add(self.classroom3)

        self.student1_serializer = StudentListSerializer(self.student1)
        self.student2_serializer = StudentListSerializer(self.student2)
        self.student3_serializer = StudentListSerializer(self.student3)
        self.student4_serializer = StudentListSerializer(self.student4)
        self.student5_serializer = StudentListSerializer(self.student5)

    def test_basic_student_list_positive(self):
        """Test successfully retrieving the students list"""
        students = Student.get_active().order_by('fullname')
        serializer = StudentListSerializer(students, many=True)
        res = self.client.get(STUDENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_student_list_show_inactive(self):
        """Test successfully retriving the studants list including inactives"""
        students = Student.objects.all().order_by('fullname')
        serializer = StudentListSerializer(students, many=True)
        res = self.client.get(STUDENT_LIST_URL, {'show_inactive': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_student_excluded_information_is_not_shown(self):
        """Test the excluded model fields are not shown in list"""
        res = self.client.get(STUDENT_LIST_URL)
        excluded_fields = [
            'active',
            'monthly_payment',
            'register_date',
            'departure_date',
            'classes',
            'guardian1',
            'guardian2',
        ]

        for field in excluded_fields:
            self.assertNotIn(field, res.data[0].keys())

    def test_student_list_filter_grade_positive(self):
        """Test successfully retrieving the students list filtered by grade"""
        res = self.client.get(
            STUDENT_LIST_URL,
            {'grades': f'{self.grade1.id},{self.grade3.id}'}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.student1_serializer.data, res.data)
        self.assertIn(self.student4_serializer.data, res.data)
        self.assertIn(self.student5_serializer.data, res.data)
        self.assertNotIn(self.student2_serializer.data, res.data)
        self.assertNotIn(self.student3_serializer.data, res.data)

    def test_student_list_filter_classroom_positive(self):
        """Test successfully retrieving students list filtered by classes"""
        res = self.client.get(
            STUDENT_LIST_URL,
            {'classes': f'{self.classroom1.id},{self.classroom2.id}'}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.student1_serializer.data, res.data)
        self.assertIn(self.student2_serializer.data, res.data)
        self.assertNotIn(self.student3_serializer.data, res.data)
        self.assertNotIn(self.student4_serializer.data, res.data)
        self.assertNotIn(self.student5_serializer.data, res.data)

    def test_student_list_multiple_filters_positive(self):
        """Test successfully retrieving students list with multiple filters"""
        res = self.client.get(
            STUDENT_LIST_URL,
            {
                'grades': f'{self.grade2.id}',
                'classes': f'{self.classroom1.id},{self.classroom2.id}',
                'show_inactive': 1
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.student3_serializer.data, res.data)
        self.assertIn(self.student2_serializer.data, res.data)
        self.assertNotIn(self.student1_serializer.data, res.data)
        self.assertNotIn(self.student4_serializer.data, res.data)
        self.assertNotIn(self.student5_serializer.data, res.data)

    def test_student_list_filter_no_object(self):
        """Test returning an empty query to filters that have no match"""
        res = self.client.get(
            STUDENT_LIST_URL,
            {
                'grades': f'{self.grade3.id}',
                'classes': f'{self.classroom1.id}',
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_student_list_filter_nonexisting_value(self):
        """Test returning an empty query to filters that have no match"""
        res = self.client.get(STUDENT_LIST_URL, {'grades': '1000'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)


class StudentListApiNegativeTests(TestCase):
    """Test the student list api for unsuccessfull requests"""

    def test_unauthenticated_retrieve_list_forbidden(self):
        """Test an unauthenticated request cannot retrieve student list"""
        client = APIClient()
        res = client.get(STUDENT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class StudentListApiDestructiveTests(TestCase):
    """Test the student list api for intentionally bad requests"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        sample_student()
        sample_student()
        sample_student(active=False)

    def test_invalid_show_inactive_is_ignored(self):
        """Test setting the show_inactive parameter to a word is ignored"""
        students = Student.get_active().order_by('fullname')
        serializer = StudentListSerializer(students, many=True)
        res = self.client.get(STUDENT_LIST_URL, {'show_inactive': 'gasfh'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_invalid_grades_filter_is_ignored(self):
        """Test passing an invalid grades filter is ignored"""
        students = Student.get_active().order_by('fullname')
        serializer = StudentListSerializer(students, many=True)

        res = self.client.get(STUDENT_LIST_URL, {'grades': '1,4.2'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        res = self.client.get(STUDENT_LIST_URL, {'grades': 'abc'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_invalid_classes_filter_is_ignored(self):
        """Test passing an invalid classes filter is ignored"""
        students = Student.get_active().order_by('fullname')
        serializer = StudentListSerializer(students, many=True)

        res = self.client.get(STUDENT_LIST_URL, {'classes': '1,4.2'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        res = self.client.get(STUDENT_LIST_URL, {'classes': 'abc'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
