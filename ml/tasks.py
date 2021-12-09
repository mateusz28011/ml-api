from io import BytesIO

import pandas as pd
from celery import shared_task
from django.core.files.base import ContentFile
from sklearn import metrics
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

from .models import AlgorithmData, Scores


class AlgorithmWorkflow:
    def __init__(self, algorithm_instance, algorithm_data_instance):
        self.algorithm_instance = algorithm_instance
        self.algorithm_data_instance = algorithm_data_instance
        name = self.algorithm_data_instance.get_algorithm_display().replace(" ", "_")
        self.name = f"{name}_{self.algorithm_data_instance.id}"

    def load_dataset_into_data_frame(self):
        self.data = pd.read_csv(self.algorithm_data_instance.clustering.dataset.file)

    def save_data_into_file_field(self, data, field, filename):
        output = BytesIO()
        pd.DataFrame(data).to_csv(output, index=False, header=False, index_label=False)
        field.save(f"{filename}.csv", ContentFile(output.getvalue()))

    def calculate_metrics(self):
        ss = metrics.silhouette_score(self.data, self.labels, metric="euclidean")
        chs = metrics.calinski_harabasz_score(self.data, self.labels)
        dbs = metrics.davies_bouldin_score(self.data, self.labels)

        if self.algorithm_data_instance.has_scores():
            instance = self.algorithm_data_instance.scores
            instance.silhouette_score = ss
            instance.calinski_harabasz_score = chs
            instance.davies_bouldin_score = dbs
            instance.save()
        else:
            Scores.objects.create(
                algorithm_data=self.algorithm_data_instance,
                silhouette_score=ss,
                calinski_harabasz_score=chs,
                davies_bouldin_score=dbs,
            )

    def prepare_points_for_plots(self):
        self.save_data_into_file_field(
            PCA(2).fit_transform(self.data), self.algorithm_data_instance.plot_2d_points, f"{self.name}_points_2d"
        )
        self.save_data_into_file_field(
            PCA(3).fit_transform(self.data), self.algorithm_data_instance.plot_3d_points, f"{self.name}_points_3d"
        )

    def start(self):
        self.load_dataset_into_data_frame()
        self.labels = self.algorithm_instance.fit_predict(self.data)
        self.save_data_into_file_field(self.labels, self.algorithm_data_instance.result_data, self.name)
        self.calculate_metrics()
        self.prepare_points_for_plots()


def get_instance_and_save_task_id(algorithm_pk, task_id):
    instance = AlgorithmData.objects.get(pk=algorithm_pk)
    instance.task_id = task_id
    instance.save()
    return instance


def get_instance(algorithm_pk):
    return AlgorithmData.objects.get(pk=algorithm_pk)


@shared_task(bind=True)
def kmeans(self, algorithm_pk):
    instance = get_instance_and_save_task_id(algorithm_pk, self.request.id)

    AlgorithmWorkflow(
        KMeans(
            n_clusters=instance.clusters_count,
        ),
        instance,
    ).start()

    return instance.id


@shared_task(bind=True)
def gaussian_mixture(self, algorithm_pk):
    instance = get_instance_and_save_task_id(algorithm_pk, self.request.id)

    AlgorithmWorkflow(
        GaussianMixture(
            n_components=instance.clusters_count,
        ),
        instance,
    ).start()

    return instance.id


@shared_task(bind=True)
def spectral_clustering(self, algorithm_pk):
    instance = get_instance_and_save_task_id(algorithm_pk, self.request.id)

    AlgorithmWorkflow(
        SpectralClustering(
            n_clusters=instance.clusters_count,
        ),
        instance,
    ).start()

    return instance.id
