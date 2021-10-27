from django.contrib import admin

from .models import AlgorithmData, Clustering, Scores

admin.site.register(AlgorithmData)
admin.site.register(Clustering)
admin.site.register(Scores)
