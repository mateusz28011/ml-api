# Generated by Django 3.2.8 on 2021-11-21 14:50

import core.storage_backends
import datasets.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_dataset_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='file',
            field=models.FileField(storage=core.storage_backends.PrivateMediaStorage, upload_to=datasets.models.user_directory_path, validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
    ]
