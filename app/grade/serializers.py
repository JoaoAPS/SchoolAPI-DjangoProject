from rest_framework import serializers

from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for the Grade model"""

    class Meta():
        model = Grade
        fields = ['id', 'name', 'rank']
        read_only_fields = ['id']
