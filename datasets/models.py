from core.storage_backends import PrivateMediaStorage
from django.contrib.auth import get_user_model
from django.db import models


def user_directory_path(instance, filename):
    return f"users/user_{instance.owner.id}/datasets/{filename}"


class Dataset(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name="owner", on_delete=models.PROTECT)
    dataset = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage)
