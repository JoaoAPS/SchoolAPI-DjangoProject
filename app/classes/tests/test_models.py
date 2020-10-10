from django.test import TestCase
from django.core.exceptions import ValidationError

from core.utils import sample_class


class ClassModelTests(TestCase):
    """Test the Class model"""

    def test_string_representation(self):
        """Test the string representation of the model"""
        clss = sample_class(name="Basic Chemistry I", identifier="Q-001")
        self.assertEqual(str(clss), clss.identifier + ' - ' + clss.name)

    def test_days_of_week(self):
        """Test the days_of_week field is a comma separated integer list"""
        clss = sample_class(days_of_week='1,2,7')
        clss.full_clean()

        clss = sample_class(days_of_week='1,2,8')
        with self.assertRaises(ValidationError):
            clss.full_clean()
