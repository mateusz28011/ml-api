from celery.result import AsyncResult
from django.conf import settings
from django_celery_results.models import TaskResult
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ml.permissions import HasAccess, IsCreator

from .models import AlgorithmData, Clustering
from .serializers import AlgorithmDataSerializer, ClusteringSerializer
from .tasks import gaussian_mixture, kmeans, spectral_clustering


class ClusteringViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Clustering.objects.all()
    serializer_class = ClusteringSerializer
    permission_classes = [IsAuthenticated & HasAccess]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class AlgorithmDataViewset(
    mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = AlgorithmData.objects.all()
    serializer_class = AlgorithmDataSerializer
    permission_classes = [IsAuthenticated & IsCreator]

    def get_clustering(self):
        try:
            clustering = Clustering.objects.get(pk=self.kwargs["clustering_pk"])
        except:
            raise NotFound({"clustering": "Not found."})
        return clustering

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

        if instance.task_id != None:
            try:
                task_instance = TaskResult.objects.get(task_id=instance.task_id)
            except:
                raise PermissionDenied("Cannot start. Task has been sent already.")

            if task_instance.status != "FAILURE":
                raise PermissionDenied("Cannot start. Task is finished successfully.")

        if instance.algorithm == 0:
            task_id = kmeans.delay(pk)
        elif instance.algorithm == 1:
            task_id = spectral_clustering.delay(pk)
        elif instance.algorithm == 2:
            task_id = gaussian_mixture.delay(pk)

        if task_id:
            instance.task_id = task_id
            instance.save()

        return Response("Started")
