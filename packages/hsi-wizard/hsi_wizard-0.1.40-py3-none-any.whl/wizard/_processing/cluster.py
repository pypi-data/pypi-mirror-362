"""
_processing/cluster.py
========================

.. module:: cluster
:platform: Unix
:synopsis: Initialization of the exploration package for hsi-wizard.

Module Overview
---------------

This module initializes the cluster functions of the hsi-wizard package.

Functions
---------

.. autofunction:: isodata
.. autofunction:: smooth_kmneas


Credits
-------
The Isodata code was inspired by:
- Repository: pyRadar
- Author/Organization: PyRadar
- Original repository: https://github.com/PyRadar/pyradar/
"""

import numpy as np
from scipy.cluster.vq import vq
from scipy.ndimage import uniform_filter, gaussian_filter
from typing import Tuple
from typing import Optional
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.decomposition import PCA
from sklearn.feature_extraction.image import grid_to_graph
from scipy.signal import convolve2d


def _quit_low_change_in_clusters(centers: np.ndarray, last_centers: np.ndarray, theta_o: float) -> bool:
    """
    Determine if cluster update change is below the threshold to stop iteration.

    Compares current and previous cluster centers and stops if all changes are below `theta_o`.

    Parameters
    ----------
    centers : np.ndarray
        Current cluster centers.
    last_centers : np.ndarray
        Cluster centers from the previous iteration.
    theta_o : float
        Threshold for the percent change in cluster centers.

    Returns
    -------
    bool
        True if change is below the threshold and iteration should stop, False otherwise.
    """
    qt = False
    if centers.shape == last_centers.shape:
        thresholds = np.abs((centers - last_centers) / (last_centers + 1))

        if np.all(thresholds <= theta_o):  # percent of change in [0:1]
            qt = True

    return qt


def _discard_clusters(img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Remove clusters with fewer members than the minimum threshold.

    Parameters
    ----------
    img_class_flat : np.ndarray
        Flattened image class labels.
    centers : np.ndarray
        Cluster centers.
    clusters_list : np.ndarray
        List of cluster labels.
    theta_m : int
        Minimum number of pixels per cluster.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int]
        Updated centers, cluster list, and number of clusters.
    """
    k_ = centers.shape[0]
    to_delete = np.array([])
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        total_per_cluster = indices.size
        if total_per_cluster <= theta_m:
            to_delete = np.append(to_delete, cluster)

    if to_delete.size:
        to_delete = np.array(to_delete, dtype=int)
        new_centers = np.delete(centers, to_delete, axis=0)
        new_clusters_list = np.delete(clusters_list, to_delete)
    else:
        new_centers = centers
        new_clusters_list = clusters_list

    # new_centers, new_clusters_list = sort_arrays_by_first(new_centers, new_clusters_list)
    assert new_centers.shape[0] == new_clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"

    return new_centers, new_clusters_list, k_


def _update_clusters(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Update cluster centers based on the current assignments.

    Parameters
    ----------
    img_flat : np.ndarray
        Flattened image pixels.
    img_class_flat : np.ndarray
        Flattened image class labels.
    centers : np.ndarray
        Current cluster centers.
    clusters_list : np.ndarray
        List of cluster labels.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int]
        Updated centers, cluster list, and number of clusters.
    """
    k_ = centers.shape[0]
    new_centers = np.zeros((k_, img_flat.shape[1]))
    new_clusters_list = np.array([])

    if centers.shape[0] != clusters_list.size:
        raise ValueError(
            "ERROR: update_clusters() centers and clusters_list size are different"
        )

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        # get whole cluster
        cluster_values = img_flat[indices, :]
        new_cluster = cluster_values.mean(axis=0)
        new_centers[cluster, :] = new_cluster
        new_clusters_list = np.append(new_clusters_list, cluster)

    new_centers, new_clusters_list = _sort_arrays_by_first(new_centers, new_clusters_list)

    if new_centers.shape[0] != new_clusters_list.size:
        raise ValueError(
            "ERROR: update_clusters() centers and clusters_list size are different after sorting"
        )

    return new_centers, new_clusters_list, k_


