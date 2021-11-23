from datasets.models import Dataset
from rest_framework import permissions
from rest_framework.exceptions import NotFound


class HasAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and "dataset" in request.data:
            try:
                dataset = Dataset.objects.get(pk=request.data["dataset"])
            except:
                raise NotFound({"dataset": "Not found."})
            if dataset.owner != request.user:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.dataset.owner:
            return True
        return False


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        clustering = view.get_clustering()
        if request.user != clustering.dataset.owner:
            return False
        return True
