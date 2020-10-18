import datetime

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from member.models import Student, Teacher
from grade.models import Grade
from grade.serializers import GradeSerializer
from classroom.models import Classroom
from classroom.serializers import ClassroomListSerializer


class StudentListSerializer(serializers.ModelSerializer):
    """Serializer for the list view of the Student model"""
    firstname = serializers.ReadOnlyField()
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = Student
        exclude = [
            'monthly_payment',
            'register_date',
            'departure_date',
            'classes',
            'guardian1',
            'guardian2',
        ]
        read_only_fields = ['id', 'firstname']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Serializer for the detail view of the Student model"""
    firstname = serializers.ReadOnlyField()
    grade = GradeSerializer()
    classes = ClassroomListSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'firstname']


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for the create view of the Student model"""
    firstname = serializers.ReadOnlyField()
    birthdate = serializers.DateField(format='iso-8601', required=False)
    register_date = serializers.DateField(format='iso-8601', required=False)
    departure_date = serializers.DateField(format='iso-8601', required=False)
    active = serializers.BooleanField(default=True)
    grade = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(),
        required=False
    )
    classes = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'firstname']

    def validate_birthdate(self, value):
        """Assures birth date is in the past"""
        if value >= datetime.date.today():
            raise serializers.ValidationError(_(
                "Birth date must be on the past"
            ))
        return value


class TeacherListSerializer(serializers.ModelSerializer):
    """Serializer for list view of the Teacher model"""
    firstname = serializers.ReadOnlyField()

    class Meta():
        model = Teacher
        exclude = [
            'monthly_payment',
            'register_date',
            'departure_date',
            'classes',
            'bank_agency',
            'bank_account',
        ]
        read_only_fields = ['id', 'firstname']
