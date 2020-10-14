import uuid
import datetime

from member.models import Member, Student, Teacher
from grade.models import Grade
from classroom.models import Classroom


def sample_member_payload(**options):
    """Return a dict with the required fields of a member object"""
    payload = {
        'fullname': "John da Silva Doe",
        'id_doc': str(uuid.uuid4()),
        'birthdate': '2000-05-13',
        'sex': 'M',
        'monthly_payment': 100.00,
        'email': 'johnsd@gotmail.com',
        'phone_number': '+55 (41) 99999999',
        'address': 'Some Street, 10'
    }
    payload.update(options)

    return payload


def sample_student_payload(**options):
    payload = sample_member_payload()
    payload.update({
        'guardian1': 'My legal guardian',
        'guardian2': 'Another guardian'
    })
    payload.update(options)

    return payload


def sample_teacher_payload(**options):
    payload = sample_member_payload()
    payload.update({
        'academic_level': 'Ms',
        'bank_agency': 461287,
        'bank_account': 1241412
    })
    payload.update(options)

    return payload


def sample_classroom_payload(includeGrade: bool = False, **options):
    """Return a dict with the required fields of a classroom object"""
    payload = {
        'name': 'Advanced Physics',
        'identifier': str(uuid.uuid4()),
        'room': 'A10',
        'time': datetime.time(hour=9, minute=30),
        'days_of_week': '1,3,5',
    }
    includeGrade and payload.update({'grade': sample_grade()})
    payload.update(options)

    return payload


def sample_member(**options):
    """Create and return a sample Member object"""
    fields = sample_member_payload()
    fields.update(options)

    return Member.objects.create(**fields)


def sample_student(**options):
    """Create and return a sample Student object"""
    fields = sample_student_payload()
    fields.update(options)

    return Student.objects.create(**fields)


def sample_teacher(**options):
    """Create and return a sample Teacher object"""
    fields = sample_teacher_payload()
    fields.update(options)

    return Teacher.objects.create(**fields)


def sample_grade(**options):
    """Create and return a sample Grade object"""
    defaults = {
        'name': 'First Grade',
        'rank': 1,
    }
    defaults.update(options)

    return Grade.objects.create(**defaults)


def sample_classroom(**options):
    """Create and return a sample Classroom object"""
    fields = sample_classroom_payload(True, **options)
    return Classroom.objects.create(**fields)
