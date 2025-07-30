"""
Routines to sample points on a map
"""

import warnings
import numpy as np
import geopandas as gpd
import pandas as pd
import jax
from jax import numpy as jnp
from sklearn.cluster import KMeans
from scipy.stats.qmc import LatinHypercube
from scipy.stats import spearmanr, kendalltau
from shapely.geometry import Point, LineString
from .utils import set_rng
from .stratify import stratify_quantiles


jit_setdiff1d = jax.jit(jnp.setdiff1d, static_argnames=['size'])

# add periodic component to square grid (a*sin, b*cos)?


def sample_latin_hypercube(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    n: int,
    rng: np.random.Generator = None,
):
    """
    A wrapper of scipy's LatinHypercube
    :param xmin: float the minimum value of the x coordinate
    :param xmax: float the maximum value of the x coordinate
    :param ymin: float the minimum value of the y coordinate
    :param ymax: float the maximum value of the y coordinate
    :param n: the number of points
    :param rng: np.random.Generator optional random number generator
    :return:
    """
    rng = set_rng(rng)
    sampler = LatinHypercube(d=2, rng=rng)
    sample = sampler.random(n=n)
    xv = xmin + sample[:, 0] * (xmax - xmin)
    yv = ymin + sample[:, 1] * (ymax - ymin)
    out = np.array([xv, yv]).T
    return out


def sample_square_grid(
    gdf: gpd.GeoDataFrame,
    num_points: int,
    x_offset: float = 0,
    y_offset: float = 0,
    sigma: float = 0.0,
    rng: np.random.Generator = None,
    assume_coverage: bool = False,
) -> gpd.GeoDataFrame:
    """
    Returns an equally spaced grid of points in gdf
    :return:
    :param gdf: GeoDataFrame where the points are needed.
    We assume that the geometry is made by polygon.
    :param num_points: maximum number of points for each side
    :param x_offset: x offset, default to 0
    :param y_offset: y offset, default to 0
    :param sigma: float default to 0 if given adds a normal component with
        corresponding standard deviation and zero mean
    :param rng: optional numpy random number generator
    :param assume_coverage: boolean default to false.
        If true the method coverage is used to compute union_all,
        making computation generally faster
    :return: a GeoDataFrame containing the set of points forming a grid.
    """
    rng = set_rng(rng)
    if not assume_coverage:
        g1 = gdf.union_all()
    else:
        g1 = gdf.union_all(method="coverage")
    minx, miny, maxx, maxy = g1.bounds
    delta = np.maximum(maxx - minx, maxy - miny)
    dx = x_offset + np.linspace(minx, minx + delta, num_points)
    dy = y_offset + np.linspace(miny, miny + delta, num_points)
    xv, yv = np.meshgrid(dx, dy)
    xv = xv.reshape(-1)
    yv = yv.reshape(-1)
    if sigma:
        xv += sigma * rng.normal(size=len(xv))
        yv += sigma * rng.normal(size=len(yv))
    geom = gpd.points_from_xy(xv, yv)
    pts = gpd.GeoDataFrame(geometry=geom, crs=gdf.crs)
    filtered = pts[pts.within(g1)]
    filtered = filtered.reset_index().drop(columns="index")
    return filtered


def sample_hex_grid(
    gdf: gpd.GeoDataFrame,
    num_points: int,
    x_offset: float = 0,
    y_offset: float = 0,
    sigma: float = 0,
    rng: np.random.Generator = None,
    assume_coverage: bool = False,
) -> gpd.GeoDataFrame:
    """
    Returns the points on a hexagonal lattice in gdf
    :param gdf: GeoDataFrame where the points are needed.
    We assume that the geometry is made by polygon.
    :param num_points: maximum number of points for each side
    :param x_offset: x offset, default to 0
    :param y_offset: y offset, default to 0
    :param sigma: float default to 0 if given adds a normal component with
        corresponding standard deviation and zero mean
    :param rng: optional numpy random number generator
    :param assume_coverage: boolean default to false.
        If true the method coverage is used to compute union_all,
        making computation generally faster
    :return: a GeoDataFrame containing the set of points forming the lattice.
    """
    rng = set_rng(rng)
    if not assume_coverage:
        g1 = gdf.union_all()
    else:
        g1 = gdf.union_all(method="coverage")
    minx, miny, maxx, maxy = g1.bounds
    delta = np.maximum(maxx - minx, maxy - miny)
    xstep = delta / num_points
    ystep = xstep * np.sqrt(3) / 2
    dt = []
    for k, yv in enumerate(np.arange(miny + y_offset, miny + delta + y_offset, ystep)):
        for xv in np.arange(
            minx - k % 2 * xstep / 2 + x_offset,
            minx + delta + k % 2 * xstep / 2 + x_offset,
            xstep,
        ):
            dt.append([xv, yv])
    dt = np.array(dt).T
    if sigma:
        dt += sigma * rng.normal(size=np.shape(dt))
    geom = gpd.points_from_xy(dt[0], dt[1])
    pts = gpd.GeoDataFrame(geometry=geom, crs=gdf.crs)
    filtered = pts[pts.within(g1)]
    filtered = filtered.reset_index().drop(columns="index")
    return filtered


