from core.storage_backends import PrivateMediaStorageOverwrite
from datasets.models import Dataset
from django.contrib.auth import get_user_model
from django.db import models
from django_celery_results.models import TaskResult


def user_directory_path(instance, filename):
    return f"users/user_{instance.clustering.creator.id}/results/{filename}"


class Clustering(models.Model):
    name = models.CharField(max_length=50)
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)


class AlgorithmData(models.Model):
    task_id = models.CharField(max_length=50, blank=True, null=True, default=None)
    clustering = models.ForeignKey(Clustering, on_delete=models.CASCADE)
    clusters_count = models.PositiveIntegerField()
    result_data = models.FileField(
        upload_to=user_directory_path, storage=PrivateMediaStorageOverwrite, blank=True, null=True
    )
    ALGORITHMS = (
        (0, "K-means"),
        (1, "Spectral Clustering"),
        (2, "Gaussian Mixture"),
    )
    algorithm = models.PositiveSmallIntegerField(choices=ALGORITHMS)

    def has_scores(self):
        return hasattr(self, "scores")


class Scores(models.Model):
    algorithm_data = models.OneToOneField(AlgorithmData, on_delete=models.CASCADE)
    silhouette_score = models.FloatField()
    calinski_harabasz_score = models.FloatField()
    davies_bouldin_score = models.FloatField()
