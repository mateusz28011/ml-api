from celery import current_app
from celery.signals import after_task_publish
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import AlgorithmData


@receiver(pre_delete, sender=AlgorithmData)
def image_pre_delete(sender, instance, *args, **kwargs):
    if instance.result_data:
        instance.result_data.delete()


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    # the task may not exist if sent using `send_task` which
    # sends tasks by name, so fall back to the default result backend
    # if that is the case.
    task = current_app.tasks.get(sender)
    backend = task.backend if task else current_app.backend

    backend.store_result(headers["id"], None, "SENT")