def _initial_clusters(img_flat: np.ndarray, k_: int, method: str = "linspace") -> np.ndarray | None:
    """
    Generate initial cluster centers.

    Parameters
    ----------
    img_flat : np.ndarray
        Flattened image pixels.
    k_ : int
        Number of clusters.
    method : str, optional
        Initialization method: 'linspace' or 'random'.

    Returns
    -------
    np.ndarray | None
        Initial cluster centers or None on error.
    """
    methods_available = ["linspace", "random"]
    v = img_flat.shape[1]
    assert method in methods_available, f"ERROR: method {method} is not valid."
    if method == "linspace":
        maximum, minimum = img_flat.max(axis=0), img_flat.min(axis=0)
        centers = np.array([np.linspace(minimum[i], maximum[i], k_) for i in range(v)]).T
    elif method == "random":
        start, end = 0, img_flat.shape[0]
        indices = np.random.randint(start, end, k_)
        centers = img_flat[indices]
    else:
        return None

    return centers


def _sort_arrays_by_first(centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sort centers and cluster labels based on the first feature.

    Parameters
    ----------
    centers : np.ndarray
        Cluster centers.
    clusters_list : np.ndarray
        Cluster label array.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Sorted centers and cluster list.
    """
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: sort_arrays_by_first centers and clusters_list size are not equal"

    indices = np.argsort(centers[:, 0])

    sorted_centers = centers[indices, :]
    sorted_clusters_list = clusters_list[indices]

    return sorted_centers, sorted_clusters_list


def _split_clusters(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, theta_s: float, theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Split a cluster if its standard deviation exceeds a threshold.

    Parameters
    ----------
    img_flat : np.ndarray
        Flattened image pixels.
    img_class_flat : np.ndarray
        Flattened image class labels.
    centers : np.ndarray
        Cluster centers.
    clusters_list : np.ndarray
        Cluster label array.
    theta_s : float
        Standard deviation threshold for splitting.
    theta_m : int
        Minimum pixel count per cluster.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int]
        Updated centers, cluster list, and number of clusters.
    """

    assert centers.shape[0] == clusters_list.size, "ERROR: split() centers and clusters_list size are different"

    delta = 10
    k_ = centers.shape[0]
    count_per_cluster = np.zeros(k_)
    stddev = np.array([])

    avg_dists_to_clusters, k_ = _compute_avg_distance(img_flat, img_class_flat, centers, clusters_list)
    d, k_ = _compute_overall_distance(img_class_flat, avg_dists_to_clusters, clusters_list)

    # compute all the standard deviation of the clusters
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        count_per_cluster[cluster] = indices.size
        value = ((img_flat[indices] - centers[cluster]) ** 2).sum()
        value /= count_per_cluster[cluster]
        value = np.sqrt(value)
        stddev = np.append(stddev, value)

    cluster = stddev.argmax()
    max_stddev = stddev[cluster]
    max_clusters_list = int(clusters_list.max())

    if max_stddev > theta_s:
        if avg_dists_to_clusters[cluster] >= d:
            if count_per_cluster[cluster] > (2.0 * theta_m):
                old_cluster = centers[cluster, :]

                new_cluster_1 = old_cluster + delta
                new_cluster_1 = new_cluster_1.reshape(1, -1)
                new_cluster_2 = old_cluster - delta
                new_cluster_2 = new_cluster_2.reshape(1, -1)

                centers = np.delete(centers, cluster, axis=0)
                clusters_list = np.delete(clusters_list, cluster)

                centers = np.concatenate((centers, new_cluster_1), axis=0)
                centers = np.concatenate((centers, new_cluster_2), axis=0)
                clusters_list = np.append(clusters_list, max_clusters_list + 1)
                clusters_list = np.append(clusters_list, max_clusters_list + 2)

                centers, clusters_list = _sort_arrays_by_first(centers, clusters_list)

                assert centers.shape[0] == clusters_list.size, \
                    "ERROR: split() centers and clusters_list size are different"

    return centers, clusters_list, k_


def _compute_avg_distance(img_flat: np.ndarray, img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Compute average intra-cluster distance.

    Parameters
    ----------
    img_flat : np.ndarray
        Flattened image pixels.
    img_class_flat : np.ndarray
        Flattened image class labels.
    centers : np.ndarray
        Cluster centers.
    clusters_list : np.ndarray
        Cluster label array.

    Returns
    -------
    Tuple[np.ndarray, int]
        Array of average distances and cluster count.
    """
    k_ = centers.shape[0]
    avg_dists_to_clusters = np.zeros(k_)

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]

        cluster_points = img_flat[indices]
        avg_dists_to_clusters[cluster] = np.mean(np.linalg.norm(cluster_points - centers[cluster], axis=1))

    return avg_dists_to_clusters, k_


def _compute_overall_distance(img_class_flat: np.ndarray, avg_dists_to_clusters: np.ndarray, clusters_list: np.ndarray) -> Tuple[float, int]:
    """
    Calculate overall weighted distance from cluster centers.

    Parameters
    ----------
    img_class_flat : np.ndarray
        Flattened image class labels.
    avg_dists_to_clusters : np.ndarray
        Average distances per cluster.
    clusters_list : np.ndarray
        Cluster label array.

    Returns
    -------
    Tuple[float, int]
        Overall distance and number of clusters.
    """
    k_ = avg_dists_to_clusters.size
    total_count = 0
    total_dist = 0

    for cluster in range(k_):
        nbr_points = len(np.where(img_class_flat == clusters_list[cluster])[0])
        total_dist += avg_dists_to_clusters[cluster] * nbr_points
        total_count += nbr_points

    d = total_dist / total_count

    return d, k_


def _merge_clusters(img_class_flat: np.ndarray, centers: np.ndarray, clusters_list: np.ndarray, p: int, theta_c: int, k_: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """
    Merge nearby clusters if their distance is below a threshold.

    Parameters
    ----------
    img_class_flat : np.ndarray
        Flattened image class labels.
    centers : np.ndarray
        Cluster centers.
    clusters_list : np.ndarray
        Cluster label array.
    p : int
        Max number of merge candidates.
    theta_c : int
        Distance threshold for merging.
    k_ : int
        Current number of clusters.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, int]
        Updated centers, cluster list, and number of clusters.
    """
    pair_dists = _compute_pairwise_distances(centers)

    first_p_elements = pair_dists[:p]
    below_threshold = [(c1, c2) for d, (c1, c2) in first_p_elements if d < theta_c]

    if below_threshold:
        k_ = centers.size
        count_per_cluster = np.zeros(k_)
        to_add = np.array([])  # new clusters to add
        to_delete = np.array([])  # clusters to delete

        for cluster in range(k_):
            result = np.where(img_class_flat == clusters_list[cluster])
            indices = result[0]
            count_per_cluster[cluster] = indices.size

        for c1, c2 in below_threshold:
            c1_count = float(count_per_cluster[c1]) + 1
            c2_count = float(count_per_cluster[c2])
            factor = 1.0 / (c1_count + c2_count)
            weight_c1 = c1_count * centers[c1]
            weight_c2 = c2_count * centers[c2]

            value = round(factor * (weight_c1 + weight_c2))

            to_add = np.append(to_add, value)
            to_delete = np.append(to_delete, [c1, c2])

        # delete old clusters and their indices from the available array
        centers = np.delete(centers, to_delete)
        clusters_list = np.delete(clusters_list, to_delete)

        # generate new indices for the new clusters
        # starting from the max index 'to_add.size' times
        start = int(clusters_list.max())
        end = to_add.size + start

        centers = np.append(centers, to_add)
        clusters_list = np.append(clusters_list, range(start, end))

        centers, clusters_list = _sort_arrays_by_first(centers, clusters_list)

    return centers, clusters_list, k_


def _compute_pairwise_distances(centers: np.ndarray) -> list:
    """
    Compute all pairwise distances between cluster centers.

    Parameters
    ----------
    centers : np.ndarray
        Cluster centers.

    Returns
    -------
    list
        Sorted list of (distance, (cluster1, cluster2)) tuples.
    """
    pair_dists = []

    for i in range(centers.shape[0]):
        for j in range(i):
            # Compute the Euclidean distance using np.linalg.norm
            d = np.linalg.norm(centers[i] - centers[j])
            pair_dists.append((d, (i, j)))

    # Sort by the computed distance (the first element in the tuple)
    return sorted(pair_dists, key=lambda x: x[0])


def isodata(dc, k: int = 10, it: int = 10, p: int = 2, theta_m: int = 10,
            theta_s: float = 0.1, theta_c: int = 2, theta_o: float = 0.05,
            k_: Optional[int] = None) -> np.ndarray:
    """
    Classify hyperspectral image data using the ISODATA clustering algorithm.

    Performs iterative clustering on a hyperspectral DataCube, adapting the number of clusters
    by splitting and merging based on data distribution, until convergence or iteration limit is reached.

    Parameters
    ----------
    dc : DataCube
        DataCube object containing the hyperspectral image with shape (v, x, y).
    k : int, optional
        Initial number of clusters to begin clustering. Default is 10.
    it : int, optional
        Maximum number of iterations. Default is 10.
    p : int, optional
        Maximum number of cluster pairs allowed to merge. Default is 2.
    theta_m : int, optional
        Minimum number of pixels required per cluster. Default is 10.
    theta_s : float, optional
        Threshold for standard deviation to trigger cluster splitting. Default is 0.1.
    theta_c : int, optional
        Distance threshold for merging clusters. Default is 2.
    theta_o : float, optional
        Threshold for minimum change in cluster centers to stop iteration. Default is 0.05.
    k_ : int, optional
        Alternative number of clusters to override initial `k`. Default is None.

    Returns
    -------
    np.ndarray
        2D array (x, y) with cluster labels assigned to each pixel.

    Raises
    ------
    ValueError
        If intermediate clustering steps produce inconsistent dimensions or invalid data.

    Notes
    -----
    This implementation adapts clustering during iterations by merging or splitting clusters,
    based on the intra-cluster statistics and spatial constraints. The algorithm stops early
    if cluster centers converge according to `theta_o`.

    Examples
    --------
    >>> labels = isodata(dc, k=5, it=15)
    """
    img = np.transpose(dc.cube, (1, 2, 0))  # Rearrange cube dimensions to (H, W, Channels)

    if k_ is None:
        k_ = k

    x, y, _ = img.shape
    img_flat = img.reshape(-1, img.shape[2])  # Flatten spatial dimensions
    clusters_list = np.arange(k_)
    centers = _initial_clusters(img_flat, k_, "linspace")

    for i in range(it):
        last_centers = centers.copy()

        # Assign samples to the nearest cluster center
        img_class_flat, _ = vq(img_flat, centers)

        # Discard underpopulated clusters
        centers, clusters_list, k_ = _discard_clusters(img_class_flat, centers, clusters_list, theta_m)

        # Update cluster centers
        centers, clusters_list, k_ = _update_clusters(img_flat, img_class_flat, centers, clusters_list)

        # Handle excessive or insufficient clusters
        if k_ <= (k / 2.0):  # Too few clusters -> Split clusters
            centers, clusters_list, k_ = _split_clusters(img_flat, img_class_flat, centers, clusters_list, theta_s, theta_m)
        elif k_ > (k * 2.0):  # Too many clusters -> Merge clusters
            centers, clusters_list, k_ = _merge_clusters(img_class_flat, centers, clusters_list, p, theta_c, k_)

        # Terminate early if cluster changes are minimal
        if _quit_low_change_in_clusters(centers, last_centers, theta_o):
            break

    return img_class_flat.reshape(x, y)


def _generate_gaussian_kernel(size=3, sigma=1.0):
    """
    Generate a 2D Gaussian kernel for image smoothing.

    Creates a square kernel using the Gaussian function, which can be used
    for spatial smoothing via convolution operations.

    Parameters
    ----------
    size : int, optional
        Size of the kernel (must be odd). Default is 3.
    sigma : float, optional
        Standard deviation of the Gaussian distribution. Default is 1.0.

    Returns
    -------
    np.ndarray
        2D array representing the normalized Gaussian kernel.

    Notes
    -----
    The kernel is normalized so that the sum of all elements equals 1. The
    kernel is computed as the outer product of two 1D Gaussian vectors.

    Examples
    --------
    >>> kernel = _generate_gaussian_kernel(size=5, sigma=1.5)
    >>> print(kernel.shape)
    (5, 5)
    """

    ax = np.linspace(-(size // 2), size // 2, size)
    gauss = np.exp(-0.5 * (ax / sigma) ** 2)
    kernel = np.outer(gauss, gauss)
    return kernel / kernel.sum()


def _optimal_clusters(pixels, max_clusters=5, threshold=0.1) -> int:
    """
    Estimate the optimal number of KMeans clusters using centroid distance threshold.

    Iteratively fits KMeans with increasing cluster counts and evaluates the minimum
    distance between centroids. Clustering stops when the closest centroids are within
    the specified distance threshold, indicating excessive overlap.

    Parameters
    ----------
    pixels : np.ndarray
        2D array of shape (n_samples, n_features), representing the flattened image spectra.
    max_clusters : int, optional
        Maximum number of clusters to evaluate. Default is 5.
    threshold : float, optional
        Minimum acceptable distance between any pair of cluster centroids. Default is 0.1.

    Returns
    -------
    int
        Optimal number of clusters where centroid spacing satisfies the distance threshold.

    Raises
    ------
    ValueError
        If input `pixels` is not a 2D array or has insufficient samples.

    Notes
    -----
    Uses pairwise Euclidean distances to determine centroid separation.
    Cluster count starts from 2 up to `max_clusters`.

    Examples
    --------
    >>> pixels = dc.cube.reshape(dc.cube.shape[0], -1).T
    >>> k = _optimal_clusters(pixels, max_clusters=6, threshold=0.2)
    >>> print(k)
    4
    """
    best_k = 2
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_
        dists = pairwise_distances(centers)
        np.fill_diagonal(dists, np.inf)  # Ignore self-distances
        closest_dist = np.min(dists)
        if closest_dist > threshold:
            best_k = k
        else:
            break
    return best_k


def smooth_kmeans(dc, n_clusters=5, threshold=.1, mrf_iterations=5, kernel_size=12, sigma=1.0):
    """
    Segment a hyperspectral DataCube using KMeans clustering with MRF-based spatial smoothing.

    Performs initial clustering on spectral data using KMeans, followed by iterative Markov Random
    Field (MRF)-based smoothing using Gaussian kernel convolution to enforce spatial consistency.

    Parameters
    ----------
    dc : DataCube
        Hyperspectral data cube with shape (v, x, y), where `v` is spectral resolution.
    n_clusters : int, optional
        Maximum number of clusters for initial KMeans clustering. Default is 5.
    threshold : float, optional
        Minimum allowable distance between KMeans centroids to stop increasing cluster count. Default is 0.1.
    mrf_iterations : int, optional
        Number of spatial smoothing iterations using MRF regularization. Default is 5.
    kernel_size : int, optional
        Size of the Gaussian kernel used for smoothing. Must be an odd integer. Default is 12.
    sigma : float, optional
        Standard deviation of the Gaussian kernel. Default is 1.0.

    Returns
    -------
    np.ndarray
        2D array (x, y) of cluster labels after smoothing.

    Raises
    ------
    ValueError
        If input DataCube is malformed or smoothing parameters are invalid.

    Notes
    -----
    The function uses `optimal_clusters` to determine a suitable number of clusters
    before applying KMeans. MRF smoothing is implemented by convolving binary masks
    of each cluster with a Gaussian kernel and reassigning pixels based on weighted responses.

    Examples
    --------
    >>> labels = smooth_kmeans(dc, n_clusters=6, mrf_iterations=3)
    >>> plt.imshow(labels, cmap='viridis')
    >>> plt.show()
    """

    v, x, y = dc.shape

    # Reshape cube for clustering
    pixels = dc.cube.reshape(v, -1).T

    # Determine optimal number of clusters
    optimal_k = _optimal_clusters(pixels, max_clusters=n_clusters, threshold=threshold)
    _kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    labels = _kmeans.fit_predict(pixels)
    labels = labels.reshape(x, y)

    # Generate dynamic Gaussian kernel
    kernel = _generate_gaussian_kernel(size=kernel_size, sigma=sigma)

    # Apply Markov Random Field-based spatial regularization
    for _ in range(mrf_iterations):
        smoothed_labels = np.zeros_like(labels, dtype=np.float64)
        for cluster in range(optimal_k):
            binary_mask = (labels == cluster).astype(np.float64)
            smoothed_mask = convolve2d(binary_mask, kernel, mode='same', boundary='symm')
            smoothed_labels += cluster * smoothed_mask
        labels = np.round(smoothed_labels).astype(np.int32)

    return labels


def pca(dc, n_components=25):
    """
    Perform principal component analysis to reduce the spectral dimensionality of a DataCube.

    This function reshapes the DataCube’s underlying array from shape (v, x, y) to (x*y, v),
    applies PCA to reduce the number of spectral bands to `n_components`, then reshapes
    the result back to (n_components, x, y). It also updates the DataCube’s wavelengths
    to a simple integer index for each new component.

    Parameters
    ----------
    dc : DataCube
        The DataCube instance whose `cube` attribute (a numpy array of shape (v, x, y))
        will be reduced in its spectral dimension.
    n_components : int, optional
        The number of principal components to retain. Defaults to 25.

    Returns
    -------
    DataCube
        The same DataCube instance, with its `cube` attribute replaced by the reduced
        cube of shape (n_components, x, y) and its `wavelengths` attribute set to
        integer indices from 0 to n_components-1.

    Raises
    ------
    ValueError
        If `n_components` is greater than the original number of spectral bands (v).

    Notes
    -----
    - Uses `sklearn.decomposition.PCA` under the hood.
    - The new wavelengths are not actual physical wavelengths but simple indices.
    - The transformation is done in-place on the provided DataCube.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("hyperspectral_data.cube")
    >>> dc = pca(dc, n_components=10)
    >>> print(dc.cube.shape)
    (10, 512, 512)
    """
    v, x, y = dc.cube.shape

    cube = dc.cube

    # Reshape to (n_pixels, v)
    data = cube.reshape(v, -1).T  # (x*y, v)

    # PCA reduction
    pca_model = PCA(n_components=n_components)
    reduced = pca_model.fit_transform(data)  # (x*y, n_components)

    # Reshape back to (n_components, x, y)
    reduced_cube = reduced.T.reshape(n_components, x, y)

    wave = np.arange(n_components, dtype=int)

    dc.set_cube(reduced_cube)
    dc.set_wavelengths(wave)
    return dc


def spectral_spatial_kmeans(dc, n_clusters: int, spatial_radius: int) -> np.ndarray:
    """
    Spectral–spatial K-Means clustering for hyperspectral images.

    Applies K-Means to pixel spectra augmented by the mean spectrum of their local neighborhood.

    Parameters
    ----------
    dc : DataCube
        Hyperspectral data cube with shape (v, x, y), where v is number of bands.
    n_clusters : int
        Number of clusters to form.
    spatial_radius : int
        Radius (in pixels) of the square neighborhood for local averaging.

    Returns
    -------
    labels : np.ndarray of shape (x, y)
        Integer cluster label for each pixel.

    Raises
    ------
    ValueError
        If `spatial_radius < 0` or `n_clusters <= 0`.

    Notes
    -----
    - Uses a uniform filter to compute the local mean spectrum for each pixel.
    - Flattens the augmented spectral features and applies scikit-learn’s KMeans.

    Examples
    --------
    >>> labels = spectral_spatial_kmeans(dc, n_clusters=5, spatial_radius=1)
    """
    if spatial_radius < 0 or n_clusters <= 0:
        raise ValueError("spatial_radius must be ≥0 and n_clusters >0")

    # Compute local-mean cube
    v, x, y = dc.cube.shape
    local_cube = np.empty_like(dc.cube)
    for band in range(v):
        local_cube[band] = uniform_filter(dc.cube[band], size=2 * spatial_radius + 1, mode='reflect')

    # Stack spectral + spatial-mean features
    features = np.vstack([
        dc.cube.reshape(v, -1),
        local_cube.reshape(v, -1)
    ]).T  # shape (x*y, 2v)

    # Run KMeans
    km = KMeans(n_clusters=n_clusters, random_state=0)
    flat_labels = km.fit_predict(features)

    return flat_labels.reshape(x, y)


def spatial_agglomerative_clustering(dc, n_clusters: int) -> np.ndarray:
    """
    Agglomerative clustering with a 4-connected grid graph enforcing spatial contiguity.

    Flattens the spectral vectors and uses `grid_to_graph` for pixel connectivity,
    so only spatial neighbors can merge.

    Parameters
    ----------
    dc : DataCube
        Hyperspectral data cube (v, x, y).
    n_clusters : int
        Desired number of clusters.

    Returns
    -------
    labels : np.ndarray of shape (x, y)
        Connected clusters that respect spatial adjacency.

    Notes
    -----
    - Uses `sklearn.feature_extraction.image.grid_to_graph` to build a sparse connectivity matrix over the x×y grid.
    - May be more memory-intensive for large images.

    Examples
    --------
    >>> labels = spatial_agglomerative_clustering(dc, n_clusters=8)
    """
    v, x, y = dc.cube.shape
    # Build connectivity graph on the 2D grid
    connectivity = grid_to_graph(n_x=x, n_y=y)

    # Flatten spectral data
    data = dc.cube.reshape(v, -1).T  # shape (x*y, v)

    # Agglomerative clustering with spatial connectivity
    agg = AgglomerativeClustering(n_clusters=n_clusters,
                                  connectivity=connectivity,
                                  linkage='ward')
    flat_labels = agg.fit_predict(data)

    return flat_labels.reshape(x, y)


def smooth_cluster(img, sigma=1.0, n_iter=1):
    """
    Smooth a cluster label image to remove mislabelled pixels.

    Apply a Gaussian filter to the input cluster label image to reduce spurious
    mislabelled pixels by smoothing label intensities, then round back to the
    nearest integer labels.

    Parameters
    ----------
    img : numpy.ndarray
        Integer label image of shape (H, W) or (H, W, ...).
    sigma : float, optional
        Standard deviation for Gaussian kernel. Default is 1.0.
    n_iter: int, optional
        Number of iterations to apply the Gaussian filter. Default is 1.

    Returns
    -------
    numpy.ndarray
        Smoothed label image with same shape and dtype as input.

    Raises
    ------
    TypeError
        If img is not a numpy.ndarray.
    ValueError
        If img is empty.

    Notes
    -----
    Internally, the image labels are converted to float, smoothed, then rounded
    back to integer labels. This may remove small isolated noisy pixels.

    Examples
    --------
    >>> import numpy as np
    >>> img = np.array([[1,1,2],[1,2,2],[2,2,2]])
    >>> smooth_cluster(img, sigma=0.5)
    array([[1,1,2],
           [1,2,2],
           [2,2,2]])
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("img must be a numpy.ndarray")
    if img.size == 0:
        raise ValueError("img must not be empty")

    result = img.copy()
    for _ in range(n_iter):
        img_float = result.astype(np.float64)
        smoothed = gaussian_filter(img_float, sigma=sigma)
        result = np.rint(smoothed).astype(img.dtype)
        
    return result


def kmeans(dc, n_clusters=5, n_init=10):
    """
    Perform KMeans clustering on a hyperspectral DataCube without spatial smoothing.

    This function reshapes the spectral data into pixel vectors and applies KMeans to
    segment the data into the specified number of clusters.

    Parameters
    ----------
    dc : DataCube
        Hyperspectral data cube with shape (v, x, y), where `v` is the spectral resolution.
    n_clusters : int
        Number of clusters to form. Default is 5.
    n_init : int
        Number of time the k-means algorithm will be run with different centroid seeds.
        Default is 10.

    Returns
    -------
    np.ndarray
        2D array of shape (x, y) containing cluster labels for each pixel.

    Raises
    ------
    ValueError
        If the input DataCube is malformed or `n_clusters` or `n_init` are invalid.

    Notes
    -----
    This function does not perform any spatial regularization or smoothing.
    """
    # Validate inputs
    if n_clusters < 1 or n_init < 1:
        raise ValueError("`n_clusters` and `n_init` must be positive integers.")

    # Reshape cube for clustering
    v, x, y = dc.cube.shape
    pixels = dc.cube.reshape(v, -1).T

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=n_init)
    labels_flat = kmeans.fit_predict(pixels)

    # Reshape back to image dimensions
    return labels_flat.reshape(x, y)
