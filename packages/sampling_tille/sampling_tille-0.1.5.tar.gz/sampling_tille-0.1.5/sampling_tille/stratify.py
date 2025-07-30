"""
This module includes the most popular methods to perform
stratification.
"""

import numpy as np
import shapely
import geopandas as gpd
import pandas as pd
from sklearn.cluster import KMeans


def stratify_bins(x: np.array, num_strata: int) -> np.array:
    """
    A wrapper for numpy digitalize
    :param x: np.array the array containing the data to stratify
    :param num_strata: int the number of strata
    :return: np.array the array containing the stratum of each entry
    """
    bins = np.linspace(0.99 * np.min(x), 1.01 * np.max(x), num_strata + 1)
    return np.digitize(x, bins) - 1


def stratify_quantiles(
    x: np.array, num_strata: int, quantiles: np.array = None
) -> np.array:
    """
    A wrapper for numpy digitalize
    :param x: np.array the array containing the data to stratify
    :param num_strata: int the number of strata
    :param quantiles: np.array optional parameter. If given, it specifies
            the values of the quantiles used to separate the strata.
            If not given, then the quantiles are equally spaced on [0,1].
    :return: np.array the array containing the stratum of each entry
    """
    if quantiles is None:
        quantiles = np.linspace(0, 1, num_strata + 1)[1:-1]
    return np.digitize(x, np.quantile(x, quantiles))


def stratify_kmeans(
    x: np.array, num_strata: int, random_state: int | None = None
) -> np.array:
    """
    Performs a k-means to cluster x into num-strata
    :param x: np.array the array containing the data to stratify
    :param num_strata: int the number of strata
    :param random_state: int optional random seed
    :return: np.array the array containing the cluster of each entry
    """
    if len(np.shape(x)) == 1:
        xn = np.reshape(x, (-1, 1))
    else:
        xn = x
    km = KMeans(n_clusters=num_strata, random_state=random_state)
    y = km.fit_predict(X=xn)
    return y


def stratify_geom(x: np.array, num_strata: int) -> np.array:
    """
    Performs a stratification via geometric progression into num-strata.
    Gives identical results to the R package stratify
    :param x: np.array the array containing the data to stratify
    :param num_strata: int the number of strata
    :return: np.array the array containing the stratum of each entry
    """
    k0 = np.min(x)
    kmax = np.max(x)
    r = (kmax / k0) ** (1 / num_strata)
    s = np.arange(0, num_strata)
    return np.digitize(x, k0 * r**s) - 1


def stratify_square_root(x, num_strata, n_bins: int = None) -> np.array:
    """
    Performs a square-root frequency stratification.
    Verified with bank loans example from Cochran's textbook
    https://rpubs.com/trjohns/stratification
    :param x: np.array the array containing the data to stratify
    :param n_strata: int the number of strata
    :param n_bins: int optionally the number of bins used to compute
            the histogram of x. If None then it's set to 100*len(x)
    :return: np.array the array containing the cluster of each entry
    """
    n = num_strata
    if n_bins is None:
        n_bins = 100 * len(x)
    freq, bins = np.histogram(x, n_bins)
    cs = np.cumsum(np.sqrt(freq))
    step = cs[-1] / n
    out = [np.argmin(np.abs(cs - elem)) for elem in step * np.arange(1, n)]

    return np.digitize(x, bins[out])


def stratify_geo_square_grid(
    gdf: gpd.GeoDataFrame, n_step: int, x_offset: float = 0, y_offset: float = 0
) -> gpd.GeoDataFrame:
    """
    Performs a stratification of a GeoDataFrame into a square grid with a total of nxn squares.
    In order to perform a meaningful stratification the crs of the geodataframe should
    not be expressed a geographic CRS but should be projected.
    :param gdf: the GeoDataFrame to stratify
    :param n_step: the number of steps of each side of a square grid with size equal to
    the major size of the bounding box
    :return:  a copy of the input geodataframe containing and additional column "geo_stratum"
            where the stratum of each row is located.
    """
    crs = gdf.crs
    bsd = gdf.bounds
    x0 = bsd["minx"].min() + x_offset
    x1 = bsd["maxx"].max() + x_offset
    y0 = bsd["miny"].min() + y_offset
    y1 = bsd["maxy"].max() + y_offset
    dx = x1 - x0
    dy = y1 - y0
    delta = max(dx, dy)
    step = delta / float(n_step)

    xv = np.linspace(x0, x0 + delta - step, n_step - 1)
    yv = np.linspace(y0, y0 + delta - step, n_step - 1)
    grid_cells = []
    for x in xv:
        for y in yv:
            grid_cells.append(shapely.geometry.box(x, y, x + step, y + step))
    ind = range(len(grid_cells))
    cell = gpd.GeoDataFrame({"geometry": grid_cells, "geo_stratum": ind}, crs=crs)
    merged = gpd.sjoin_nearest(gdf, cell, how="left")
    merged["geo_stratum"] = merged["geo_stratum"].astype(int)
    map_codes = {
        elem: k for k, elem in enumerate(merged["geo_stratum"].drop_duplicates())
    }
    merged["geo_stratum"] = merged["geo_stratum"].map(map_codes)
    merged["geo_stratum"] = pd.Categorical(merged["geo_stratum"])
    return merged


def stratify_geo_hex_grid(
    gdf: gpd.GeoDataFrame, n_step: int, x_offset: float = 0, y_offset: float = 0
) -> gpd.GeoDataFrame:
    """
    Performs a stratification of a GeoDataFrame into a hexagonal grid.
    In order to perform a meaningful stratification the crs of the geodataframe should
    not be expressed a geographic CRS but should be projected.
    :param gdf: the GeoDataFrame to stratify
    :param n_step: the number of steps of each side of a square grid with size equal to
    the major size of the bounding box
    :return:  a copy of the input geodataframe containing and additional column "geo_stratum"
            where the stratum of each row is located.
    """
    minx, miny, maxx, maxy = gdf.bounds.values[0]
    minx += x_offset
    maxx += x_offset
    miny += y_offset
    maxy += y_offset
    delta = np.maximum(maxx - minx, maxy - miny)
    xstep = delta / n_step
    ystep = xstep * np.sqrt(3) / 2
    dt = []
    for k, yv in enumerate(np.arange(miny, miny + delta, ystep)):
        for xv in np.arange(
            minx - k % 2 * xstep / 2,
            minx + delta + k % 2 * xstep / 2,
            xstep,
        ):
            dt.append([xv, yv])
    dt = np.array(dt).T
    geom = gpd.points_from_xy(dt[0], dt[1])
    pts = gpd.GeoDataFrame(geometry=geom, crs=gdf.crs)
    pts["geo_stratum"] = range(len(pts))
    merged = gpd.sjoin_nearest(gdf, pts, how="left")

    merged["geo_stratum"] = merged["geo_stratum"].astype(int)
    map_codes = {
        elem: k for k, elem in enumerate(merged["geo_stratum"].drop_duplicates())
    }
    merged["geo_stratum"] = merged["geo_stratum"].map(map_codes)
    merged["geo_stratum"] = pd.Categorical(merged["geo_stratum"])
    return merged
