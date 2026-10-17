from rest_framework import viewsets

from .models import Direction, Faculty, Group
from .serializers import DirectionSerializer, FacultySerializer, GroupSerializer


class FacultyViewsSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DirectionViewsSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer

    def get_queryset(self):
        queryset = Direction.objects.select_related('faculty')
        faculty = self.request.query_params.get('faculty', '')
        if faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))
        return queryset


class GroupViewsSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.select_related('direction__faculty')
        direction = self.request.query_params.get('direction', '')
        if direction.isdigit():
            queryset = queryset.filter(direction__id=int(direction))
        return queryset
