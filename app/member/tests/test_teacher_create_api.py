import datetime as dt

from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Teacher
from member.serializers import TeacherCreateSerializer
from core.utils import \
    sample_teacher_payload, \
    sample_teacher, \
    sample_classroom, \
    sample_user, \
    str_to_date


TEACHER_LIST_URL = reverse('member:teacher-list')


class TestTeacherCreateApiPublicTests(TestCase):
    """Test the teacher create api for unauthenticated requests"""

    def test_teacher_create_unathenticated_forbidden(self):
        """Test an unathenticated request cannot create a teacher object"""
        payload = sample_teacher_payload()
        res = APIClient().post(TEACHER_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestTeacherCreateApiPositiveTests(TestCase):
    """Test the teacher create api for successful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_teacher_create_api_basic_positive(self):
        """Test successfully creating a basic teacher object"""
        payload = sample_teacher_payload(
            fullname="Teacher Tester",
            sex='F',
            birthdate='1990-02-27',
            email='teacha@gotmail.com',
            academic_level='Dr',
            bank_agency=21421,
            bank_account=11117,
            monthly_payment=12412
        )
        res = self.client.post(TEACHER_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        teacher = Teacher.objects.filter(**payload)
        self.assertTrue(teacher.exists())

        teacher = teacher[0]
        serializer = TeacherCreateSerializer(teacher)
        self.assertEqual(res.data, serializer.data)

        self.assertTrue(teacher.active)
        self.assertFalse(teacher.classes.exists())
        self.assertEqual(teacher.register_date, dt.date.today())

    def test_teacher_create_api_optional_positive(self):
        """Test successfully creating a teacher object with optional params"""
        classroom1 = sample_classroom(name='Class1')
        classroom2 = sample_classroom(name='Class2')
        payload = sample_teacher_payload(
            fullname="Tester Teacher",
            active=False,
            departure_date='2010-10-01',
            classes=[classroom1.id, classroom2.id]
        )
        res = self.client.post(TEACHER_LIST_URL, payload)
        payload.pop('classes')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        teacher = Teacher.objects.filter(**payload)
        self.assertTrue(teacher.exists())

        teacher = teacher[0]
        serializer = TeacherCreateSerializer(teacher)
        self.assertEqual(res.data, serializer.data)

        self.assertFalse(teacher.active)
        self.assertEqual(
            teacher.departure_date,
            str_to_date(payload['departure_date'])
        )
        self.assertIn(classroom1, teacher.classes.all())
        self.assertIn(classroom2, teacher.classes.all())


class TeacherCreateApiNegativeTests(TestCase):
    """Test the teacher create api for unsuccessful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_teacher_create_invalid_payload_negative(self):
        """Test an invalid payload request does not create a teacher object"""
        payloads = [
            sample_teacher_payload(sex='U'),
            sample_teacher_payload(
                birthdate=dt.date.today() + dt.timedelta(days=1)
            ),
            sample_teacher_payload(monthly_payment=99999999999999),
            sample_teacher_payload(academic_level='Aa'),
            sample_teacher_payload(bank_agency=-123),
            sample_teacher_payload(bank_account=-2144),
            sample_teacher_payload(classes=[99994])
        ]

        for payload in payloads:
            res = self.client.post(TEACHER_LIST_URL, payload)
            payload.pop('classes', None)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(Teacher.objects.filter(**payload).exists())

    def test_teacher_create_illegal_operation_negative(self):
        """Test an illegal create teacher operation is not performed"""
        teacher = sample_teacher(fullname="First Teacher")
        payload = sample_teacher_payload(
            fullname="Doppelganger",
            id_doc=teacher.id_doc
        )
        res = self.client.post(TEACHER_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Teacher.objects.filter(**payload).exists())


class TeacherCreateApiDestructiveTests(TestCase):
    """Test the teacher create api for destructive requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_teacher_create_set_id_negative(self):
        """Test the teacher id cannot be set by the create request"""
        payload = sample_teacher_payload(id=99999)
        res = self.client.post(TEACHER_LIST_URL, payload)
        request_id = payload.pop('id')
        teacher = Teacher.objects.get(**payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(teacher.id, request_id)
        self.assertNotEqual(res.data['id'], request_id)

    def test_teacher_create_set_firstname_negative(self):
        """Test the teacher firstname cannot be set by the create request"""
        payload = sample_teacher_payload(fullname="Peter Pan", firstname="Ott")
        res = self.client.post(TEACHER_LIST_URL, payload)
        request_firstname = payload.pop('firstname')
        teacher = Teacher.objects.get(**payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(teacher.firstname, request_firstname)
        self.assertNotEqual(res.data['firstname'], request_firstname)
