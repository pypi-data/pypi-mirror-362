"""
Dataset loader utilities for LMGEC experiments.

This module provides functions to load and preprocess multiple benchmark
datasets stored in MATLAB .mat files. Each function returns adjacency
matrices (As), feature matrices (Xs), and ground-truth labels.

Supported datasets include:
- acm, dblp, imdb, photos, wiki
- mfeat, aloi, arabidopsis (multi-view graph structure)
- Custom dispatch via `datagen(dataset)`
"""

import os
import numpy as np
from scipy import io
from sklearn.neighbors import kneighbors_graph
from typing import List, Tuple


def _load_mat_file(filename: str) -> dict:
    """
    Load a MATLAB .mat file from the appropriate directory.
    """
    base_dirs = [
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "datasets", "data_lmgec")),  # noqa: E501
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "prepared_datasets")),  # noqa: E501
    ]
    for base_dir in base_dirs:
        data_path = os.path.join(base_dir, filename)
        if os.path.exists(data_path):
            print(f"Loading data file: {data_path}")
            return io.loadmat(data_path)

    raise FileNotFoundError(f"File not found in {base_dirs}: {filename}")


def _extract_multi_view_data(data: dict) -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:  # noqa: E501
    """
    Generic handler for multi-view datasets like arabidopsis, aloi, mfeat.
    """
    Xs, As = [], []
    labels = None

    for key in sorted(data.keys()):
        if key.startswith("X_"):
            Xs.append(np.asarray(data[key]))
        elif key.startswith("A_"):
            A = data[key]
            As.append(A)  # garder la matrice sparse (COO, CSR, etc.)

        elif key in {"label", "labels", "gnd"}:
            labels = data[key].reshape(-1)

    if labels is None:
        raise ValueError("No labels found in the dataset.")

    return As, Xs, labels


def acm() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("ACM.mat")
    X = data["features"]
    A = data["PAP"]
    B = data["PLP"]
    Xs = [X.toarray()]
    As = [A.toarray(), B.toarray()]
    labels = data["label"].reshape(-1)
    return As, Xs, labels


def dblp() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("DBLP.mat")
    X = data["features"]
    As = [data["net_APTPA"], data["net_APCPA"], data["net_APA"]]
    Xs = [X.toarray()]
    As = [A.toarray() for A in As]
    labels = data["label"].reshape(-1)
    return As, Xs, labels


def imdb() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("IMDB.mat")
    X = data["features"]
    As = [data["MAM"], data["MDM"]]
    Xs = [X.toarray()]
    As = [A.toarray() for A in As]
    labels = data["label"].reshape(-1)
    return As, Xs, labels


def photos() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("Amazon_Photos.mat")
    X = data["features"]
    A = data["adj"]
    labels = data["label"].reshape(-1)

    X = X.toarray() if hasattr(X, "toarray") else np.asarray(X)
    A = A.toarray() if hasattr(A, "toarray") else np.asarray(A)

    try:
        X2 = X @ X.T
    except Exception as e:
        print(f"Warning: failed to compute X @ X.T: {e}")
        X2 = X

    Xs = [X, X2]
    As = [A]
    return As, Xs, labels


def wiki() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("wiki.mat")
    X = data["fea"]
    A = data.get("W")

    X = X.toarray() if hasattr(X, "toarray") else np.asarray(X)
    X = X.astype(float)

    if A is None:
        raise ValueError("Adjacency matrix 'W' not found in wiki.mat")

    A = A.toarray() if hasattr(A, "toarray") else A
    knn = kneighbors_graph(X, n_neighbors=5, metric="cosine")
    knn = knn.toarray() if hasattr(knn, "toarray") else knn

    Xs = [X, np.log2(1 + X)]
    As = [A, knn]
    labels = data["gnd"].reshape(-1)
    return As, Xs, labels


def mfeat() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("mfeat.mat")
    return _extract_multi_view_data(data)


def aloi() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("aloi.mat")
    return _extract_multi_view_data(data)


def arabidopsis() -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:
    data = _load_mat_file("arabidopsis.mat")
    return _extract_multi_view_data(data)


def datagen(dataset: str) -> Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]:  # noqa: E501
    loaders = {
        "acm": acm,
        "dblp": dblp,
        "imdb": imdb,
        "photos": photos,
        "wiki": wiki,
        "mfeat": mfeat,
        "aloi": aloi,
        "arabidopsis": arabidopsis,
    }
    if dataset.lower() not in loaders:
        raise ValueError(f"Unknown dataset: {dataset}")
    return loaders[dataset.lower()]()
