import numpy as np
from scipy.stats import multivariate_normal


class GaussianMixture:
    def __init__(self, clusters_count, max_iter=100):
        self.clusters_count = clusters_count
        self.max_iter = int(max_iter)

    def initialize(self):
        self.shape = self.X.shape
        self.n, self.m = self.shape

        # Inicjalizacja tablicy jednowymiarowej pi oraz tablicy dwuwymiarowej wag
        self.pi = np.full(shape=self.clusters_count, fill_value=1 / self.clusters_count)
        self.weights = np.full(shape=self.shape, fill_value=1 / self.clusters_count)

        # Inicjalizacja tablic dwuwymiarowych średnich oraz kowariancji
        random_row = np.random.randint(low=0, high=self.n, size=self.clusters_count)
        self.mu = [self.X[row_index, :] for row_index in random_row]
        self.sigma = [np.cov(self.X.T) for _ in range(self.clusters_count)]

    def predict_proba(self):
        likelihood = np.zeros((self.n, self.clusters_count))
        # Obliczanie dla każdej grupy wielowymiarowego rozkładu normalnego
        # a nastepnie prawdopodobienstwo przynaleznosci do grupy za pomoca
        # funckji gęstości prawdopodobieństwa
        for i in range(self.clusters_count):
            distribution = multivariate_normal(mean=self.mu[i], cov=self.sigma[i])
            likelihood[:, i] = distribution.pdf(self.X)

        # Normalizacja sumy wag do jedynki
        numerator = likelihood * self.pi
        denominator = numerator.sum(axis=1)[:, np.newaxis]
        weights = numerator / denominator
        return weights

    def _e_step(self):
        # Obliczanie prawdopodobiensta przynależności do grupy
        self.weights = self.predict_proba()
        # Aktualizacja pi
        self.cluster_weights_sum = self.weights.sum(axis=0)
        self.pi = self.cluster_weights_sum / self.n

    def _m_step(self):
        # Aktualizacja średniej oraz kowariancji dla każdej grupy
        for i in range(self.clusters_count):
            # weight = self.weights[:, [i]]
            # total_weight = weight.sum()
            self.mu[i] = (self.X * self.weights[:, [i]]).sum(axis=0) / self.cluster_weights_sum[i]
            self.sigma[i] = np.cov(
                self.X.T, aweights=(self.weights[:, [i]] / self.cluster_weights_sum[i]).flatten(), bias=True
            )

    def fit_predict(self, X):
        self.X = X
        self.initialize()

        # Korzystamy z algorytmu expectation-maximization, ponieważ
        # nie ma określonych grup dla zestawu danych
        for _ in range(self.max_iter):
            self._e_step()
            self._m_step()

        weights = self.predict_proba()
        return np.argmax(weights, axis=1)
