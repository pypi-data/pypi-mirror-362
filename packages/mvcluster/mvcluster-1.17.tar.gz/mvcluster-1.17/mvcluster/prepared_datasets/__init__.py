import os
from scipy.io import loadmat

# Path helper for local file access


def _dataset_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def load_mfeat():
    return loadmat(_dataset_path("mfeat.mat"))


def load_aloi():
    return loadmat(_dataset_path("aloi.mat"))


def load_arabidopsis():
    return loadmat(_dataset_path("arabidopsis.mat"))


__all__ = ["load_mfeat", "load_aloi", "load_arabidopsis"]
