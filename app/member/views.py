from rest_framework import viewsets, mixins, permissions

from member.models import Student, Teacher
from member.serializers import \
    StudentListSerializer, \
    StudentDetailSerializer, \
    StudentCreateSerializer, \
    TeacherListSerializer, \
    TeacherDetailSerializer


class StudentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    """Views for managing the student class"""

    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return the appropriate serializer class"""
        if self.action == 'retrieve':
            return StudentDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return StudentCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        """Return the sorted queryset after applying the filters"""
        filtered = self.queryset

        show_inactive = self.request.query_params.get('show_inactive')
        show_inactive = _get_int_from_param(show_inactive)
        if not show_inactive or not bool(show_inactive):
            filtered = filtered.filter(active=True)

        grades = self.request.query_params.get('grades')
        grades = _get_list_from_param(grades)
        if grades:
            filtered = filtered.filter(grade__id__in=grades)

        classes = self.request.query_params.get('classes')
        classes = _get_list_from_param(classes)
        if classes:
            filtered = filtered.filter(classes__id__in=classes)

        return filtered.order_by('fullname')


class TeacherViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """Views for managing the Teacher model"""

    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return the appropriate serializer class"""
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        """Return the filtered and sorted queryset"""
        queryset = self.queryset

        show_inactive = self.request.query_params.get('show_inactive')
        show_inactive = _get_int_from_param(show_inactive)
        if not show_inactive:
            queryset = queryset.filter(active=True)

        academic_level = self.request.query_params.get('academic_level')
        academic_level = academic_level.split(',') if academic_level else None
        if academic_level:
            queryset = queryset.filter(academic_level__in=academic_level)

        classes = self.request.query_params.get('classes')
        classes = _get_list_from_param(classes)
        if classes:
            queryset = queryset.filter(classes__id__in=classes)

        return queryset.order_by('fullname')


def _get_int_from_param(param_str):
    """Return a integer from the parameter string"""
    if not param_str:
        return None

    try:
        i = int(param_str)
    except ValueError:
        return None
    else:
        return i


def _get_list_from_param(param_str):
    """Return a list from the comma sepparated integer string"""
    if not param_str:
        return None

    try:
        param_list = list(map(int, param_str.split(',')))
    except ValueError:
        return None
    else:
        return param_list
