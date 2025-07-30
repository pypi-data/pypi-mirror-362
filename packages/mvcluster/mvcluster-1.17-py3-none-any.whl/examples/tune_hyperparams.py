import argparse
import itertools
import os
from typing import List, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.metrics import adjusted_rand_score as ari
from scipy.io import loadmat

from mvcluster.cluster.lmgec import LMGEC
from mvcluster.utils.metrics import clustering_accuracy, clustering_f1_score
from mvcluster.utils.preprocess import preprocess_dataset


def load_custom_mat(path: str) -> Tuple[List[Tuple[np.ndarray, np.ndarray]], Optional[np.ndarray]]:  # noqa: E501
    """
    Load various possible .mat file formats with views and labels.
    Returns:
        views: list of (A, X) tuples
        labels: ndarray or None
    """
    from scipy.sparse import issparse

    mat = loadmat(path)
    Xs, As = [], []
    labels = None
    if "labels" in mat:
        labels = mat["labels"].squeeze()
    elif "label" in mat:
        labels = mat["label"].squeeze()
    if labels is not None and labels.ndim != 1:
        labels = labels.ravel()
    if labels is not None and not isinstance(labels, np.ndarray):
        labels = np.array(labels)

    i = 0
    while f"X_{i}" in mat and f"A_{i}" in mat:
        Xs.append(mat[f"X_{i}"])
        As.append(mat[f"A_{i}"].astype(np.float32))
        i += 1
    if Xs:
        return list(zip(As, Xs)), labels

    i = 1
    while f"X{i}" in mat:
        X = mat[f"X{i}"]
        A = np.eye(X.shape[0], dtype=np.float32)
        Xs.append(X)
        As.append(A)
        i += 1
    if Xs:
        return list(zip(As, Xs)), labels

    for key in ("features", "views"):
        if key in mat:
            value = mat[key]

            if issparse(value):
                # Cas : une seule matrice sparse (1 vue)
                A = np.eye(value.shape[0], dtype=np.float32)
                return [(A, value)], labels

            if isinstance(value, np.ndarray) and value.ndim == 2:
                # Cas : une seule matrice dense (1 vue)
                A = np.eye(value.shape[0], dtype=np.float32)
                return [(A, value)], labels

            try:
                # Cas : plusieurs vues stockées dans un array de shape (1, n)
                raw_views = value[0]
                for view in raw_views:
                    if issparse(view):
                        view = view.tocsr()
                    A = np.eye(view.shape[0], dtype=np.float32)
                    Xs.append(view)
                    As.append(A)
                return list(zip(As, Xs)), labels
            except Exception as e:
                raise ValueError(f"Unsupported format under key '{key}': {e}")


    if "fea" in mat and "W" in mat:  # noqa :303
        X = mat["fea"]
        A = mat["W"].astype(np.float32)
        Xs.append(X)
        As.append(A)
        if "gnd" in mat:
            labels = mat["gnd"].squeeze()
            if labels.ndim != 1:
                labels = labels.ravel()
            if not isinstance(labels, np.ndarray):
                labels = np.array(labels)
        return list(zip(As, Xs)), labels

    raise ValueError("Unsupported .mat file structure. Expected known keys.")

