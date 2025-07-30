"""
LMGEC clustering model implementation.

This module provides the LMGEC class, which implements the Localized
Multi-Graph Embedding Clustering (LMGEC) algorithm. It extends
scikit-learn's BaseEstimator and ClusterMixin interfaces, offering
fit, predict, and transform methods for clustering across multiple views.
"""

import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin

from ..utils.init_utils import init_G_F, init_W  # type: ignore
from ..models.lmgec_core import train_loop  # type: ignore


class LMGEC(BaseEstimator, ClusterMixin):
    """
    Localized Multi-Graph Embedding Clustering (LMGEC) model.

    :param int n_clusters: Number of clusters to form.
    :param int embedding_dim: Dimension of embedding space.
    :param float temperature: Temperature for view weighting.
    :param int max_iter: Max training iterations.
    :param float tolerance: Convergence threshold.
    """

    def __init__(
        self,
        n_clusters: int = 3,
        embedding_dim: int = 10,
        temperature: float = 0.5,
        max_iter: int = 30,
        tolerance: float = 1e-6,
    ):
        self.n_clusters = n_clusters
        self.embedding_dim = embedding_dim
        self.temperature = temperature
        self.max_iter = max_iter
        self.tolerance = tolerance

    def fit(self, X_views, y=None):
        """
        Fit the LMGEC model to multiple data views.

        :param list X_views: List of 2D arrays (one per view), shape
            (n_samples, n_features) for each.
        :param y: Ignored, for API compatibility.
        :returns: The fitted estimator.
        :rtype: self
        """
        if not X_views or len(X_views) == 0:
            raise ValueError("X_views must be a non-empty list of 2D numpy arrays.")  # noqa: E501

        for i, X in enumerate(X_views):
            if X is None or not isinstance(X, np.ndarray) or X.size == 0:
                raise ValueError(f"View {i} is empty or invalid.")
            print(
                f"View {i} shape: {X.shape}, sum: {np.sum(X)}, "
                f"any NaN: {np.isnan(X).any()}"
            )

        n_views = len(X_views)  # noqa: F841
        Ws = []
        inertias = []

        # Step 1: Initialize projection matrices and compute inertia
        for v, Xv in enumerate(X_views):
            Wv = init_W(Xv, self.embedding_dim)
            Ws.append(Wv)
            XWv = Xv @ Wv
            print(f"View {v}: XWv norm = {np.linalg.norm(XWv)}")
            Gv, Fv = init_G_F(XWv, self.n_clusters)
            try:
                reconstruction = Fv[Gv]
            except IndexError:
                raise ValueError(f"Invalid clustering result in view {v}.")
            inertia = np.linalg.norm(XWv - reconstruction)
            inertias.append(inertia)
        # Step 2: Compute alphas (softmax of -inertia)
        inertias = np.array(inertias)
        if inertias.size == 0:
            raise ValueError("No valid inertias were computed. Check input data.")  # noqa: E501

        scaled = -inertias / (self.temperature + 1e-8)
        max_scaled = np.max(scaled)
        exp_scaled = np.exp(scaled - max_scaled)
        sum_exp = np.sum(exp_scaled)
        if sum_exp == 0:
            raise ValueError("Sum of softmax weights is zero. Check your data.")  # noqa: E501
        alphas = exp_scaled / sum_exp

        print("DEBUG: Inertias =", inertias)
        print("DEBUG: Alphas (normalized weights) =", alphas)
        print("DEBUG: Sum of alphas =", np.sum(alphas))

        # Step 3: Compute consensus embedding
        XW_consensus = sum(
            alpha * (X @ W) for alpha, X, W in zip(alphas, X_views, Ws)
        )

        # Step 4: Initialize clustering on consensus embedding
        G, F = init_G_F(XW_consensus, self.n_clusters)

        # Step 5: Run training loop to refine G, F, W
        G, F, XW_final, losses = train_loop(
            X_views,
            F,        # cluster centroids
            G,        # assignments
            alphas,   # view weights
            self.n_clusters,
            self.max_iter,
            self.tolerance,
        )

        self.labels_ = G.numpy() if hasattr(G, "numpy") else G
        self.F_ = F
        self.XW_ = XW_final
        self.loss_history_ = losses

        return self

    def predict(self, X_views):
        """
        Predict cluster labels for input views after fitting.

        :param list X_views: List of feature matrices (ignored).
        :returns: Cluster labels from fit.
        :rtype: array-like
        """
        return self.labels_

    def transform(self, X_views):
        """
        Transform input views into the final embedding space.

        :param list X_views: List of feature matrices (ignored).
        :returns: Consensus embedding from fit.
        :rtype: array-like
        """
        return self.XW_
