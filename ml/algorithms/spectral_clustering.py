import numpy as np
from ml.algorithms.kmeans import Kmeanspp
from scipy import linalg
from scipy.spatial.distance import cdist
from sklearn.preprocessing import normalize


class SpectralClustering:
    def __init__(self, clusters_count, rbf_value=None):
        self.clusters_count = clusters_count
        # Wartość domyślna jak w sklearn.metrics.pairwise.rbf_kernel
        self.rbf_value = rbf_value == None if 1.0 / clusters_count else rbf_value

    def _similarity_graph(self):
        # Macierz podobieństwa z wykorzystaniem jądra gaussowskiego
        adjacency_matrix = np.exp(-self.rbf_value * cdist(self.X, self.X, metric="sqeuclidean"))
        # Macierz wag
        degree_matrix = np.diag(adjacency_matrix.sum(axis=1))
        # Macierz wag ^ -1/2
        degree_matrix = linalg.fractional_matrix_power(degree_matrix, -1 / 2)
        # Znormalizowana macierz laplaca
        self.normalized_laplacian = degree_matrix.dot(adjacency_matrix).dot(degree_matrix)

    def _eigenvalue_decomposition(self):
        # Obliczanie wektorów własnych
        # W zmiennej U wektory sa przechowywanie w kolumnach
        U, _, _ = linalg.svd(self.normalized_laplacian, full_matrices=False)
        # Bierzemy tyle kolumn ile klas chcemy znaleźć
        self.U_sub = U[:, 0 : self.clusters_count]

    def fit_predict(self, X):
        self.X = X
        self.samples_count, self.features_count = self.X.shape

        self._similarity_graph()

        self._eigenvalue_decomposition()

        # Otrzymane wektory normalizujemy i znajdujemy grupy przy pomocy k-means
        self.labels = Kmeanspp(self.clusters_count).fit_predict(normalize(self.U_sub))

        return self.labels
