from django_celery_results.models import TaskResult
from rest_framework import serializers

from .models import AlgorithmData, Clustering


class ClusteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clustering
        fields = ["id", "creator", "dataset"]
        read_only_fields = ["creator"]


class AlgorithmDataSerializer(serializers.ModelSerializer):
    algorithm_display = serializers.CharField(source="get_algorithm_display", read_only=True)
    task_status = serializers.SerializerMethodField()

    class Meta:
        model = AlgorithmData
        fields = ["id", "task_status", "result_data", "algorithm", "algorithm_display", "clusters_count"]
        read_only_fields = ["result_data", "task_status"]
        write_only_fields = ["algorithm"]

    def get_task_status(self, obj):
        if obj.task_id:
            try:
                instance = TaskResult.objects.get(task_id=obj.task_id)
                return instance.status
            except:
                return "PENDING"
        else:
            return None
