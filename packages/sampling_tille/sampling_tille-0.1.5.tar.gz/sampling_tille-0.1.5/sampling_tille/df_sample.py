"""
Implementation of the sampling methods directly to pandas dataframe.
"""

import numpy as np
import geopandas as gpd
import pandas as pd
from scipy.spatial.distance import squareform, pdist
from sampling_tille import (
    srswor,
    stratified_sampling,
    systematic_sampling,
    cluster_sampling,
    cube_sample,
    pivotal_random,
    pivotal_distance,
    spread_balanced_sampling,
)


def normalize(df: pd.DataFrame, columns: list[str], norm: str | None) -> pd.DataFrame:
    """
    Performs a normalization of the columns of a dataframe
    :param df: pd.DataFrame
    :param columns: list[str] the columns to normalize
    :param norm: str the normalization strategy.
            Allowed values are "minmax", "std" or None
    :return: pd.DataFrame the dataframe containing the normalzied columns
    """
    if norm == "minmax":
        X = (df[columns] - df[columns].min()) / (df[columns].max() - df[columns].min())
    elif norm == "std":
        X = (df[columns] - df[columns].mean()) / (df[columns].std())
    elif norm is None:
        X = df[columns]
    else:
        raise ValueError(
            'Unknown value for "norm". Allowed values are "minmax", "std" or None.'
        )
    return X


def sample(
    df: pd.DataFrame,
    n: int,
    kind: str = "simple",
    rng: np.random.Generator | None = None,
    columns: list[str] | str | None = None,
    method: str | None = None,
    balance: list[str] | None = None,
    proba: np.array = None,
    norm: str = "minmax",
) -> np.array:
    """
    performs sampling on pandas dataframe.
    :param df: pd.DataFrame the dataframe containing the information of the sample
    :param n: int the number of desired elements in the sample.
    :param kind: str|none
        The desired sampling kind.
        Valid values are "simple", "cluster", "stratified", "systematic", "balanced" or "pivotal".
        Default is simple
    :param rng: np.random.Generator|None the random number generator.
    :param columns: list(str) The columns where the stratification,
            clustering or pivoting is desired.
            Only used for "stratified", "cluster", "pivotal" or "balanced" kind.
            If kind is "cluster" then only the first item is considered.
            The corresponding columns are assumed/converted to categorical
                if "kind" is "stratified" or "cluster2.
    :param method: str|None The method used to compute the probabilities.
            If "kind"="stratified", valid values are "proportional" or "equal_size".
            If "kind"="pivotal" then, if "method"="local" a local pivotal sampling
            is performed, otherwise a normal pivotal sampling is performed.
    :param balance: list(str)|None The columns where the balancing is desired.
            Only considered if method is "balanced".
    :param proba: np.array|None optional parameter for the sampling probabilities
    :param norm: normalization used to compute the distance for the pivotal
            sampling. If "minmax" then the min-max scaling is performed,
            if "std" then the ordinary normalization is performed,
            if None then no normalization is performed. Default is minmax.
    :return: np.array(bool): The mask representing the sample.

    >>> import numpy as np
    >>> from sampling_tille.load_data import load_data
    >>> from sampling_tille.df_sample import sample
    >>> df = load_data('fertility')
    >>> rng = np.random.default_rng(42)
    >>> mask = sample(df, n=20, rng=rng)
    >>> df_out = df[mask]
    >>> df_out.head()
           rownames morekids gender1 gender2  age afam hispanic other  work
    16085     16086      yes  female  female   35   no       no    no    48
    23850     23851       no    male    male   24   no       no    no     0
    32513     32514      yes  female  female   30   no       no    no     0
    57978     57979      yes    male    male   32   no       no    no     0
    94373     94374      yes  female    male   30   no       no    no     0

    """
    if isinstance(columns, str):
        columns = [columns]

    match kind:
        case "simple":
            mask = srswor(n, len(df), rng=rng)
        case "cluster":
            mask = cluster_sampling(
                n,
                pd.Categorical(df[columns[0]]).codes,
                rng=rng,
                method=method,
                proba=proba,
            )
        case "stratified":
            cols = np.array([pd.Categorical(df[col]).codes for col in columns]).T
            mask = stratified_sampling(n, cols, method=method, rng=rng, proba=proba)
        case "systematic":
            mask = systematic_sampling(n, len(df), rng=rng)
        case "balanced":
            if proba is None:
                pi0 = np.ones(len(df)) / len(df) * n
            else:
                pi0 = proba / np.sum(proba) * n
            m = np.ones(len(df))
            if columns:
                m1 = pd.get_dummies(df[columns], drop_first=True).astype(int).values
                m = np.vstack([m.T, m1.T]).T
            if balance:
                m2 = df[balance].values
                m = np.vstack([m.T, m2.T]).T
            if not balance and not columns:
                raise ValueError(
                    '''If "kind" is "balanced",
                 at least one between "columns" and "balance" must be given.
                 Alternatively you can use "kind"="simple"'''
                )
            if proba is not None:
                mask = cube_sample(pi0, m, rng=rng, pi0=proba)
            else:
                mask = cube_sample(pi0, m, rng=rng)
        case "pivotal":
            if proba is None:
                pi = np.ones(len(df)) / len(df) * n
            else:
                pi = proba / np.sum(proba) * n
            if columns is None:
                mask = pivotal_random(pi, rng=rng)
            else:
                X = normalize(df, columns, norm)
                mat = squareform(pdist(X.iloc[:, 1:]))
                match method:
                    case "local":
                        mask = pivotal_distance(pi, mat, rng=rng, method="local")
                    case _:
                        mask = pivotal_distance(pi, mat, rng=rng)
        case _:
            raise ValueError(
                """Unknown method.
             Valid methods are simple, cluster, systematic, stratified, pivotal or balanced"""
            )
    return mask.astype(bool)


