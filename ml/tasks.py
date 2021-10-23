from io import BytesIO

import pandas as pd
from celery import shared_task
from django.core.files.base import ContentFile
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

from .models import AlgorithmData


class AlgorithmWorkflow:
    def __init__(self, algorithm_instance, algorithm_data_instance):
        self.algorithm_instance = algorithm_instance
        self.algorithm_data_instance = algorithm_data_instance

    def load_dataset_into_data_frame(self):
        self.data = pd.read_csv(self.algorithm_data_instance.clustering.dataset.file)

    def save_data_into_result_in_csv(self):
        output = BytesIO()
        pd.DataFrame(self.labels).to_csv(output, index=False)
        name = self.algorithm_data_instance.get_algorithm_display().replace(" ", "_")
        result_data = self.algorithm_data_instance.result_data
        result_data.save(f"{name}_{self.algorithm_data_instance.id}.csv", ContentFile(output.getvalue()))

    def start(self):
        self.load_dataset_into_data_frame()
        self.labels = self.algorithm_instance.fit_predict(self.data)
        self.save_data_into_result_in_csv()


@shared_task
def kmeans(algorithm_pk):
    instance = AlgorithmData.objects.get(pk=algorithm_pk)

    # pca = PCA(2)
    # df = pca.fit_transform(df)

    awf = AlgorithmWorkflow(
        KMeans(
            n_clusters=instance.clusters_count,
        ),
        instance,
    )

    awf.start()

    return instance.id


@shared_task
def gaussian_mixture(algorithm_pk):
    instance = AlgorithmData.objects.get(pk=algorithm_pk)

    awf = AlgorithmWorkflow(
        GaussianMixture(
            n_components=10,
        ),
        instance,
    )

    awf.start()

    return instance.id


@shared_task
def spectral_clustering(algorithm_pk):
    instance = AlgorithmData.objects.get(pk=algorithm_pk)

    awf = AlgorithmWorkflow(
        SpectralClustering(
            n_clusters=10,
        ),
        instance,
    )

    awf.start()

    return instance.id
