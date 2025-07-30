#############################
# 2. Original metrics.py    #
#############################

"""
Clustering evaluation utilities.

Functions:
- ordered_confusion_matrix: reorder confusion matrix to maximize diagonal.
- cmat_to_psuedo_y_true_and_y_pred: convert confusion matrix.
- clustering_accuracy: compute accuracy from reordered confusion matrix.
- clustering_f1_score: compute macro F1 score after label matching.
"""

import numpy as np
from sklearn import metrics
from scipy.optimize import linear_sum_assignment

def ordered_confusion_matrix(y_true: list, y_pred: list) -> np.ndarray:  # noqa: E302,E501
    conf_mat = metrics.confusion_matrix(y_true, y_pred)
    cost_mat = np.max(conf_mat) - conf_mat
    row_ind, col_ind = linear_sum_assignment(cost_mat)
    return conf_mat[row_ind, :][:, col_ind]

def cmat_to_psuedo_y_true_and_y_pred(cmat: np.ndarray) -> tuple:  # noqa: E302
    y_true, y_pred = [], []
    for true_label, row in enumerate(cmat):
        for pred_label, count in enumerate(row):
            y_true.extend([true_label] * count)
            y_pred.extend([pred_label] * count)
    return y_true, y_pred

def clustering_accuracy(y_true: list, y_pred: list) -> float:  # noqa: E302,E501
    conf_mat = ordered_confusion_matrix(y_true, y_pred)
    return np.trace(conf_mat) / np.sum(conf_mat)

def clustering_f1_score(y_true: list, y_pred: list, **kwargs) -> float:  # noqa: E302, E501
    conf_mat = ordered_confusion_matrix(y_true, y_pred)
    y_t, y_p = cmat_to_psuedo_y_true_and_y_pred(conf_mat)
    return metrics.f1_score(y_t, y_p, **kwargs)
