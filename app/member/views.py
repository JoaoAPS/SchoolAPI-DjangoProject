from rest_framework import viewsets, permissions

from member.serializers import \
    StudentListSerializer, StudentDetailSerializer, StudentCreateSerializer
from member.models import Student


class StudentViewSet(viewsets.ModelViewSet):
    """Views for managing the student class"""

    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return the appropriate serializer class"""
        if self.action == 'retrieve':
            return StudentDetailSerializer
        if self.action == 'create':
            return StudentCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        """Return the sorted queryset after applying the filters"""
        filtered = self.queryset

        show_inactive = self.request.query_params.get('show_inactive')
        show_inactive = self._get_int_from_param(show_inactive)
        if not show_inactive or not bool(show_inactive):
            filtered = filtered.filter(active=True)

        grades = self.request.query_params.get('grades')
        grades = self._get_list_from_param(grades)
        if grades:
            filtered = filtered.filter(grade__id__in=grades)

        classes = self.request.query_params.get('classes')
        classes = self._get_list_from_param(classes)
        if classes:
            filtered = filtered.filter(classes__id__in=classes)

        return filtered.order_by('fullname')

    def _get_int_from_param(self, param_str):
        """Return a integer from the parameter string"""
        if not param_str:
            return None

        try:
            i = int(param_str)
        except ValueError:
            return None
        else:
            return i

    def _get_list_from_param(self, param_str):
        """Return a list from the comma sepparated integer string"""
        if not param_str:
            return None

        try:
            param_list = list(map(int, param_str.split(',')))
        except ValueError:
            return None
        else:
            return param_list