def two_stage_sampling(
    df: pd.DataFrame,
    n: int,
    n_clusters: int,
    clustering_col: str,
    rng: np.random.Generator = None,
    kind: str = "simple",
    method: str | None = None,
    proba: np.array = None,
    **stage_two_kwargs,
) -> np.array:
    """
    Performs a two stage sampling
    :param df: pd.DataFrame the dataframe containing the information of the sample
    :param n: int number of elements in the sample
    :param n_clusters: int number of clusters
    :param clustering_col: str column to use to cluster the units
    :param rng: np.random.Generator
    :param kind: str the sampling method to use in the second stage
    :param method: the method used in the first stage
    :param proba: the probabilities used in the first stage
    :param stage_two_kwargs: arguments to use in the second stage sampling,
        see the sample function help(sample).
    :return: np.array
    """
    mask_cluster = sample(
        df,
        n=n_clusters,
        rng=rng,
        kind="cluster",
        columns=[clustering_col],
        method=method,
        proba=proba,
    )
    clusters = df[mask_cluster][clustering_col].drop_duplicates()

    mask_total = mask_cluster.astype(int)

    for cluster in clusters:
        mask_single = df[clustering_col] == cluster
        df_red = df[mask_single]
        msk = sample(df_red, n // n_clusters, rng=rng, kind=kind, **stage_two_kwargs)
        mask_total[mask_single] = msk
    return mask_total.astype(bool)


def gdf_spread_balanced_sample(
    gdf: gpd.GeoDataFrame,
    n: int,
    columns: list[str] = None,
    balance: list[str] = None,
    eps: float = 1e-11,
    proba: np.array = None,
    rng: np.random.Generator = None,
) -> np.array:
    """
    Performs a spread balanced sampling
    :param gdf: gpd.GeoDataFramethe dataframe containing the information of the sample
    :param n: int the number of desired elements in the sample.
    :param columns: list(str) The columns where the stratification,
        clustering or pivoting is desired.
        Only used for "stratified", "cluster", "pivotal" or "balanced" kind.
        If kind is "cluster" then only the first item is considered.
        The corresponding columns are assumed/converted to categorical
            if "kind" is "stratified" or "cluster2.
    :param balance: list(str)|None The columns where the balancing is desired.
            Only considered if method is "balanced".
    :param proba: np.array|None optional parameter for the sampling probabilities
    :param rng: np.random.Generator|None the random number generator.
    :return: np.array
    """
    coords = gdf.get_coordinates().values

    if proba is not None:
        pi0 = proba / np.sum(proba) * n
    else:
        pi0 = np.ones(len(gdf)) / len(gdf) * n
    m = np.ones(len(gdf))
    if columns:
        m1 = pd.get_dummies(gdf[columns], drop_first=True).astype(int).values
        m = np.vstack([m.T, m1.T]).T
    if balance:
        m2 = gdf[balance].values
        m = np.vstack([m.T, m2.T]).T
    pi = spread_balanced_sampling(pi0, m, coords, eps=eps, rng=rng)
    return pi
