from django.test import TestCase
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from classroom.models import Classroom
from classroom.serializers import \
    ClassroomListSerializer, ClassroomDetailSerializer
from core.utils import \
    sample_classroom_payload, \
    sample_grade, \
    sample_classroom, \
    sample_user


CLASSROOM_LIST_URL = reverse('classroom:classroom-list')


def classroom_detail_url(classroom_id):
    return reverse('classroom:classroom-detail', args=[classroom_id])


class PublicClassroomApiTests(TestCase):
    """Test the classroom api for public requests"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_retrieve_forbidden(self):
        """Test the classrooms can't be retrived without authentication"""
        res = self.client.get(CLASSROOM_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_create_forbidden(self):
        """Test a classroom cannot be created without authentication"""
        grade = sample_grade()
        payload = sample_classroom_payload(grade=grade)
        res = self.client.post(CLASSROOM_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateClassroomApiTests(TestCase):
    """Test the classroom api with authenticated requests"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(sample_user())

    def test_retrive_classroom_list(self):
        """Test retriving the classroom list"""
        sample_classroom(name='CR 1', identifier='BC01')
        sample_classroom(name='CR 2', identifier='AB01', grade=sample_grade())
        classrooms = Classroom.objects.all().order_by('identifier')
        serializer = ClassroomListSerializer(classrooms, many=True)
        res = self.client.get(CLASSROOM_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_classroom_detail(self):
        """Test retriving the detail view of a classroom"""
        classroom = sample_classroom(name='Test', grade=sample_grade())
        serializer = ClassroomDetailSerializer(classroom)
        res = self.client.get(classroom_detail_url(classroom.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_classroom_successful(self):
        """Test creating a classroom object"""
        payload = sample_classroom_payload(
            name='Testing',
            grade=sample_grade().id,
            days_of_week='2,4'
        )
        res = self.client.post(CLASSROOM_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Classroom.objects.filter(**payload).exists())

    def test_create_classroom_unsuccessful(self):
        """Test providing invalid days_of_week doesn't create classroom"""
        payloads = [
            sample_classroom_payload(
                name='Test Class',
                days_of_week='1,2,9'
            ),
            sample_classroom_payload(
                name='Test Class',
                days_of_week='24'
            ),
            sample_classroom_payload(
                name='Test Class',
                days_of_week='2.4'
            ),
        ]

        for payload in payloads:
            res = self.client.post(CLASSROOM_LIST_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(Classroom.objects.filter(**payload).exists())

    def test_full_update(self):
        """Test fully updating the a classroom object"""
        classroom = sample_classroom(name="Test CR", room='A45')
        payload = sample_classroom_payload(
            name="Other name",
            days_of_week='1',
            grade=sample_grade().id
        )
        res = self.client.put(classroom_detail_url(classroom.id), payload)
        classroom.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Classroom.objects.get(**payload), classroom)

    def test_partial_update(self):
        """Test partially updating the a classroom object"""
        classroom = sample_classroom(name="Test CR", room='A45')
        payload = {'name': 'Other name', 'room': 'Other room'}
        res = self.client.patch(classroom_detail_url(classroom.id), payload)
        classroom.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(classroom.name, payload['name'])
        self.assertEqual(classroom.room, payload['room'])