def sample_uniform_points(
    gdf: gpd.GeoDataFrame,
    num_points: int,
    mult: float = 5,
    rng: np.random.Generator = None,
    assume_coverage: bool = False,
) -> gpd.GeoDataFrame:
    """
    Returns a set of uniformly distributed points in gdf
    :param gdf: GeoDataFrame where the points are needed.
    We assume that the geometry is made by polygon.
    :param num_points: maximum number of points for each side
    :param mult: optional positive parameter if given increases the number
        of sampled points by the corresponding factor. Default to 5.
    :param rng: optional numpy random number generator
    :param assume_coverage: boolean default to false.
        If true the method coverage is used to compute union_all,
        making computation generally faster
    :return: a GeoDataFrame containing the set of points forming a grid.
    """
    rng = set_rng(rng)
    if not assume_coverage:
        g1 = gdf.union_all()
    else:
        g1 = gdf.union_all(method="coverage")
    minx, miny, maxx, maxy = g1.bounds
    k = int(num_points * mult * (maxx - minx) * (maxy - miny) / g1.area)
    xv = rng.uniform(minx, maxx, size=k)
    yv = rng.uniform(miny, maxy, size=k)
    geom = gpd.points_from_xy(xv, yv)
    pts = gpd.GeoDataFrame(geometry=geom, crs=gdf.crs)
    filtered = pts[pts.within(g1)]
    filtered = filtered.iloc[:num_points]
    filtered = filtered.reset_index().drop(columns="index")
    return filtered


def spatial_coverage_sampling(
    num_strata: int,
    xv: np.array,
    yv: np.array,
    rng: np.random.Generator,
    max_iter: int = 100,
    tol: float = 5e-2,
):
    """
    Performs a spatial coverage sampling, as described in
    https://www.sciencedirect.com/science/article/abs/pii/S0166248106310148
    :param num_strata: int number of desired strata
    :param xv: np.array x coordinates of the (masked) raster
    :param yv: np.array y coordinates of the (masked) raster
    :param rng: np.random.Generator
    :param max_iter: maximum number of iterations
    :param tol: relative tolerance of the iterative algorithm
    :return: np.array the coordinates of the sampled points
    """
    rng = set_rng(rng)
    rs = rng.integers(0, 10000)
    ind = rng.choice(range(len(xv)), size=num_strata, replace=False)
    Xtrain = np.array([xv[ind], yv[ind]]).T
    converged = False
    for _ in range(max_iter):
        if not converged:
            Xpred = np.array([xv, yv]).T
            km = KMeans(n_clusters=num_strata, random_state=rs).fit(Xtrain)
            ypred = km.predict(Xpred)
            Xnew = np.array(
                [np.mean(Xpred[ypred == s], axis=0) for s in range(0, num_strata)]
            )
            err = np.max(
                np.abs(
                    (Xtrain - Xnew) / (np.max(Xpred, axis=0) - np.min(Xpred, axis=0))
                )
            )
            if err < tol:
                converged = True
            else:
                Xtrain = Xnew
    return Xnew


def _update_init(v0, d, theta):
    v1 = v0 + d * np.array([np.cos(2.0 * np.pi * theta), np.sin(2.0 * np.pi * theta)])
    return v1


