from core.storage_backends import PrivateMediaStorage
from datasets.models import Dataset
from django.contrib.auth import get_user_model
from django.db import models
from django_celery_results.models import TaskResult


def user_directory_path(instance, filename):
    return f"users/user_{instance.creator.id}/results/{filename}"


class AlgorithmData(models.Model):
    creator = models.ForeignKey(get_user_model(), related_name="creator", on_delete=models.PROTECT)
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)
    task = models.OneToOneField(TaskResult, blank=True, null=True, on_delete=models.PROTECT)
    result_data = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage, blank=True, null=True)
    ALGORITHMS = (
        (0, "K-means"),
        (1, "Spectral Clustering"),
        (2, "Hidden Markov model"),
        (3, "Gaussian Mixture"),
        (4, "Neural networks"),
    )
    algorithm = models.PositiveSmallIntegerField(choices=ALGORITHMS)


class KmeansParameters(models.Model):
    algorithm = models.OneToOneField(AlgorithmData, on_delete=models.CASCADE)
    n_clusters = models.PositiveSmallIntegerField(default=8)
    METHODS = (
        (0, "k-means++"),
        (1, "random"),
    )
    init = models.PositiveSmallIntegerField(choices=METHODS, default=0)
    n_init = models.PositiveSmallIntegerField(default=10)
    max_iter = models.PositiveSmallIntegerField(default=300)
