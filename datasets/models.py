from core.storage_backends import PrivateMediaStorage
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


def user_directory_path(instance, filename):
    return f"users/user_{instance.owner.id}/datasets/{filename}"


class Dataset(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(default=timezone.now)
    name = models.CharField(blank=True, max_length=50)
    file = models.FileField(
        upload_to=user_directory_path, storage=PrivateMediaStorage, validators=[FileExtensionValidator(["csv"])]
    )
    # labels = models.FileField(
    #     upload_to=user_directory_path,
    #     storage=PrivateMediaStorage,
    #     blank=True,
    #     null=True,
    # )
    # labels = models.OneToOneField("datasets.Label", blank=True, null=True, on_delete=models.PROTECT)


# class Label(models.Model):
#     labels = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage, blank=True, null=True)
#     file = models.FileField(upload_to=user_directory_path, storage=PrivateMediaStorage)
