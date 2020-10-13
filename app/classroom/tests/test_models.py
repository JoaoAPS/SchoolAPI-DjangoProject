from django.test import TestCase
from django.core.exceptions import ValidationError

from core.utils import sample_classroom


class ClassroomModelTests(TestCase):
    """Test the Classroom model"""

    def test_string_representation(self):
        """Test the string representation of the model"""
        classroom = sample_classroom(name="Chemistry I", identifier="Q-001")
        self.assertEqual(
            str(classroom),
            classroom.identifier + ' - ' + classroom.name
        )

    def test_days_of_week(self):
        """Test the days_of_week field is a comma separated integer list"""
        classroom = sample_classroom(days_of_week='1,2,7')
        classroom.full_clean()

        classroom = sample_classroom(days_of_week='1,2,8')
        with self.assertRaises(ValidationError):
            classroom.full_clean()
