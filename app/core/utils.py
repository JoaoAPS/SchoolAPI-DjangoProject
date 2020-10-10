import uuid

from member.models import Member
from grade.models import Grade


def sample_member(**options):
    """Create and return a sample Member object"""
    defaults = {
        'fullname': "John da Silva Doe",
        'id_doc': uuid.UUID(int=True),
        'birthdate': '2000-05-13',
        'sex': 'M',
        'monthly_payment': 100.00,
        'email': 'johnsd@gotmail.com',
        'phone_number': '+55 (41) 99999999',
        'address': 'Some Street, 10'
    }
    defaults.update(options)

    return Member.objects.create(**defaults)


def sample_grade(**options):
    """Create and return a sample Grade object"""
    defaults = {
        'name': 'First Grade',
        'rank': 1,
    }
    defaults.update(options)

    return Grade.objects.create(**defaults)
