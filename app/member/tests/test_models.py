from django.test import TestCase

from member.models import Member
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

    def test_get_active(self):
        """Test retriving the active members only"""
        member1 = sample_member(fullname="Member 1", active=True)
        member2 = sample_member(fullname="Member 2", active=True)
        member3 = sample_member(fullname="Member 3", active=False)
        actives = Member.get_active()

        self.assertIn(member1, actives)
        self.assertIn(member2, actives)
        self.assertNotIn(member3, actives)
