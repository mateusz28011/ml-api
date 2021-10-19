from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from datasets.models import Dataset
from datasets.serializers import DatasetSerializer


class DatasetViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
