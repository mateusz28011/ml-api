import random

import numpy as np
from scipy.spatial.distance import cdist


class Kmeanspp:
    def __init__(self, clusters_count):
        self.clusters_count = clusters_count

    def _kmeanspp(self):
        i = random.randint(0, self.samples_count)
        centroid_temp = np.array([self.X[i]])
        for k in range(1, self.clusters_count):
            D = np.array([])
            for x in self.X:
                D = np.append(D, np.min(np.sum((x - centroid_temp) ** 2)))
            prob = D / np.sum(D)
            cummulative_prob = np.cumsum(prob)
            r = random.random()
            i = 0
            for j, p in enumerate(cummulative_prob):
                if r < p:
                    i = j
                    break
            centroid_temp = np.append(centroid_temp, [self.X[i]], axis=0)
        self.centroids = centroid_temp

    def _calculate_distances(self):
        self.distances = cdist(self.X, self.centroids, "euclidean")

    def _calculate_clusters(self):
        self.labels = np.array([np.argmin(i) for i in self.distances])

    def fit_predict(self, X, iterations_count=100):
        self.X = X
        self.samples_count, self.features_count = self.X.shape

        # Inicjalizacja centroidów
        self._kmeanspp()

        # Obliczanie odległości euklidesowej pomiędzy wszystkimi próbkami i centroidami
        self._calculate_distances()

        # Przydzielanie próbki do najbliższego centroidu
        self._calculate_clusters()

        for _ in range(iterations_count):
            print(_)
            # Aktualizacja centroidów, przez branie średniej próbek w każdym skupieniu
            self.centroids = np.vstack(
                [self.X[self.labels == index].mean(axis=0) for index in range(self.clusters_count)]
            )
            self._calculate_distances()
            self._calculate_clusters()

        return self.labels
