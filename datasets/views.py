from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated

from datasets.models import Dataset
from datasets.serializers import DatasetSerializer


class DatasetViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
