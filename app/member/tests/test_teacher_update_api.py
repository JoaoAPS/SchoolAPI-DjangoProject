import datetime as dt

from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from member.models import Teacher
from member.serializers import TeacherCreateSerializer
from core.utils import \
    sample_teacher, sample_teacher_payload, sample_classroom, sample_user


def teacher_detail_url(teacher_id):
    return reverse('member:teacher-detail', args=[teacher_id])


class TeacherUpdateApiPublicTests(TestCase):
    """Test the teacher update api for unauthenticated requests"""

    def setUp(self):
        self.client = APIClient()
        self.teacher = sample_teacher(fullname="Original Teacher")
        self.teacher_url = teacher_detail_url(self.teacher.id)

    def test_teacher_full_update_unauthenticated_negative(self):
        """Test an unauthenticated request cannot fully update teacher"""
        payload = sample_teacher_payload(fullname="Other Name")
        res = self.client.put(self.teacher_url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Teacher.objects.get(id=self.teacher.id), self.teacher)

    def test_teacher_partial_update_unauthenticated_negative(self):
        """Test an unauthenticated request cannot partially update teacher"""
        payload = {'fullname': "Other Name"}
        res = self.client.patch(self.teacher_url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Teacher.objects.get(id=self.teacher.id), self.teacher)


class TeacherUpdateApiPositiveTests(TestCase):
    """Test teacher update api for successful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.teacher = sample_teacher(
            fullname="Original Teacher",
            sex='O',
            birthdate='1990-02-27',
            email='teacha@gotmail.com',
            academic_level='Dr',
            bank_agency=21421,
            bank_account=11117,
            monthly_payment=12412
        )
        self.teacher_url = teacher_detail_url(self.teacher.id)

    def test_teacher_full_update_basic_positive(self):
        """Test successfully fully updating a teacher with basic information"""
        payload = sample_teacher_payload(
            fullname="Other Name",
            sex='F',
            birthdate='1996-01-30',
            email='othermail@gotmail.com',
            academic_level='Ms',
            bank_agency=24214,
            bank_account=124312,
            monthly_payment=1900
        )
        res = self.client.put(self.teacher_url, payload)
        self.teacher.refresh_from_db()
        serializer = TeacherCreateSerializer(self.teacher)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Teacher.objects.get(**payload), self.teacher)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_full_update_optional_positive(self):
        """Test successfully fully updating a teacher with optional params"""
        classroom1 = sample_classroom(name="Class1")
        classroom2 = sample_classroom(name="Class2")
        payload = sample_teacher_payload(
            fullname="Other name",
            active=False,
            departure_date='2010-10-01',
            classes=[classroom1.id, classroom2.id]
        )
        res = self.client.put(self.teacher_url, payload)
        payload.pop('classes')
        self.teacher.refresh_from_db()
        serializer = TeacherCreateSerializer(self.teacher)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Teacher.objects.get(**payload), self.teacher)
        self.assertIn(classroom1, self.teacher.classes.all())
        self.assertIn(classroom2, self.teacher.classes.all())
        self.assertEqual(res.data, serializer.data)

    def test_teacher_partial_update_basic_positive(self):
        """Test successfully partially updating a teacher with basic params"""
        payload = {
            'fullname': "Other Name",
            'birthdate': '1996-01-30',
            'academic_level': 'Ms',
        }
        res = self.client.patch(self.teacher_url, payload)
        self.teacher.refresh_from_db()
        serializer = TeacherCreateSerializer(self.teacher)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Teacher.objects.get(**payload), self.teacher)
        self.assertEqual(res.data, serializer.data)

    def test_teacher_partial_update_optional_positive(self):
        """Test successfully partially updating teacher with optional params"""
        classroom1 = sample_classroom(name="Class1")
        classroom2 = sample_classroom(name="Class2")
        payload = {
            'fullname': 'Other Name',
            'active': False,
            'departure_date': '2010-10-01',
            'classes': [classroom1.id, classroom2.id]
        }
        res = self.client.patch(self.teacher_url, payload)
        payload.pop('classes')
        self.teacher.refresh_from_db()
        serializer = TeacherCreateSerializer(self.teacher)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Teacher.objects.get(**payload), self.teacher)
        self.assertIn(classroom1, self.teacher.classes.all())
        self.assertIn(classroom2, self.teacher.classes.all())
        self.assertEqual(res.data, serializer.data)


class TeacherUpdateApiNegativeTests(TestCase):
    """Test the teacher update api for unsuccessful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.teacher = sample_teacher(fullname="Original Teacher")
        self.teacher_url = teacher_detail_url(self.teacher.id)

    def test_teacher_full_update_invalid_payload_negative(self):
        """Test teacher cannot be fully updated with invalid payload"""
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
            res = self.client.put(self.teacher_url, payload)
            payload.pop('classes', None)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                Teacher.objects.get(id=self.teacher.id),
                self.teacher
            )

    def test_teacher_full_update_illegal_operation_negative(self):
        """Test an illegal teacher full update operation is not performed"""
        teacher = sample_teacher(fullname="First Teacher")
        payload = sample_teacher_payload(id_doc=teacher.id_doc)
        res = self.client.put(self.teacher_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Teacher.objects.get(id=self.teacher.id), self.teacher)

    def test_teacher_partial_update_invalid_payload_negative(self):
        """Test teacher cannot be partially updated with invalid payload"""
        payloads = [
            {'sex': 'U'},
            {'birthdate': dt.date.today() + dt.timedelta(days=1)},
            {'monthly_payment': 99999999999999},
            {'academic_level': 'Aa'},
            {'bank_agency': -123},
            {'bank_account': -2144},
            {'classes': [99994]}
        ]

        for payload in payloads:
            res = self.client.patch(self.teacher_url, payload)
            payload.pop('classes', None)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                Teacher.objects.get(id=self.teacher.id),
                self.teacher
            )

    def test_teacher_partial_update_illegal_operation_negative(self):
        """Test an illegal teacher partial update operation is not performed"""
        teacher = sample_teacher(fullname="First Teacher")
        payload = {'id_doc': teacher.id_doc}
        res = self.client.patch(self.teacher_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Teacher.objects.get(id=self.teacher.id), self.teacher)


