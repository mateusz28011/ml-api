from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AlgorithmData, KmeansParameters
from .serializers import AlgorithmDataSerializer
from .tasks import gaussian_mixture, kmeans, spectral_clustering


class AlgorithmViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlgorithmData.objects.all()
    serializer_class = AlgorithmDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)
        if instance.algorithm == 0:
            KmeansParameters.objects.create(algorithm=instance)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        instance = self.get_object()

        if instance.algorithm == 0:
            kmeans.delay(pk)
        elif instance.algorithm == 1:
            spectral_clustering.delay(pk)
        elif instance.algorithm == 3:
            gaussian_mixture.delay(pk)

        return Response(2)
