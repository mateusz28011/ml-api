from io import BytesIO

import pandas as pd
from celery import shared_task
from django.core.files.base import ContentFile
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .models import Algorithm


@shared_task
def kmeans(algorithm_pk):
    instance = Algorithm.objects.get(pk=algorithm_pk)

    df = pd.read_csv(instance.dataset.dataset.file)

    # pca = PCA(2)
    # df = pca.fit_transform(df)

    parameters = instance.kmeansparameters
    init_method = parameters.get_init_display()
    alg = KMeans(
        n_clusters=parameters.n_clusters,
        init=init_method,
        n_init=parameters.n_init,
        max_iter=parameters.max_iter,
    )
    label = alg.fit_predict(df)

    output = BytesIO()
    pd.DataFrame(label).to_csv(output, index=False)
    instance.result_data.save(f"kmeans_{instance.id}.csv", ContentFile(output.getvalue()))

    return instance.id
