from rest_framework import viewsets, permissions

from .serializers import GradeSerializer
from .models import Grade


class GradeApiViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return all grades ordered by rank"""
        return self.queryset.order_by('rank')
