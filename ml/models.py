from core.storage_backends import PrivateMediaStorage
from datasets.models import Dataset
from django.contrib.auth import get_user_model
from django.db import models
from django_celery_results.models import TaskResult


def user_directory_path(instance, filename):
    return f"users/user_{instance.clustering.creator.id}/results/{filename}"


class Clustering(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)
    # dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)
    # algorithms = models.ManyToManyField("ml.AlgorithmData")


class AlgorithmData(models.Model):
    task = models.OneToOneField(TaskResult, blank=True, null=True, on_delete=models.PROTECT)
    clustering = models.ForeignKey(Clustering, on_delete=models.CASCADE)
    clusters_count = models.SmallIntegerField()
    result_data = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage, blank=True, null=True)
    ALGORITHMS = (
        (0, "K-means"),
        (1, "Spectral Clustering"),
        (2, "Gaussian Mixture"),
    )
    algorithm = models.PositiveSmallIntegerField(choices=ALGORITHMS)
