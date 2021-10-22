from core.storage_backends import PrivateMediaStorage
from django.contrib.auth import get_user_model
from django.db import models


def user_directory_path(instance, filename):
    return f"users/user_{instance.owner.id}/datasets/{filename}"


class Dataset(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name="owner", on_delete=models.PROTECT)
    file = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage)
    labels = models.OneToOneField("datasets.Label", blank=True, null=True, on_delete=models.PROTECT)
    is_checked = models.BooleanField(default=False)


class Label(models.Model):
    labels = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage, blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage)
