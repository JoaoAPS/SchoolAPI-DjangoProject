from django.test import TestCase

from core.utils import sample_member


class MemberTests(TestCase):
    """Test the Member model"""

    def test_member_string_representation(self):
        """Test the string representations of the model"""
        member = sample_member()
        self.assertEqual(str(member), member.fullname)

    def test_firstname(self):
        """Test the first name is successfully retrieved from the full name"""
        member = sample_member(fullname="Paul Levie")
        self.assertEqual(member.firstname, "Paul")
