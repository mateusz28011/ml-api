# Generated by Django 3.2.8 on 2021-11-19 12:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_auto_20211118_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
