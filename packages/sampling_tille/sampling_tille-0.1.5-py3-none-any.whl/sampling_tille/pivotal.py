"""
Functions to perform pivotal sampling, as provided by Tillé
"""

import numpy as np
from .sampling import set_rng


def if_value_positive(value: np.array, vpos: np.array, vneg: np.array) -> np.array:
    """
    if value > 0 return vpos else return vneg
    :param value: np.array predicate
    :param vpos: np.array value to return if the predicate is positive
    :param vneg: np.array value to return if the predicate is negative
    :return: np.array vpos or vneg
    """
    return np.heaviside(value, 0.0) * vpos + np.heaviside(-value, 1.0) * vneg


def _update_pivotal_step(pi: np.array, i: int, j: int, unif: float) -> np.array:
    """
    The basic step for the pivotal procedure, as defined in the "Sampling" textbook by Tillé
    :param pi: vector of inclusion probabilities.
            We assume that 0<pi[i]<1 for all i
    :param i: int index of the first element
    :param j: int index of the second element. We assume i != j
    :param unif: float a (uniformly distributed) random number
    :return: np.array the updated inclusion probabilities vector
    """
    out = pi.copy()
    pi_sum = pi[i] + pi[j]
    alpha = if_value_positive(1 - pi_sum, pi[i] / pi_sum, (1 - pi[j]) / (2 - pi_sum))
    x1 = if_value_positive(1 - pi_sum, pi_sum, pi_sum - 1)
    x2 = if_value_positive(1 - pi_sum, 0, 1)

    out[i] = if_value_positive(alpha - unif, x1, x2)
    out[j] = if_value_positive(alpha - unif, x2, x1)

    return out


def _pivotal_random_step(pi: np.array, eps: float, rng: np.random.Generator) -> tuple:
    """
    The step for the pivotal procedure with random choice of the pairs
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: tuple
    """
    out = pi.copy()
    msk = np.abs(out * (1 - out)) > eps
    to_update = np.sum(msk)
    if to_update > 1:
        pi_red = pi[msk]
        i, j = rng.choice(np.arange(len(pi_red)), size=2, replace=False)
        unif = rng.uniform()
        updated = _update_pivotal_step(pi_red, i, j, unif)
        out[msk] = updated
        return out, to_update - 1
    pi_red = pi[msk]
    updated = np.round(pi_red)
    out[msk] = updated
    return out, 0


def pivotal_random(
    pi: np.array, eps: float = 1e-9, rng: np.random.Generator | None = None
):
    """
    Pivotal sampling with random order
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: np.array the vector, containing only 0 or 1, of the updated probabilities.
    The sum of the elements of the output is the rounded sum of the elements of pi
    """
    rng = set_rng(rng)
    cnt = len(pi)
    tmp = pi
    while cnt:
        tmp, cnt = _pivotal_random_step(tmp, eps, rng)
    return tmp


def _pivotal_vector(
    pi: np.array, x: np.array, eps: float, rng: np.random.Generator
) -> tuple:
    """
    The step for the pivotal procedure with pairs determined by x
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param x: np.array 1d vector of the quantity we want to balance. len(x) must be equal to len(pi)
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: tuple
    """

    def get_j(i, m):
        if i == 0:
            return 1
        if i == len(m) - 1:
            return len(m) - 2
        if np.abs(m[i] - m[i + 1]) < np.abs(m[i] - m[i - 1]):
            return i + 1
        return i - 1

    out = pi.copy()
    msk = np.abs(out * (1 - out)) > eps
    to_update = np.sum(msk)
    if to_update > 1:
        pi_red = pi[msk]
        x_red = x[msk]
        i = rng.choice(np.arange(len(pi_red)))
        j = get_j(i, x_red)
        unif = rng.uniform()
        updated = _update_pivotal_step(pi_red, i, j, unif)
        out[msk] = updated
        return out, to_update - 1
    pi_red = pi[msk]
    updated = np.round(pi_red)
    out[msk] = updated
    return out, 0


