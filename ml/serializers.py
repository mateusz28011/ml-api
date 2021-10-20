from rest_framework import serializers

from .models import Algorithm


class AlgorithmSerializer(serializers.ModelSerializer):
    algorithm_display = serializers.CharField(source="get_algorithm_display", read_only=True)

    class Meta:
        model = Algorithm
        fields = ["id", "creator", "dataset", "task", "result_data", "algorithm", "algorithm_display"]
        read_only_fields = ["task", "result_data", "creator"]
        write_only_fields = ["algorithm"]