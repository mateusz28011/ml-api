from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from datasets.models import Dataset
from datasets.permissions import IsOwner
from datasets.serializers import DatasetSerializer


class DatasetViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Dataset.objects.all()
    parser_classes = [MultiPartParser]
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated & IsOwner]

    def perform_create(self, serializer):
        if "name" not in self.request.data:
            serializer.save(owner=self.request.user, name=self.request.data["file"].name)
        else:
            serializer.save(owner=self.request.user)