class TeacherUpdateApiDestructiveTests(TestCase):
    """Test the teacher update api for destructive requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.teacher = sample_teacher(fullname="Original Teacher")
        self.teacher_url = teacher_detail_url(self.teacher.id)

    def test_teacher_full_update_set_id_negative(self):
        """Test the teacher id cannot be set by a full update request"""
        payload = sample_teacher_payload(id=self.teacher.id + 1)
        res = self.client.put(self.teacher_url, payload)
        self.teacher.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.teacher.id, payload['id'])
        self.assertNotEqual(res.data['id'], payload['id'])

    def test_teacher_full_update_set_firstname_negative(self):
        """Test the teacher firstname cannot be set by a full update request"""
        payload = sample_teacher_payload(fullname="Peter Pan", firstname="Ott")
        res = self.client.put(self.teacher_url, payload)
        self.teacher.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.teacher.firstname, payload['firstname'])
        self.assertNotEqual(res.data['firstname'], payload['firstname'])

    def test_teacher_partial_update_set_id_negative(self):
        """Test the teacher id cannot be set by a partial update request"""
        payload = {'id': self.teacher.id + 1}
        res = self.client.patch(self.teacher_url, payload)
        self.teacher.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.teacher.id, payload['id'])
        self.assertNotEqual(res.data['id'], payload['id'])

    def test_teacher_partial_update_set_firstname_negative(self):
        """Test teacher firstname cannot be set by a partial update request"""
        payload = {'fullname': "Peter Pan", 'firstname': "Ott"}
        res = self.client.patch(self.teacher_url, payload)
        self.teacher.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.teacher.firstname, payload['firstname'])
        self.assertNotEqual(res.data['firstname'], payload['firstname'])
