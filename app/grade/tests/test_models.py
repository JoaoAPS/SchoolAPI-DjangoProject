from django.test import TestCase

from core.utils import sample_grade


class GradeModelTests(TestCase):
    """Test the Grade model"""

    def test_string_representation(self):
        """Test the string representation of the Grade model"""
        grade = sample_grade(name='Some grade')
        self.assertEqual(str(grade), grade.name)
