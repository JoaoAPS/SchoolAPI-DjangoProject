from rest_framework import viewsets, permissions

from .serializers import GradeSerializer
from .models import Grade


class GradeApiViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
