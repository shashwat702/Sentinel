import numpy as np


def z_score(value, mean, std):

    if std == 0 or np.isnan(std):
        return 0

    return abs((value - mean) / std)