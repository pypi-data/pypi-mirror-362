import argparse
from time import time
from itertools import product

import numpy as np
from scipy.sparse import issparse
from sklearn.metrics import adjusted_rand_score as ari
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
from sklearn.preprocessing import StandardScaler

from ..cluster.lmgec import LMGEC
from ..utils.datagen import datagen
from ..utils.metrics import clustering_accuracy, clustering_f1_score
from ..utils.preprocess import preprocess_dataset


def run_lmgec_experiment(
    dataset: str,
    temperature: float = 1.0,
    beta: float = 1.0,
    max_iter: int = 10,
    tolerance: float = 1e-7,
    runs: int = 1,
) -> dict:
    """
    Run the LMGEC clustering experiment for a given dataset.
    """
    print("=" * 80)
    print(f"[INFO] Running LMGEC experiment on dataset: '{dataset}'")
    print("=" * 80)

    As, Xs, labels = datagen(dataset)
    k = len(np.unique(labels))
    print(f"[INFO] Number of detected clusters (k): {k}")
    views = list(product(As, Xs))

    print("\n[STEP] Preprocessing views (A, X)...")
    for idx, (A, X) in enumerate(views):
        use_tfidf = dataset in ["acm", "dblp", "imdb", "photos","aloi", "mfeat","arabidopsis"]  # noqa : E231
        norm_adj, feats = preprocess_dataset(
            A, X, tf_idf=use_tfidf, beta=int(beta)
        )

        if feats.shape[0] * feats.shape[1] > 1e6 and issparse(feats):
            feats = feats.tocsr()
        else:
            feats = feats.toarray() if issparse(feats) else feats

        views[idx] = (norm_adj, feats)

    metrics = {m: [] for m in ["acc", "nmi", "ari", "f1", "loss", "time"]}

    for run_idx in range(runs):
        t0 = time()

        Hs = []
        for view_idx, (S, X) in enumerate(views):

            if issparse(S):
                H = S.dot(X)
            else:
                H = S @ X

            if H.shape[0] * H.shape[1] < 1e6:
                H = H.toarray() if issparse(H) else H
                H_scaled = StandardScaler(with_std=False).fit_transform(H)
            else:
                if issparse(H):
                    H_scaled = H - H.mean(axis=0)
                else:
                    H_scaled = H - np.mean(H, axis=0, keepdims=True)

            Hs.append(H_scaled)

        print("\n[STEP] Training LMGEC model...")
        model = LMGEC(
            n_clusters=k,
            embedding_dim=k + 1,
            temperature=temperature,
            max_iter=max_iter,
            tolerance=tolerance,
        )
        model.fit(Hs)
        print(f"  → Training finished in {len(model.loss_history_)} iterations")  # noqa: E501
        print(f"  → Final loss value: {model.loss_history_[-1]:.4f}")

        y_pred = model.labels_
        metrics["time"].append(time() - t0)
        metrics["acc"].append(clustering_accuracy(labels, y_pred))
        metrics["nmi"].append(nmi(labels, y_pred))
        metrics["ari"].append(ari(labels, y_pred))
        metrics["f1"].append(clustering_f1_score(labels, y_pred, average="macro"))  # noqa: E501
        metrics["loss"].append(model.loss_history_[-1])

        print(f"[SCORE] ACC: {metrics['acc'][-1]:.4f}, F1: {metrics['f1'][-1]:.4f}, "  f"NMI: {metrics['nmi'][-1]:.4f}, ARI: {metrics['ari'][-1]:.4f}")  # noqa: E501, E122, E291

    results = {
        "mean": {k: round(np.mean(v), 4) for k, v in metrics.items()},
        "std": {k: round(np.std(v), 4) for k, v in metrics.items()},
    }

    print("\n[📊 FINAL SUMMARY]")
    print("Means:")
    for k, v in results["mean"].items():
        print(f"  - {k.upper()}: {v}")
    print("\nStandard deviations:")
    for k, v in results["std"].items():
        print(f"  - {k.upper()}: {v}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run LMGEC clustering experiments via CLI."
    )
    parser.add_argument(
        "--dataset", type=str, default="acm",
        help="Dataset to load (e.g., acm, dblp, imdb, photos, wallomics)."
    )
    parser.add_argument(
        "--temperature", type=float, default=1.0,
        help="Temperature for the LMGEC model."
    )
    parser.add_argument(
        "--beta", type=float, default=1.0,
        help="Beta for preprocessing."
    )
    parser.add_argument(
        "--max_iter", type=int, default=10,
        help="Max iterations for convergence."
    )
    parser.add_argument(
        "--tol", type=float, default=1e-7,
        help="Tolerance threshold."
    )
    parser.add_argument(
        "--runs", type=int, default=1,
        help="Number of runs to average."
    )
    args = parser.parse_args()

    run_lmgec_experiment(
        dataset=args.dataset,
        temperature=args.temperature,
        beta=args.beta,
        max_iter=args.max_iter,
        tolerance=args.tol,
        runs=args.runs,
    )
