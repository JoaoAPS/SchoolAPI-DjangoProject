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


def student_detail_url(student_id):
    return reverse('member:student-detail', args=[student_id])


class StudentUpdateApiPublicRequests(TestCase):
    """Test the student update api for public requests"""

    def test_unauthenticated_student_full_update_negative(self):
        """Test an unauthenticated request cannot fully update a student"""
        student = sample_student(fullname="A Full Name")
        payload = sample_student_payload(fullname="Other name")
        res = APIClient().put(student_detail_url(student.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.get(id=student.id), student)

    def test_unauthenticated_student_partial_update_negative(self):
        """Test an unauthenticated request cannot partially update a student"""
        student = sample_student(fullname="A Full Name")
        payload = {'fullname': "Other name"}
        res = APIClient().patch(student_detail_url(student.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.get(id=student.id), student)


class StudentUpdateApiPostiveTests(TestCase):
    """Test the student full update api for successful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.student = sample_student(
            fullname="Not Deafult Name",
            sex='F',
            id_doc='7129d792',
            birthdate='1997-02-02',
            email='emailll.yes@gotmail.com',
            guardian2='Second G.'
        )

    def test_student_basic_full_update_positive(self):
        """Test successfully fully updating a student object"""
        payload = sample_student_payload(
            fullname="The correct Name",
            sex='O',
            birthdate='2000-01-01',
            email='testoildo@gotmail.com'
        )
        res = self.client.put(student_detail_url(self.student.id), payload)
        self.student.refresh_from_db()
        serializer = StudentCreateSerializer(self.student)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get(**payload), self.student)
        self.assertEqual(res.data, serializer.data)

    def test_student_optional_full_update_positive(self):
        """Test successfully fully updating a student with optional params"""
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
        res = self.client.put(student_detail_url(self.student.id), payload)
        self.student.refresh_from_db()
        payload.pop('classes')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get(**payload), self.student)
        self.assertEqual(self.student.guardian2, payload['guardian2'])
        self.assertEqual(self.student.grade, grade)
        self.assertIn(classroom1, self.student.classes.all())
        self.assertIn(classroom3, self.student.classes.all())
        self.assertNotIn(classroom2, self.student.classes.all())

        serializer = StudentCreateSerializer(self.student)
        self.assertEqual(res.data, serializer.data)

    def test_student_basic_partial_update_positive(self):
        """Test successfully partially updating a student object"""
        payload = {
            'fullname': "The correct Name",
            'sex': 'O',
            'birthdate': '2000-01-01',
        }
        res = self.client.patch(student_detail_url(self.student.id), payload)
        self.student.refresh_from_db()
        serializer = StudentCreateSerializer(self.student)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.student.fullname, payload['fullname'])
        self.assertEqual(self.student.sex, payload['sex'])
        self.assertEqual(
            self.student.birthdate,
            str_to_date(payload['birthdate'])
        )
        self.assertEqual(res.data, serializer.data)

    def test_student_optional_partial_update_positive(self):
        """Test successful partial update of a student with optional params"""
        grade = sample_grade()
        classroom1 = sample_classroom()
        classroom2 = sample_classroom()
        classroom3 = sample_classroom()

        payload = {
            'active': False,
            'departure_date': '2010-10-10',
            'guardian2': 'Mr. Guard',
            'grade': grade.id,
            'classes': [classroom1.id, classroom3.id]
        }
        res = self.client.patch(student_detail_url(self.student.id), payload)
        self.student.refresh_from_db()
        payload.pop('classes')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(self.student.active, payload['active'])
        self.assertEqual(
            self.student.departure_date,
            str_to_date(payload['departure_date'])
        )
        self.assertEqual(self.student.guardian2, payload['guardian2'])

        self.assertEqual(self.student.grade, grade)
        self.assertIn(classroom1, self.student.classes.all())
        self.assertIn(classroom3, self.student.classes.all())
        self.assertNotIn(classroom2, self.student.classes.all())

        serializer = StudentCreateSerializer(self.student)
        self.assertEqual(res.data, serializer.data)


class StudentUpdateApiNegativeTests(TestCase):
    """Test the student update api for unsuccessful requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

        self.student = sample_student(
            fullname="Not Deafult Name",
            sex='F',
            id_doc='7129d792',
            birthdate='1997-02-02',
            email='emailll.yes@gotmail.com',
            guardian2='Second G.'
        )

    def test_student_full_update_invalid_payload_negative(self):
        """Test an invalid payload cannot fully update a student object"""
        payloads = [
            sample_student_payload(sex='G'),
            sample_student_payload(
                birthdate=dt.date.today() + dt.timedelta(days=1)
            ),
            sample_student_payload(email='not_an_email.com'),
            sample_student_payload(grade=1111),
            sample_student_payload(classes=[1241]),
            sample_student_payload(monthly_payment=10000000000),
        ]

        for payload in payloads:
            res = self.client.put(student_detail_url(self.student.id), payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                Student.objects.get(id=self.student.id),
                self.student
            )

    def test_student_full_update_illegal_operation_negative(self):
        """Test requests with illegal operations cannot fully update student"""
        student = sample_student(fullname="Joseph Alleph")
        payload = sample_student_payload(
            fullname="Joseph Doppelganger",
            id_doc=student.id_doc
        )
        res = self.client.put(student_detail_url(self.student.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Student.objects.get(id=self.student.id), self.student)

    def test_student_partial_update_invalid_payload_negative(self):
        """Test an invalid payload cannot partially update a student object"""
        payloads = [
            {'sex': 'G'},
            {'birthdate': dt.date.today() + dt.timedelta(days=1)},
            {'email': 'not_an_email.com'},
            {'grade': 1111},
            {'classes': [1241]},
            {'monthly_payment': 10000000000},
        ]

        for payload in payloads:
            res = self.client.patch(
                student_detail_url(self.student.id),
                payload
            )

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                Student.objects.get(id=self.student.id),
                self.student
            )

    def test_student_partial_update_illegal_operation_negative(self):
        """Test illegal operations cannot partially update student object"""
        student = sample_student(fullname="Joseph Alleph")
        payload = {'id_doc': student.id_doc}
        res = self.client.patch(student_detail_url(self.student.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Student.objects.get(id=self.student.id), self.student)
