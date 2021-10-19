from io import BytesIO

import pandas as pd
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .models import Algorithm
from .serializers import AlgorithmSerializer
from .tasks import kmeans


class AlgorithmViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        instance = self.get_object()
        print(dir(instance.dataset.dataset))
        df = pd.read_csv(instance.dataset.dataset.file)

        pca = PCA(2)

        df = pca.fit_transform(df)

        alg = KMeans(n_clusters=10)

        label = alg.fit_predict(df)

        output = BytesIO()
        pd.DataFrame(label).to_csv(output, index=False)
        instance.result_data.save(f"django_test.csv", ContentFile(output.getvalue()))

        # print(df)
        # kmeans.delay(pk)

        return Response(2)
