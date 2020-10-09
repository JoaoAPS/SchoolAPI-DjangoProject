from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from django.db.utils import OperationalError


class AuxCursorClass:
    """A class whose objects can call a cursor method successully"""

    def cursor(self):
        return True


class CommandTests(TestCase):
    """Test new manage.py commands"""

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, sleep):
        """Test the app waits for db before statings"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [AuxCursorClass()]
            call_command('wait_for_db')
            self.assertTrue(gi.call_count, 6)
