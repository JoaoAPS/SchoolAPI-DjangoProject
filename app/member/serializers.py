from rest_framework import serializers

from member.models import Student
from grade.models import Grade
from grade.serializers import GradeSerializer
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
