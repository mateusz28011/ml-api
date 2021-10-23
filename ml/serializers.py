from rest_framework import serializers

from .models import AlgorithmData, Clustering


class ClusteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clustering
        fields = ["id", "creator", "dataset"]
        read_only_fields = ["creator"]


class AlgorithmDataSerializer(serializers.ModelSerializer):
    algorithm_display = serializers.CharField(source="get_algorithm_display", read_only=True)

    class Meta:
        model = AlgorithmData
        fields = ["id", "task", "result_data", "algorithm", "algorithm_display", "clusters_count"]
        read_only_fields = ["task", "result_data"]
        write_only_fields = ["algorithm"]
