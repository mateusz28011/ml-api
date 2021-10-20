from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Algorithm, KmeansParameters
from .serializers import AlgorithmSerializer
from .tasks import kmeans


class AlgorithmViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user)
        KmeansParameters.objects.create(algorithm=instance)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        instance = self.get_object()

        if instance.algorithm == 0:
            kmeans.delay(pk)

        return Response(2)
