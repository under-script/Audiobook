from rest_framework import viewsets

from apps.chapter.models import Chapter
from apps.chapter.serializers import ChapterSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
