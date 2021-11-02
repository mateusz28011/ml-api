from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.db import transaction
from rest_framework import serializers

from .models import User


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get("first_name")
        user.last_name = self.data.get("last_name")
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "join_date", "is_staff",]
        read_only_fields = ["email", "join_date", "is_staff"]


class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

