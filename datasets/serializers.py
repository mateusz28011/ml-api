from rest_framework import serializers

from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "file", "name", "created"]
        read_only_fields = ["created"]
