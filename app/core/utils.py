import uuid

from member.models import Member


def sample_member(**options):
    """Return a sample Member object"""
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
