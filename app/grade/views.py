from rest_framework import viewsets, permissions

from .serializers import GradeSerializer
from .models import Grade


class GradeApiViewSet(viewsets.ModelViewSet):
    """Views for managing the grade model"""

    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return queryset ordered by rank"""
        return self.queryset.order_by('rank')
