from celery import shared_task
from django.db import models

from .models import Algorithm


@shared_task
def kmeans(algorithm_pk):
    instance = Algorithm.objects.get(pk=algorithm_pk)
    return instance.id