def pivotal_vector(
    pi: np.array, x: np.array, eps: float = 1e-9, rng: np.random.Generator | None = None
):
    """
    Pivotal sampling with random order
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param x: np.array 1d vector of the quantity we want to balance. len(x) must be equal to len(pi)
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: np.array the vector, containing only 0 or 1, of the updated probabilities.
    The sum of the elements of the output is the rounded sum of the elements of pi
    """
    msk = np.argsort(x)
    pi_sort = pi[msk]
    x_sort = x[msk]
    rng = set_rng(rng)
    cnt = len(pi)
    tmp = pi_sort
    while cnt:
        tmp, cnt = _pivotal_vector(tmp, x_sort, eps, rng)
    return tmp[msk]


def _pivotal_matrix(
    pi: np.array, distance_matrix: np.array, eps: float, rng: np.random.Generator
) -> tuple:
    """
    The step for the pivotal procedure with pairs determined by the distance matrix
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param distance_matrix: np.array 2d square distance matrix of the elements of pi
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: tuple
    """
    out = pi.copy()
    msk = np.abs(out * (1 - out)) > eps
    to_update = np.sum(msk)
    if to_update > 1:
        pi_red = pi[msk]
        # d_mat_red = distance_matrix[msk].T[msk].T
        d_mat_red = distance_matrix[np.ix_(msk, msk)]
        i = rng.choice(np.arange(len(pi_red)))
        j = np.argmin(d_mat_red[i, :])
        unif = rng.uniform()
        updated = _update_pivotal_step(pi_red, i, j, unif)
        out[msk] = updated
        return out, to_update - 1
    pi_red = pi[msk]
    updated = np.round(pi_red)
    out[msk] = updated
    return out, 0


def _get_ij_lp(i: int, d_mat_red: np.array):
    """
    Selection of the i, j pair according to the local pivotal method
    :param i: int the row of the distance matrix
    :param d_mat_red: np.array the distance matrix
    :return:
    """
    j = np.argmin(d_mat_red[i, :])
    if np.argmin(d_mat_red[j, :]) == i:
        return i, j
    return _get_ij_lp(j, d_mat_red)


def _local_pivotal_matrix(
    pi: np.array, distance_matrix: np.array, eps: float, rng: np.random.Generator
) -> tuple:
    """
    The step for the local pivotal procedure with pairs determined by the distance matrix.
    See
    https://academic.oup.com/biometrics/article-abstract/68/2/514/7390733?redirectedFrom=fulltext
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param distance_matrix: np.array 2d square distance matrix of the elements of pi
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :return: tuple
    """

    out = pi.copy()
    msk = np.abs(out * (1 - out)) > eps
    to_update = np.sum(msk)
    if to_update > 1:
        pi_red = pi[msk]
        d_mat_red = distance_matrix[msk].T[msk].T
        i0 = rng.choice(np.arange(len(pi_red)))
        i, j = _get_ij_lp(i0, d_mat_red)
        unif = rng.uniform()
        updated = _update_pivotal_step(pi_red, i, j, unif)
        out[msk] = updated
        return out, to_update - 1
    pi_red = pi[msk]
    updated = np.round(pi_red)
    out[msk] = updated
    return out, 0


def pivotal_distance(
    pi: np.array,
    distance_matrix: np.array,
    eps: float = 1e-9,
    rng: np.random.Generator | None = None,
    method: str = None,
):
    """
    Pivotal sampling performed on the basis on the distance matrix.
    This method randomly selects one item different from 0 or 1 from pi
    and its nearest element, then performs the pivotal step.
    :param pi: vector of inclusion probabilities.
            We assume that 0<=pi[i]<=1 for all i
    :param distance_matrix: np.array 2d square distance matrix of the elements of pi
    :param eps: float: the tolerance
    :param rng: np.random.Generator
    :param method: str|None the method used to compute i and j.
            If "local" it uses the local pivotal method, otherwise it performs an
            ordinary pivotal method.
    :return: np.array the vector, containing only 0 or 1, of the updated probabilities.
    The sum of the elements of the output is the rounded sum of the elements of pi
    """
    ## We make the diagonal elements large enough so we don't have to consider them
    dist_aux = distance_matrix + 2.0 * np.max(distance_matrix) * np.eye(len(pi))
    rng = set_rng(rng)
    cnt = len(pi)
    tmp = pi.copy()
    if method == "local":
        while cnt:
            tmp, cnt = _local_pivotal_matrix(tmp, dist_aux, eps, rng)
        return tmp

    while cnt:
        tmp, cnt = _pivotal_matrix(tmp, dist_aux, eps, rng)
    return tmp