def _draw_initial_equidistant(dist, geom, size, rng: np.random.Generator):
    rng = set_rng(rng)
    v0 = rng.uniform(size=2)
    minx, miny, maxx, maxy = tuple(geom.bounds.values[0])
    xs = np.array([minx + v0[0] * (maxx - minx), miny + v0[1] * (maxy - miny)])
    while not geom.contains(Point(xs)).all():
        v0 = rng.uniform(size=2)
        xs = np.array([minx + v0[0] * (maxx - minx), miny + v0[1] * (maxy - miny)])
    tmp = [xs]
    while len(tmp) < size:
        s1 = rng.uniform()
        vn = _update_init(tmp[-1], dist, s1)
        if geom.contains(Point(vn)).all():
            tmp.append(vn)
    return np.array(tmp)


def _draw_update_equidistant(
    dist, geom, xold, size: int = 1, rng: np.random.Generator = None
):
    tmp = []
    out = []
    rng = set_rng(rng)
    for _, x in enumerate(xold):
        for _ in range(size):
            is_inside = False
            while not is_inside:
                s1 = rng.uniform()
                vn = _update_init(x, dist, s1)
                if geom.contains(Point(vn)).all():
                    is_inside = True
                    tmp.append(vn)
                    out.append(LineString(np.array([x, vn])))
    return np.array(tmp), out


def draw_equidistant_points(
    geom: gpd.GeoDataFrame,
    num: int,
    dist: list[float],
    reps: list[int] = None,
    rng: np.random.Generator = None,
):
    """
    Draws samples with fixed distances to investigate distance dependence
    as proposed in
        https://precision-agriculture.sydney.edu.au/wp-content/uploads/2019/08/YoudenMehlich.pdf
    :param geom: geopandas.GeoDataFrame determines the boundary of the sampling region
    :param num: number of points in the initial set
    :param dist: list[float] distance between the points
    :param reps: list[int] optional number of repetitions in the subsequent steps.
        Default to 1. Its size must be len(dist)-1.
    :param rng: np.random.Generator optional random number generator
    :return: tuple made by two items. The first one is the set of points, the second
            is a geodataframe where points with fixed distance are linked by a line.
            In the geodataframe the column "scale" corresponds to the distance of the corresponding
            class, the "class" column to the number of class (from 0 to len(dist))
    """
    rng = set_rng(rng)
    pts = _draw_initial_equidistant(dist[0], geom, size=num, rng=rng)
    l0 = LineString(pts)

    g0 = gpd.GeoDataFrame(
        geometry=[l0], crs=geom.crs, data={"scale": [dist[0]], "class": [str(0)]}
    )
    out = [g0]
    for k, d in enumerate(dist[1:]):
        if reps:
            ptsn, ln = _draw_update_equidistant(d, geom, pts, size=reps[k], rng=rng)
        else:
            ptsn, ln = _draw_update_equidistant(d, geom, pts, size=1, rng=rng)
        pts = np.array(list(pts) + list(ptsn))
        cats = [str(k + 1)] * len(ln)
        out += [
            gpd.GeoDataFrame(
                geometry=ln, crs=geom.crs, data={"scale": [d] * len(ln), "class": cats}
            )
        ]
    return pts, pd.concat(out)


def _corr(mat, method: str = "Kendall"):
    out = np.ones(len(mat))
    if method == "Pearson":
        out = np.corrcoef(mat)
    elif method == "Spearman":
        out = np.array([[spearmanr(x, y).statistic for x in mat] for y in mat])
    elif method == "Kendall":
        out = np.array([[kendalltau(x, y).statistic for x in mat] for y in mat])
    return np.nan_to_num(out, nan=5)


