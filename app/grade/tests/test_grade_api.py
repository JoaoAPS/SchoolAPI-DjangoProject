from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APIClient
from rest_framework import status

from grade.models import Grade
from grade.serializers import GradeSerializer
from core.utils import sample_grade


GRADE_LIST_URL = reverse('grades:grade-list')


def grade_detail_url(grade_id):
    """Return the url for the grade object detail view with the specified id"""
    return reverse('grades:grade-detail', args=[grade_id])


class PublicGradeApiTests(TestCase):
    """Test the grade API for public requests"""

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_retrieve_forbidden(self):
        """Test authentication is required to retrieve grades"""
        res = self.client.get(GRADE_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_create_forbidden(self):
        """Test authentication is required to retrieve grades"""
        payload = {
            'name': 'Test',
            'rank': 2
        }

        res = self.client.post(GRADE_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateGradeApiTests(TestCase):
    """Test the grade API for authenticated requests"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='Test User',
            password='TestPass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_grade_list(self):
        """Test retrieving the grade list"""
        sample_grade(name='Test grade 1', rank=4)
        sample_grade(name='Test grade 2', rank=2)
        res = self.client.get(GRADE_LIST_URL)

        grades = Grade.objects.all().order_by('rank')
        serializer = GradeSerializer(grades, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_grade(self):
        """Test creating a grade object"""
        payload = {
            'name': 'Test Grade',
            'rank': 3
        }
        res = self.client.post(GRADE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Grade.objects.filter(**payload).exists())

    def test_retrieve_grade_detail(self):
        """Test retrieving the detail view of a grade object"""
        grade = sample_grade()
        serializer = GradeSerializer(grade)
        res = self.client.get(grade_detail_url(grade.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_full_update_grade(self):
        """Test fully updating a grade object"""
        payload = {'name': 'Other Name', 'rank': 3}
        grade = sample_grade(name='Test Grade', rank=1)
        res = self.client.put(grade_detail_url(grade.id), payload)
        grade.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(grade.name, payload['name'])
        self.assertEqual(grade.rank, payload['rank'])

    def test_partial_update_grade(self):
        """Test partially updating a grade object"""
        payload = {'name': 'Other Name'}
        grade = sample_grade(name='Test Grade', rank=1)
        res = self.client.patch(grade_detail_url(grade.id), payload)
        grade.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(grade.name, payload['name'])
