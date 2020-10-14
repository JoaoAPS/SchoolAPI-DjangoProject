from rest_framework import serializers

from member.models import Student
from grade.models import Grade


class StudentListSerializer(serializers.ModelSerializer):
    """Serializer for the Student model"""
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta():
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