def conditional_latin_hypercube_legacy(
    X: np.array,
    n: int,
    beta: float = 0.1,
    num_iter: int = 10000,
    Xcat: np.array = None,
    p: float = 0.2,
    thr: float = 0.2,
    rng: np.random.Generator = None,
) -> np.array:
    """
    Performs a conditional latin hypercube sampling. Limited to continuous covariates
    :param X: np.array, array of continuous covariates
    :param n: int number of units in the sample
    :param Xcat: np.array, optional array of coategorical covariates
    :param beta: optional float 0<beta<1 reverse temperature
    :param num_iter: maximum number of iterations
    :param p: optional float 0 <=p<=1  probability of random replacement of a unit in the sample
        see Budiman McBratney
    :param thr: tolerance if the loss function is less than this parameter, the algorithm stops
    :param rng: np.random.Generator optional random number generator
    :return: np.array the indexes of the units in the sample
    """
    rng = set_rng(rng)
    decr = 1.02
    N = np.shape(X)[0]
    qi = np.linspace(0, 1, n + 1)
    Qi = [np.quantile(X.T, q=qq, axis=1) for qq in qi]
    base_set = np.arange(N)
    assert len(qi) == n + 1

    # Xall = X
    method = "Pearson"
    if Xcat is not None:
        method = "Pearson"
        cats = np.array([np.unique(elem) for elem in Xcat.T])
        kappa = np.array(
            [np.unique(elem, return_counts=True)[1] for elem in Xcat.T]
        ) / len(Xcat)
        # Xall = np.concat([X, Xcat], axis=1)

    T = _corr(X.T, method=method)
    ww1 = 1
    ww2 = 1
    ww3 = 1

    def _get_loss(sample):
        x = X[:][sample]
        t = _corr(x.T, method=method)
        o1 = np.sum(np.abs(t - T))
        qmat = get_qmat(Qi, X, n, sample)
        o2 = 0
        if Xcat is not None:
            px = _compute_px(Xcat, cats, n, sample)
            o2 = np.sum(np.abs(kappa - px))
        o3 = np.sum(np.abs(qmat - 1))
        loss = ww1 * o1 + ww2 * o2 + ww3 * o3
        return loss, qmat

    sample = rng.choice(np.arange(N), replace=False, size=n)
    loss, qmat = _get_loss(sample)

    sample_old = sample
    loss_old = loss
    # reserv = list(set().difference(set(sample)))
    # reserv = np.setdiff1d(base_set, sample)
    for _ in range(num_iter):
        if loss > thr:
            # print(k)
            sample = rng.choice(np.arange(N), replace=False, size=n)
            loss, qmat = _get_loss(sample)
            if loss < loss_old:
                sample_old = sample
                loss_old = loss
                # reserv = list(set(range(N)).difference(set(sample)))
                # reserv = np.setdiff1d(base_set, sample)
            else:
                u = rng.uniform()
                if u > np.exp(-beta * (loss - loss_old)):
                    # print(f"Acc: {loss}, {loss_old}, {u}, {np.exp(-beta*(loss-loss_old))}")
                    sample_old = sample
                    loss_old = loss
                    # reserv = list(set(range(N)).difference(set(sample)))
                    # reserv = np.setdiff1d(base_set, sample)
            rnd = rng.uniform()
            if rnd < p:


                reserv = jit_setdiff1d(base_set, sample, size=N-n)
                # reserv = np.setdiff1d(base_set, sample, assume_unique=True)
                snew = rng.choice(np.arange(n))
                vnew = rng.choice(reserv)
                sample[snew] = vnew
                loss, qmat = _get_loss(sample)
                sample_old = sample
                loss_old = loss
            else:
                reserv = jit_setdiff1d(base_set, sample, size=N-n)
                snew = np.argmax(np.max(qmat, axis=1))
                vnew = rng.choice(reserv)
                sample[snew] = vnew
                loss, qmat = _get_loss(sample)
                sample_old = sample
                loss_old = loss
            beta *= decr
        else:
            return sample
    warnings.warn(
        """Algorithm did not converge.
     Consider relaxing the constraints or using another sampling method."""
    )
    return sample_old


def _compute_px(Xcat, cats, n, sample):
    px = np.array(
        [
            np.array(
                [
                    np.sum((Xcat[sample].T[l] == elem).astype(int)) / n
                    for elem in cats[l]
                ]
            )
            for l in range(np.shape(Xcat)[1])
        ]
    )
    return px


def get_qmat(Qi, X, n, sample):
    """Computes the occupation matrix of the strata"""
    qmat = np.array(
        [
            np.sum(
                np.array(
                    [
                        [
                            (np.array(Qi).T[l][k - 1] <= elem < np.array(Qi).T[l][k])
                            for elem in X[sample].T[l]
                        ]
                        for k in np.arange(1, n + 1)
                    ]
                ).astype(int),
                axis=1,
            )
            for l in range(np.shape(X)[1])
        ]
    )
    return qmat


