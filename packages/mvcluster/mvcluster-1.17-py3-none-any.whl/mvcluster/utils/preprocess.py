"""
Dataset preprocessing utilities for LMGEC experiments.

This module provides functions to normalize adjacency matrices and feature
matrices, with optional TF-IDF transformation. Adjacency normalization adds
self-loops scaled by a beta parameter and row-normalizes the result.

Functions:
- preprocess_dataset: normalize adjacency and features.
"""

import numpy as np
import scipy.sparse as sp
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import StandardScaler


def preprocess_dataset(
    adj: sp.spmatrix,
    features: np.ndarray,
    tf_idf: bool = False,
    beta: float = 1.0,
    max_features: int = 5000
) -> tuple[sp.spmatrix, np.ndarray]:
    """
    Normalize adjacency matrix and feature matrix.

    Parameters
    ----------
    adj : sp.spmatrix
        Sparse adjacency matrix.
    features : np.ndarray
        Feature matrix (dense or sparse).
    tf_idf : bool, optional
        Whether to apply TF-IDF transformation, by default False.
    beta : float, optional
        Scaling factor for self-loops, by default 1.0.
    max_features : int, optional
        Maximum number of feature columns to retain, by default 1000.

    Returns
    -------
    tuple[sp.spmatrix, np.ndarray]
        Tuple containing the normalized adjacency and processed features.
    """
    print(f"[DEBUG] Feature matrix shape before preprocessing: {features.shape}")  # noqa :E501

    # Add self-loops scaled by beta
    adj = adj + beta * sp.eye(adj.shape[0], format="csr")

    # Compute row sums and inverse for normalization
    rowsum = np.array(adj.sum(1)).flatten()
    r_inv = np.power(rowsum, -1, where=rowsum != 0)
    r_inv[np.isinf(r_inv)] = 0.0
    r_mat_inv = sp.diags(r_inv)

    # Row-normalize adjacency
    adj_normalized = r_mat_inv.dot(adj)

    # Truncate feature matrix if it's too wide
    if features.shape[1] > max_features:
        print(
            f"[INFO] Reducing feature dimensionality from {features.shape[1]} "
            f"to {max_features}"
        )
        features = features[:, :max_features]

    # Process features: TF-IDF or L2 normalization
    if tf_idf:
        transformer = TfidfTransformer(norm="l2")
        features_processed = transformer.fit_transform(features)
    else:
        features_processed = normalize(features, norm="l2")

    return adj_normalized, features_processed


def prepare_embeddings_from_views(
    As: list[sp.spmatrix],
    Xs: list[np.ndarray],
    tf_idf: bool = False,
    beta: float = 1.0,
) -> list[np.ndarray]:
    """
    Preprocess all (A, X) pairs and compute final embeddings (H = A @ X).

    Parameters
    ----------
    As : list of sp.spmatrix
        Adjacency matrices for each view.
    Xs : list of np.ndarray
        Feature matrices for each view.
    tf_idf : bool
        Whether to apply TF-IDF transformation to features.
    beta : float
        Scaling for self-loops in adjacency normalization.

    Returns
    -------
    list of np.ndarray
        List of processed H embeddings (one per view).
    """
    Hs = []

    for idx, (A, X) in enumerate(zip(As, Xs)):
        A_norm, X_proc = preprocess_dataset(A, X, tf_idf=tf_idf, beta=beta)

        # Compute H = A @ X
        H = A_norm.dot(X_proc) if sp.issparse(A_norm) else A_norm @ X_proc

        # Normalize / center H
        if H.shape[0] * H.shape[1] < 1e6:
            H = H.toarray() if sp.issparse(H) else H
            H_scaled = StandardScaler(with_std=False).fit_transform(H)
        else:
            if sp.issparse(H):
                H_scaled = H - H.mean(axis=0)
            else:
                H_scaled = H - np.mean(H, axis=0, keepdims=True)

        Hs.append(H_scaled)

        print(f"✅ Processed view {idx + 1}: H shape {H_scaled.shape}")

    return Hs
