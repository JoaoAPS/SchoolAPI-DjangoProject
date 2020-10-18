import datetime

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from member.models import Student
from grade.models import Grade
from grade.serializers import GradeSerializer
from classroom.models import Classroom
from classroom.serializers import ClassroomListSerializer


class StudentListSerializer(serializers.ModelSerializer):
    """Serializer for the list view of the Student model"""
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = Student
        exclude = [
            'active',
            'monthly_payment',
            'register_date',
            'departure_date',
            'classes',
            'guardian1',
            'guardian2',
        ]
        read_only_fields = ['id']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Serializer for the detail view of the Student model"""
    grade = GradeSerializer()
    classes = ClassroomListSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id']


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for the create view of the Student model"""
    grade = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(),
        required=False
    )
    classes = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        many=True,
        required=False
    )
    birthdate = serializers.DateField(format='iso-8601', required=False)
    register_date = serializers.DateField(format='iso-8601', required=False)
    departure_date = serializers.DateField(format='iso-8601', required=False)
    active = serializers.BooleanField(default=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a student base on the data"""
        classes = validated_data.pop('classes')
        student = Student.objects.create(**validated_data)

        for classroom in classes:
            student.classes.add(classroom)

        student.save()
        return student

    def validate_birthdate(self, value):
        """Assures birth date is in the past"""
        if value >= datetime.date.today():
            raise serializers.ValidationError(_(
                "Birth date must be on the past"
            ))
        return value
