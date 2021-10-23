from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AlgorithmData, Clustering
from .serializers import AlgorithmDataSerializer, ClusteringSerializer
from .tasks import gaussian_mixture, kmeans, spectral_clustering


class ClusteringViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Clustering.objects.all()
    serializer_class = ClusteringSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class AlgorithmDataViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlgorithmData.objects.all()
    serializer_class = AlgorithmDataSerializer
    permission_classes = [IsAuthenticated]

    def get_clustering(self):
        return Clustering.objects.get(id=self.kwargs["clustering_pk"])

    def perform_create(self, serializer):
        serializer.save(clustering=self.get_clustering())

    def get_queryset(self):
        if self.action == "list":
            queryset = AlgorithmData.objects.filter(clustering=self.kwargs["clustering_pk"])
        else:
            queryset = self.queryset

        return queryset

    @action(detail=True, methods=["post"])
    def start(self, request, pk, *args, **kwargs):
        instance = self.get_object()

        if instance.algorithm == 0:
            kmeans.delay(pk)
        elif instance.algorithm == 1:
            spectral_clustering.delay(pk)
        elif instance.algorithm == 2:
            gaussian_mixture.delay(pk)

        return Response(2)