def conditional_latin_hypercube(
    X: np.array,
    n: int,
    beta: float = 0.1,
    num_iter: int = 10000,
    Xcat: np.array = None,
    thr: float = 0.2,
    rng: np.random.Generator = None,
) -> np.array:
    """
    Performs a conditional latin hypercube sampling.
    :param X: np.array, array of continuous covariates
    :param n: int number of units in the sample
    :param Xcat: np.array, optional array of coategorical covariates
    :param beta: optional float 0<beta<1 reverse temperature
    :param num_iter: maximum number of iterations
    :param p: optional float 0 <=p<=1  probability of random replacement of a unit in the sample
        see Budiman McBratney
    :param thr: tolerance if the loss function is less than this parameter, the algorithm stops
    :param rng: np.random.Generator optional random number generator
    :return: np.array the indexes of the units in the sample
    """
    rng = set_rng(rng)
    decr = 1.02
    N = np.shape(X)[0]
    qi = np.linspace(0, 1, n + 1)
    Qi = [np.quantile(X.T, q=qq, axis=1) for qq in qi]
    base_set = np.arange(N)
    assert len(qi) == n + 1

    Xall = X
    method = "Pearson"
    if Xcat is not None:
        method = "Kendall"
        cats = np.array([np.unique(elem) for elem in Xcat.T])
        kappa = np.array(
            [np.unique(elem, return_counts=True)[1] for elem in Xcat.T]
        ) / len(Xcat)
        Xall = np.concat([X, Xcat], axis=1)

    T = _corr(Xall.T, method=method)
    ww1 = 1
    ww2 = 1
    ww3 = 1

    def _get_loss(sample):
        x = Xall[:][sample]
        t = _corr(x.T, method=method)
        o1 = np.sum(np.abs(t - T))
        qmat = get_qmat(Qi, X, n, sample)
        o2 = 0
        if Xcat is not None:
            px = _compute_px(Xcat, cats, n, sample)
            o2 = np.sum(np.abs(kappa - px))
        o3 = np.sum(np.abs(qmat - 1))
        loss = ww1 * o1 + ww2 * o2 + ww3 * o3
        return loss, qmat
    def _choose_item(Qi, X, nn, on, p: float=0):
        # find under-represented strata
        alpha = rng.uniform()
        if alpha < p:
            s = rng.choice(range(n))
            l = rng.choice(range(n), size=s, replace=False)
            h = rng.choice(range(N), size=s, replace=False)
            on[l] = h
            return on, True
        else:
            cchs = (get_qmat(Qi, X, nn, on)<1).astype(int)
            lind = np.argmax(np.sum(cchs, axis=1))
            lind1 = np.argmax(np.sum(cchs, axis=0))
            selct = np.arange(n)[(cchs[lind]).astype(bool)]
            # reservoir
            to_choose = np.invert(np.isin(np.arange(N), on))
            sstrats = np.array([stratify_quantiles(X.T[l], num_strata=n) for l in range(np.shape(X)[1])])
            p0 = np.isin(sstrats[lind], selct).astype(int)
            p1 = np.invert(np.isin(np.arange(N), on)).astype(int)
            msk = (p0*p1).astype(bool)
            status = False
            if np.sum(msk):
                inew = rng.choice(np.arange(N)[msk])
                on[lind1] = inew
                status = True

            return on, status
    sample = rng.choice(np.arange(N), replace=False, size=n)
    loss, qmat = _get_loss(sample)
    sample_old = sample
    loss_old = loss
    #print(f"Loss: {loss_old}")
    # reserv = list(set().difference(set(sample)))
    # reserv = np.setdiff1d(base_set, sample)
    status = True
    for _ in range(num_iter):
        if ((loss_old > thr) and status):
            sample, status = _choose_item(Qi, X, n, sample_old, p=0.2)
            loss, qmat = _get_loss(sample)
            #print(f"Loss: {loss}")
            u = rng.uniform()
            if u > np.exp(-beta * (loss - loss_old)):
                sample_old = sample
                loss_old = loss
                #print(f"Loss: {loss_old}")
        else:
            return sample_old
    warnings.warn(
        """Algorithm did not converge.
     Consider relaxing the constraints or using another sampling method."""
    )
    return sample_old