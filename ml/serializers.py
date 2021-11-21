from django_celery_results.models import TaskResult
from rest_framework import serializers

from .models import AlgorithmData, Clustering, Scores


class ClusteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clustering
        fields = ["id", "name", "dataset"]
        # read_only_fields = ["creator"]


class AlgorithmDataListSerializer(serializers.ModelSerializer):
    algorithm_display = serializers.CharField(source="get_algorithm_display", read_only=True)
    task_status = serializers.SerializerMethodField()

    class Meta:
        model = AlgorithmData
        fields = ["id", "task_status", "algorithm_display", "clusters_count"]

    def get_task_status(self, obj):
        if obj.task_id:
            try:
                instance = TaskResult.objects.get(task_id=obj.task_id)
                return instance.status
            except:
                return "PENDING"
        else:
            return None


class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = ["silhouette_score", "calinski_harabasz_score", "davies_bouldin_score"]


class AlgorithmDataSerializer(AlgorithmDataListSerializer):
    scores = ScoresSerializer(read_only=True)

    class Meta(AlgorithmDataListSerializer.Meta):
        fields = ["id", "task_status", "result_data", "algorithm", "algorithm_display", "clusters_count", "scores"]
        read_only_fields = ["result_data", "task_status", "scores"]
        write_only_fields = ["algorithm"]
