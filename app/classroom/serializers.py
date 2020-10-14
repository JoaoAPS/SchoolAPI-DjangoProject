from rest_framework import serializers

from classroom.models import Classroom
from grade.models import Grade
from grade.serializers import GradeSerializer


class ClassroomListSerializer(serializers.ModelSerializer):
    """Serializer for the list view of the classroom model"""

    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = Classroom
        fields = '__all__'
        read_only_fields = ['id']


class ClassroomDetailSerializer(serializers.ModelSerializer):
    """Serializer for the detail view of the classroom model"""

    grade = GradeSerializer(read_only=True)

    class Meta:
        model = Classroom
        fields = '__all__'
        read_only_fields = ['id']
