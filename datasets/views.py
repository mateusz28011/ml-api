from core.utils import SwaggerOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ml.serializers import ClusteringSerializer
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datasets.models import Dataset
from datasets.permissions import IsOwner
from datasets.serializers import DatasetSerializer


class DatasetViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Dataset.objects.all()
    # parser_classes = [MultiPartParser]
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated & IsOwner]
    filter_backends = [DjangoFilterBackend, SwaggerOrderingFilter]
    ordering_fields = ["created"]
    ordering = ["-created"]

    def perform_create(self, serializer):
        if "name" not in self.request.data:
            serializer.save(owner=self.request.user, name=self.request.data["file"].name)
        else:
            serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"])
    def clusterings(self, request, *args, **kwargs):
        instance = self.get_object()
        clusterings = instance.clustering_set.all()

        page = self.paginate_queryset(clusterings)
        if page is not None:
            serializer = ClusteringSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClusteringSerializer(instance, many=True)
        return Response(serializer.data)
