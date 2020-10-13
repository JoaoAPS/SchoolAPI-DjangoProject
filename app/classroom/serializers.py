from rest_framework import serializers

from classroom.models import Classroom
from grade.models import Grade
from grade.serializers import GradeSerializer


class BaseClassroomSerializer(serializers.ModelSerializer):
    """Base serializer for the classroom model"""

    class Meta():
        model = Classroom
        fields = '__all__'
        read_only_fields = ['id']


class ClassroomListSerializer(BaseClassroomSerializer):
    """Serializer for the list view of the classroom model"""

    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())


class ClassroomDetailSerializer(BaseClassroomSerializer):
    """Serializer for the detail view of the classroom model"""

    grade = GradeSerializer(read_only=True)
