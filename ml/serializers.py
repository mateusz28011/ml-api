from rest_framework import serializers

from .models import Algorithm


class AlgorithmSerializer(serializers.ModelSerializer):
    algorithm_display = serializers.CharField(source="get_algorithm_display", read_only=True)

    class Meta:
        model = Algorithm
        fields = ["id", "creator", "dataset", "task_result", "algorithm", "algorithm_display"]
        read_only_fields = ["task_result", "creator"]
        write_only_fields = ["algorithm"]
