import datetime as dt

from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Student
from member.serializers import StudentCreateSerializer
from core.utils import \
    sample_student_payload, \
    sample_student, \
    sample_grade, \
    sample_classroom, \
    sample_user, \
    str_to_date


STUDENT_LIST_URL = reverse('member:student-list')


class StudentCreateApiPublicRequests(TestCase):
    """Test the student create api for public requests"""

    def test_unauthenticated_student_create_negative(self):
        """Test an unauthenticated request cannot create a student object"""
        payload = sample_student_payload()
        res = APIClient().post(STUDENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Student.objects.filter(**payload).exists())


class StudentCreateApiPositiveTests(TestCase):
    """Test the student create api for successuful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_student_basic_create_posivite(self):
        """Test successfully creating a student object"""
        payload = sample_student_payload(
            fullname="Testonildo",
            sex='M',
            birthdate='2000-01-01',
            email='testoildo@gotmail.com'
        )

        res = self.client.post(STUDENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.filter(**payload)
        self.assertTrue(student.exists())

        student = student[0]
        serializer = StudentCreateSerializer(student)
        self.assertEqual(res.data, serializer.data)

        self.assertTrue(student.active)
        self.assertEqual(student.register_date, dt.date.today())
        self.assertFalse(student.classes.exists())

    def test_student_optional_create_positive(self):
        """Test successfully creating a student object with optional params"""
        grade = sample_grade()
        classroom1 = sample_classroom()
        classroom2 = sample_classroom()
        classroom3 = sample_classroom()

        payload = sample_student_payload(
            fullname="Testonildo",
            active=False,
            departure_date='2010-10-10',
            guardian2='Mr. Guard',
            grade=grade.id,
            classes=[classroom1.id, classroom3.id]
        )
        res = self.client.post(STUDENT_LIST_URL, payload)
        payload.pop('classes')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.filter(**payload)
        self.assertTrue(student.exists)

        student = student[0]
        serializer = StudentCreateSerializer(student)
        self.assertEqual(res.data, serializer.data)

        self.assertFalse(student.active)
        self.assertEqual(
            student.departure_date,
            str_to_date(payload['departure_date'])
        )
        self.assertEqual(student.guardian2, payload['guardian2'])
        self.assertEqual(student.grade, grade)
        self.assertIn(classroom1, student.classes.all())
        self.assertIn(classroom3, student.classes.all())
        self.assertNotIn(classroom2, student.classes.all())


class StudentCreateApiNegativeTests(TestCase):
    """Test the student create api for unsuccessuful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_student_create_invalid_payload_negative(self):
        """Test requests with invalid payload cannot create student object"""
        payloads = [
            sample_student_payload(sex='L'),
            sample_student_payload(
                birthdate=dt.date.today() + dt.timedelta(days=1)
            ),
            sample_student_payload(email='not_an_email.com'),
            sample_student_payload(grade=1111),
            sample_student_payload(classes=[1241]),
            sample_student_payload(monthly_payment=10000000000),
        ]

        for payload in payloads:
            res = self.client.post(STUDENT_LIST_URL, payload)
            payload.pop('classes', None)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(Student.objects.filter(**payload).exists())

    def test_student_create_illegal_operation_negative(self):
        """Test requests with illegal operations cannot create student"""
        student = sample_student(fullname="Joseph Alleph")
        payload = sample_student_payload(
            fullname="Joseph Doppelganger",
            id_doc=student.id_doc
        )
        res = self.client.post(STUDENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Student.objects.filter(**payload).exists())


class StudentCreateApiDestructiveTests(TestCase):
    """Test the student create api for destructive requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_student_create_cannot_set_id(self):
        """Test the student id cannot be set by the create request"""
        payload = sample_student_payload(id=99999)
        res = self.client.post(STUDENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        request_id = payload.pop('id')
        student = Student.objects.filter(**payload)
        self.assertTrue(student.exists())
        student = student[0]

        self.assertNotEqual(student.id, request_id)
        self.assertNotEqual(res.data['id'], request_id)

    def test_student_create_cannot_set_firstname(self):
        """Test the student first name cannot be set by the create request"""
        payload = sample_student_payload(firstname="Namo")
        res = self.client.post(STUDENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        request_firstname = payload.pop('firstname')
        student = Student.objects.filter(**payload)
        self.assertTrue(student.exists())
        student = student[0]

        self.assertNotEqual(student.firstname, request_firstname)
        self.assertNotEqual(res.data['firstname'], request_firstname)