def run_once(views, labels, dim, temp, beta, max_iter, tol):  # noqa : 302
    """
    Run a single LMGEC clustering evaluation with detailed
    output and flake8 compliance.

    Args:
        views (List[Tuple[np.ndarray, np.ndarray]]): List of (A, X) views.
        labels (np.ndarray): Ground truth cluster labels.
        dim (int): Embedding dimension.
        temp (float): Temperature parameter.
        beta (float): Graph regularization coefficient.
        max_iter (int): Maximum number of iterations.
        tol (float): Tolerance for convergence.

    Returns:
        dict: Dictionary of evaluation metrics.
    """
    if labels is None:
        raise ValueError("Ground truth labels are required.")

    views_proc = []
    print("\n[ÉTAPE] Prétraitement des vues")
    for idx, (A, X) in enumerate(views):
        A_norm, X_proc = preprocess_dataset(A, X, beta=beta)
        if hasattr(X_proc, "toarray"):
            X_proc = X_proc.toarray()
        print(
            f"  → Vue {idx + 1}: A ({A.shape}), X ({X.shape}) → "
            f"A_norm ({A_norm.shape}), X_proc ({X_proc.shape})"
        )
        views_proc.append((A_norm, X_proc))

    print("\n[ÉTAPE] Calcul des embeddings (H = S @ X)")
    Hs = []
    for idx, (S, X) in enumerate(views_proc):
        H = S @ X
        if isinstance(H, np.matrix):
            print(f"  [AVERTISSEMENT] Vue {idx + 1} est un np.matrix → conversion en ndarray")  # noqa: E501
            H = np.asarray(H)
        H_scaled = StandardScaler(with_std=False).fit_transform(H)
        print(
            f"  → H_{idx + 1} = S @ X : {H.shape}, "
            f"après normalisation : {H_scaled.shape}"
        )
        Hs.append(H_scaled)

    print("\n[ÉTAPE] Entraînement du modèle LMGEC")
    model = LMGEC(
        n_clusters=len(np.unique(labels)),
        embedding_dim=dim,
        temperature=temp,
        max_iter=max_iter,
        tolerance=tol,
    )
    model.fit(Hs)
    pred = model.labels_
    print(f"  → Clustering terminé en {len(model.loss_history_)} itérations")

    metrics = {
        "acc": clustering_accuracy(labels, pred),
        "nmi": nmi(labels, pred),
        "ari": ari(labels, pred),
        "f1": clustering_f1_score(labels, pred, average="macro"),
    }
    print(
        f"[SCORE] ACC: {metrics['acc']:.4f}, "
        f"NMI: {metrics['nmi']:.4f}, "
        f"ARI: {metrics['ari']:.4f}, "
        f"F1: {metrics['f1']:.4f}"
    )

    return metrics


def main(args):
    views, labels = load_custom_mat(args.data_file)
    if labels is None:
        raise ValueError("Labels not found in dataset.")
    if args.n_clusters != len(np.unique(labels)):
        print(
            f"[WARN] --n_clusters ({args.n_clusters}) ≠ nb unique labels ({len(np.unique(labels))})"  # noqa: E501
        )

    temperatures = [0.1, 0.5, 1.0, 2.0, 10.0, 20.0]
    betas = [1.0, 2.0]
    embedding_dims = [3, 4, 5]

    results = []
    for temp, beta, dim in itertools.product(temperatures, betas, embedding_dims):  # noqa: E501
        print("\n" + "=" * 60)
        print(f"[TEST] Température={temp}, β={beta}, dim={dim}")
        metrics = run_once(
            views,
            labels,
            dim=dim,
            temp=temp,
            beta=beta,
            max_iter=args.max_iter,
            tol=args.tolerance,
        )
        metrics.update(temperature=temp, beta=beta, embedding_dim=dim)
        results.append(metrics)

    df = pd.DataFrame(results)
    df.to_csv("hyperparam_results.csv", index=False)

    print("\n[TOP CONFIGS PAR NMI]")
    print(df.sort_values("nmi", ascending=False).head())

    os.makedirs("plots", exist_ok=True)
    for metric in ("nmi", "ari", "acc", "f1"):
        plt.figure(figsize=(8, 5))
        sns.lineplot(
            data=df,
            x="temperature",
            y=metric,
            hue="embedding_dim",
            style="beta",
            markers=True,
        )
        plt.title(f"{metric.upper()} vs Température")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"plots/{metric}_vs_temperature.png")
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", type=str, required=True)
    parser.add_argument("--n_clusters", type=int, required=True)
    parser.add_argument("--max_iter", type=int, default=50)
    parser.add_argument("--tolerance", type=float, default=1e-7)
    args = parser.parse_args()
    main(args)
