from rest_framework import viewsets, permissions

from classroom.models import Classroom
from classroom.serializers import \
    ClassroomListSerializer, ClassroomDetailSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    """Views for managing the classroom model"""

    queryset = Classroom.objects.all()
    serializer_class = ClassroomListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Get the appropriate serializer"""
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return self.serializer_class
