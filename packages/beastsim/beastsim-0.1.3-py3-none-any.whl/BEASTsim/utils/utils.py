import os
from tqdm import tqdm
from anndata import AnnData
from typing import List, Optional, Tuple, Union, Dict
from numpy import ndarray
from pandas import DataFrame, Series

from BEASTsim.beast_data import BEAST_Data

def _save_data(data: Dict[str, Union[DataFrame, Series]], filename: str):
    """Save the normalized benchmark results to a file."""
    from pickle import dump
    with open(filename, "wb") as f:
        dump(data, f)

def _load_data(filename: str) -> Dict[str, Union[DataFrame, Series]]:
    """Load the normalized benchmark results from a file."""
    from pickle import load
    with open(filename, "rb") as f:
        return load(f)

def _normalize_benchmark_results(data: Dict[str, Union[DataFrame, Series]], min=None, max=None) -> Dict[str, Union[DataFrame, Series]]:
    from pandas import concat, Series
    # Convert all Series to DataFrames for consistent processing
    data = {key: (df.to_frame() if isinstance(df, Series) else df) for key, df in data.items()}

    # Concatenate all data for row-wise min-max normalization
    combined_data = concat(data.values(), axis=1)

    row_min = combined_data.min(axis=1, skipna=True) if min is None else Series(min, index=combined_data.index)
    row_max = combined_data.max(axis=1, skipna=True) if max is None else Series(max, index=combined_data.index)

    row_range = row_max - row_min
    row_range[row_range == 0] = 1  # Prevent division by zero for constant rows

    # Normalize data
    normalized_data = {
        key: (df.iloc[:, 0] - row_min) / row_range
        for key, df in data.items()
    }

    # Fill NaN values with 0
    normalized_data = {key: df.fillna(0) for key, df in normalized_data.items()}



    # Filter out rows where all values are identical across benchmarks
    filtered_indices = (combined_data.nunique(axis=1) > 1)
    normalized_data = {key: df[filtered_indices] for key, df in normalized_data.items()}

    # Convert back to Series if original input was a Series
    normalized_data = {
        key: df.iloc[:, 0] if isinstance(data[key], Series) else df
        for key, df in normalized_data.items()
    }

    return normalized_data

def _merge_results(data: List[Dict[str, Series]], score_title: str) -> Dict[str, Series]:
    from collections import defaultdict
    from pandas import concat

    merged_results = defaultdict(lambda: Series(dtype="float64"))  # Initialize empty Series

    for benchmark_result in data:  # Each benchmark's result is a dict
        for sim_name, scores in benchmark_result.items():
            merged_results[sim_name] = concat([merged_results[sim_name], scores])

    merged_results = {k: v.rename(score_title) for k, v in merged_results.items()}
    return merged_results

def _clean(attributes: List[str], fields: List[str], data):
    for attr in attributes:
        for field in fields:
            if field in getattr(data.data, attr, {}):
                del getattr(data.data, attr)[field]

def _use_ground_truth(use_ground_truth: str, real: BEAST_Data, sim_data: List[BEAST_Data]) -> Optional[List[BEAST_Data]]:
    from copy import deepcopy
    def _create_copy(name_suffix: str) -> BEAST_Data:
        copied_data = deepcopy(real)
        copied_data.name = f"{name_suffix}-{real.name}"
        copied_data.is_simulated = True
        if name_suffix == "Variance":
            if "centroids" in copied_data.data.uns:
                _clean(attributes=["obs"], fields=["cell_type"], data=copied_data)
                _clean(attributes=["uns"], fields=["centroids"], data=copied_data)
                _clean(attributes=["obsm"], fields=["cell_type_distribution"], data=copied_data)
            elif "voxelized_subdata" in copied_data.data.uns:
                _clean(attributes=["uns"], fields=["voxelized_subdata"], data=copied_data)
            _clean(attributes=["var"], fields=["q_val", "p_val"], data=copied_data)
        return copied_data

    if not real.copied:
        if use_ground_truth.lower() == 'real':
            sim_data.append(_create_copy(name_suffix="GT"))
        elif use_ground_truth.lower() == 'variance':
            sim_data.append(_create_copy(name_suffix="Variance"))
        elif use_ground_truth.lower() == 'both':
            sim_data.append(_create_copy(name_suffix="GT"))
            sim_data.append(_create_copy(name_suffix="Variance"))
        else:
            return None
    else:
        return None
    real.copied = True
    return sim_data

def _replace_nan_with_zero(obj):
    import math
    if isinstance(obj, list):
        return [_replace_nan_with_zero(x) for x in obj]  # Recursively process lists
    elif isinstance(obj, float) and math.isnan(obj):
        return 0  # Replace NaN with 0
    else:
        return obj  # Keep everything else unchanged

def _format_name_html(name: str, max_length: int = 15) -> str:
    """
    Formats a string by replacing underscores with spaces, preserving existing capitalization,
    capitalizing words only if they start with a lowercase letter, and inserting <br>
    when the name exceeds a certain length.

    Args:
        name (str): The input string to format.
        max_length (int): The maximum length before inserting a <br>.

    Returns:
        str: The formatted string with appropriate capitalization and <br> for long names.
    """
    import textwrap

    # Replace underscores with spaces
    formatted_name = " ".join(
        word.capitalize() if word and word[0].islower() else word
        for word in name.replace("_", " ").split()
    )

    # Insert <br> if the string is too long
    return "<br>".join(textwrap.wrap(formatted_name, max_length))

def _cluster_cell_distributions(cell_distributions: DataFrame, k_start: int = 2, k_end: int = 10,
                                weights: dict = {"silhouette": 0.5, "davies": 0.5}, seed: int = 42) -> \
tuple[List[tuple[int, float]], List[List[float]]]:
    """
    Perform KMeans clustering on cell type distributions and output cluster centroids.
    The optimal number of clusters is selected using silhouette score and Davies Bouldin index.

    Args:
        cell_distributions (DataFrame): Pandas DataFrame where rows are cells and columns are cell type distributions.
        k_start (int): The starting number of clusters for KMeans.
        k_end (int): The ending number of clusters for KMeans.
        weights (dict): Weights for the different clustering evaluation metrics (silhouette, davies).
        seed (int): Random seed for reproducibility.

    Returns:
        tuple: A tuple containing the ranking of the number of clusters based on the weighted sum and
               the centroids of the best KMeans model.
    """
    from sklearn.cluster import KMeans
    from numpy import log
    def _run_kmeans(k_start: int, k_end: int, data: ndarray, random_state: int = 42) -> List[KMeans]:
        """
        Run KMeans clustering for a range of cluster numbers and return the trained models.

        Args:
            k_start (int): The starting number of clusters (inclusive).
            k_end (int): The ending number of clusters (inclusive).
            data (ndarray): The dataset to be clustered.
            random_state (int, optional): The random seed for reproducibility. Default is 42.

        Returns:
            list: A list of trained KMeans models, one for each number of clusters in the specified range.
        """
        models = []
        for k in range(k_start, k_end + 1):
            kmeans = KMeans(n_clusters=k, init="k-means++", random_state=random_state)
            kmeans.fit(data)
            models.append(kmeans)
        return models

    def _calc_silhouette(k_start: int, k_end: int, models: List[KMeans], data: ndarray) -> List[tuple[int, float]]:
        """
        Calculate the silhouette scores for a range of clusters and return them sorted from best to worst.

        Args:
            k_start (int): The starting number of clusters (inclusive).
            k_end (int): The ending number of clusters (inclusive).
            models (list): A list of trained KMeans models corresponding to the cluster range.
            data (ndarray): The dataset used for clustering.

        Returns:
            list: A list of tuples where each tuple contains:
                  - The number of clusters (k).
                  - The silhouette score for that clustering.
                  The list is sorted in descending order by silhouette score.
        """
        from sklearn.metrics import silhouette_score
        s_scores = []
        ks = list(range(k_start, k_end + 1))
        for k, model in list(zip(ks, models)):
            s_score = silhouette_score(data, model.labels_)
            s_scores.append((k, s_score))
        s_scores = sorted(s_scores, key=lambda x: x[1], reverse=True)
        return s_scores

    def _calc_davies_bouldin(k_start: int, k_end: int, models: List[KMeans], data: ndarray) -> List[
        tuple[int, float]]:
        """
        Calculate the Davies-Bouldin Index (DBI) for a range of clusters and return them sorted from best to worst.

        Args:
            k_start (int): The starting number of clusters (inclusive).
            k_end (int): The ending number of clusters (inclusive).
            models (list): A list of trained KMeans models corresponding to the cluster range.
            data (ndarray): The dataset used for clustering.

        Returns:
            list: A list of tuples where each tuple contains:
                  - The number of clusters (k).
                  - The Davies-Bouldin Index for that clustering.
                  The list is sorted in ascending order by DBI score.
        """
        from sklearn.metrics import pairwise_distances
        from numpy import array, mean, inf, linalg

        dbi_scores = []
        ks = list(range(k_start, k_end + 1))

        for k, model in zip(ks, models):
            labels = model.labels_
            centroids = array([data[labels == i].mean(axis=0) for i in range(k)])

            scatter = []
            for i in range(k):
                cluster_points = data[labels == i]
                dist = pairwise_distances(cluster_points, [centroids[i]])
                scatter.append(mean(dist))

            db_index = 0.0
            for i in range(k):
                max_ratio = -inf
                for j in range(k):
                    if i != j:
                        inter_cluster_dist = linalg.norm(centroids[i] - centroids[j])
                        ratio = (scatter[i] + scatter[j]) / inter_cluster_dist
                        max_ratio = max(max_ratio, ratio)
                db_index += max_ratio

            dbi_scores.append((k, db_index / k))

        dbi_scores = sorted(dbi_scores, key=lambda x: x[1])

        return dbi_scores

    if not isinstance(cell_distributions, ndarray):
        data = cell_distributions.to_numpy()
    else:
        data = cell_distributions

    models = _run_kmeans(k_start=k_start, k_end=k_end, data=data, random_state=seed)

    # Silhouette
    s_scores = _calc_silhouette(k_start=k_start, k_end=k_end, models=models, data=data)
    s_scores = [(k, (score - min(s_scores, key=lambda x: x[1])[1]) / (
            max(s_scores, key=lambda x: x[1])[1] - min(s_scores, key=lambda x: x[1])[1])) for k, score in s_scores]

    # Davies Bouldin
    dbi_scores = _calc_davies_bouldin(k_start=k_start, k_end=k_end, models=models, data=data)
    dbi_scores = [(k, 1 - (score - min(dbi_scores, key=lambda x: x[1])[1]) / (
            max(dbi_scores, key=lambda x: x[1])[1] - min(dbi_scores, key=lambda x: x[1])[1])) for k, score in
                  dbi_scores]

    weights = {k: v / sum(weights.values()) for k, v in weights.items()} # Normalize the weights

    weighted_sums = []
    for k in range(k_start, k_end + 1):
        sil_score = dict(s_scores).get(k, 0)
        davies_score = dict(dbi_scores).get(k, 0)

        weighted_sum = (weights["silhouette"] * sil_score) + \
                       (weights["davies"] * davies_score)

        weighted_sums.append((k, weighted_sum))

    # Ranking (higher is better)
    ranking = sorted(weighted_sums, key=lambda x: x[1], reverse=True)

    best_k = ranking[0][0]
    best_kmeans = models[best_k - k_start]
    centroids = best_kmeans.cluster_centers_

    return ranking, centroids

def _find_project_root(start_path, marker="BEASTsim"):
    """
    Traverse upwards to find the project root directory.
    """
    current_dir = start_path
    while current_dir != os.path.dirname(current_dir):
        if marker in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def _trunc(values, decs=0):
    from numpy import trunc
    return trunc(values * 10 ** decs) / (10 ** decs)

def _num_of_types(adata):
    return len(adata.obs['cell_type'].astype('category').cat.categories)

def _init_dir(path):
    os.makedirs(path, exist_ok=True)

def _cpm(x: ndarray, log: bool = False) -> ndarray:
    """
    Transforms the exact count matrix into the Counts Per Million (CPM) matrix, which may be used according to
    preferance in several benchmarks instead of the raw data

    Args:
        x (ndarray): Input array of counts where rows represent genes and columns represent samples.

        log (bool): If True, applies a log2 transformation to the CPM values after calculation. Default is False.

    Returns:
        ndarray: An array of CPM values. If log is True, returns log2-transformed CPM values.
    """
    from numpy import log2, array
    if log:
        r = log2(1e+6 * x / x.sum(axis=0) + 1)
    else:
        r = 1e+6 * x / x.sum(axis=0)
    return array(r)


def _build_statistical_dataframe(simulated_data: list, real_data=None, names: list[str] = []) -> DataFrame:
    from numpy import isscalar
    dict = {}
    if real_data is not None:
        dict = {"Real": real_data}
    for i, method_name in enumerate(names):
        if isscalar(simulated_data[i]):
            simulated_data[i] = [simulated_data[i]]  # Wrap scalar in list
        elif isinstance(simulated_data[i], (list, ndarray)):
            # Ensure it's already iterable, nothing to change
            pass
        else:
            # Handle other cases if necessary
            raise ValueError(f"Unexpected data type for simulated_data[{i}]: {type(simulated_data[i])}")
        dict[method_name] = simulated_data[i]
    df = DataFrame(dict)
    return df

def _init_colors(method_names):
    method_colors = {"Real": "blue"}
    colors = ["green", "red", "orange", "pink", "yellow"]
    for i, method_name in enumerate(method_names):
        method_colors[method_name] = colors[i]
    return method_colors

def _find_closest_points_distance(adata, x_col="X", y_col="Y"):
    from numpy import inf, linalg
    # Extract coordinates
    coords = adata.obs[[x_col, y_col]].to_numpy()

    # Compute pairwise distances
    num_points = coords.shape[0]
    min_distance = inf

    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = linalg.norm(coords[i] - coords[j])
            if dist < min_distance:
                min_distance = dist

    return min_distance

def _calc_cell_type_neighborhoods(datasets, ct):
    from collections import namedtuple
    from numpy import sort, unique, append, argsort, diff, max, zeros, where, sum

    nh_list = []
    cell_types = []
    cell_types_n = []
    for i, ST in enumerate(datasets):
        x = ST.obs.X.values
        y = ST.obs.Y.values
        ## TODO: GET CELLTYPES USING CELL2LOCATION

        if i == 0:
            cell_types = sort(unique(ct[i]))
            cell_types_n = append(cell_types, "empty")

        sorted_indices = argsort(x)

        sorted_x = x[sorted_indices]
        sorted_y = y[sorted_indices]
        sorted_ct = ct[sorted_indices]

        min_x = min(sorted_x)
        min_y = min(sorted_y)

        sorted_x = sorted_x - min_x
        sorted_y = sorted_y - min_y

        unqiue_x = unique(sorted_x)
        dist_x = max(diff(unqiue_x))

        unqiue_y = unique(sorted_y)
        dist_y = max(diff(unqiue_y)) * 2

        dict = {}
        PointSetWithInteger = namedtuple(
            "PointSetWithInteger", ["neighbors", "cell_type"]
        )
        for idx, (x1, y1, ct) in tqdm(
            enumerate(zip(sorted_x, sorted_y, sorted_ct))
        ):
            points = []
            for jdx, (x2, y2) in enumerate(zip(sorted_x, sorted_y)):
                if x1 == x2 and y1 == y2:
                    continue
                if abs(x1 - x2) <= dist_x and abs(y1 - y2) <= dist_y:
                    points.append((x2, y2))
            dict[(x1, y1)] = PointSetWithInteger(set(points), ct)

        n_ct = len(unique(sorted_ct))
        ct_dist = zeros(n_ct)
        for key, val in dict.items():
            cell_type = val.cell_type
            idx = where(cell_types_n == cell_type)[0][0]
            ct_dist[idx] += 1
        ct_dist /= sum(ct_dist)

        nh_dist = zeros((n_ct, n_ct + 1))
        for key, val in dict.items():
            cell_type = val.cell_type
            idx = where(cell_types_n == cell_type)[0][0]
            neighbors = val.neighbors
            for neighbor in neighbors:
                n_cell_type = dict[neighbor].cell_type
                jdx = where(cell_types_n == n_cell_type)[0][0]
                nh_dist[idx][jdx] += 1
            nh_dist[idx][n_ct] += 6 - len(neighbors)

        for i in range(len(nh_dist)):
            nh_dist[i] /= sum(nh_dist[i])

        nh_list.append(nh_dist)
    return nh_list, cell_types, cell_types_n


def _calculate_ks(gt, pred):
    from scipy.stats import ks_2samp

    statistic, pvalue = ks_2samp(gt.flatten(), pred.flatten())
    return statistic, pvalue


def _init_spot_size(dataset):
    import math
    min_dist = math.inf
    for data in dataset:
        dist = _find_closest_points_distance(data)
        if dist < min_dist:
            min_dist = dist
    spot_size = min_dist * 0.75
    return spot_size


def _cluster_cells_into_pseudospots(adata, n_spots=500, cell_type_keys=['cell_type', 'cell_type_distribution']):
    """
    Clusters single cells into pseudo-spots and attaches a spot-level AnnData object at .uns['voxelized_subdata'].

    Mimics Visium-style spatial transcriptomics by k-means clustering the 2-D
    cell coordinates, then summing gene counts within each cluster (“pseudo-spot”).
    Centroid coordinates, per-spot cell counts, and optional cell-type
    compositions are calculated and stored.

    The resulting spot-level dataset is placed in
    `adata.uns['voxelized_subdata']`, while the original AnnData gains
    `obs['pseudo_spot']` labels and an updated `.obsm['spatial']` matrix.

    Parameters
    ----------
    adata : AnnData
        Single-cell expression object containing per-cell X/Y coordinates
        in `obs['X']` and `obs['Y']`.
    n_spots : int, default 500
        Number of k-means clusters (i.e. pseudo-spots) to generate.
    cell_type_keys : list[str], default ['cell_type', 'cell_type_distribution']
        Two keys to look for cell-type information:
        1. `obs[cell_type_keys[0]]` – categorical cell-type labels.
        2. `obsm[cell_type_keys[1]]` – per-cell probability/fraction vectors.
        The second key is preferred; if absent, the categorical labels are
        one-hot–encoded and aggregated to spot-level proportions.

    Returns
    -------
    AnnData
        The same `adata` object, augmented with:
        * `obs['pseudo_spot']` : cluster label for each cell.
        * `obsm['spatial']`    : n_cells × 2 array of X/Y coordinates
                                 (overwritten/created).
        * `uns['voxelized_subdata']` : new AnnData whose
          ├─ obs rows represent pseudo-spots
          ├─ X/Y stored in `.obsm['spatial']` and copied to `obs['X']`,`obs['Y']`
          ├─ `.X` (or `.layers['counts']`) holds summed gene counts
          ├─ `obs['cell_counts']` gives contributing cell numbers
          └─ `.obsm['cell_type_distribution']` (optional) stores per-spot
             cell-type fractions.

    Notes
    -----
    * K-means is initialised with `random_state=42` for reproducibility.
    * If `x_bin`/`y_bin` columns exist, their means (instead of raw X/Y) are
      used for spot centroids, enabling compatibility with pre-binned data.
    * Each row of the spot-level cell-type distribution sums to 1; NaNs
      (possible only for empty spots) are replaced with 0.
    """
    from pandas import get_dummies
    from sklearn.cluster import KMeans
    from numpy import vstack
    adata.obsm['spatial'] = vstack([adata.obs['X'].values, adata.obs['Y'].values]).T
    spatial_coords = adata.obsm['spatial']
    kmeans = KMeans(n_clusters=n_spots, random_state=42).fit(spatial_coords)
    adata.obs['pseudo_spot'] = kmeans.labels_
    clustered_expression = adata.to_df().groupby(adata.obs['pseudo_spot']).sum()
    clustered_expression.index = clustered_expression.index.astype(str)
    pseudo_spot_coords = (
        adata.obs.groupby("pseudo_spot")[["x_bin", "y_bin"]].mean().values
        if "x_bin" in adata.obs and "y_bin" in adata.obs
        else adata.obs.groupby("pseudo_spot")[["X", "Y"]].mean().values
    )
    cell_counts = adata.obs["pseudo_spot"].value_counts().sort_index()
    if cell_type_keys[1] in adata.obsm:
        ctd_df = DataFrame(adata.obsm[cell_type_keys[1]], index=adata.obs.index)
        aggregated_ctd = ctd_df.groupby(adata.obs["pseudo_spot"]).mean().values
    elif cell_type_keys[0] in adata.obs:
        print(f'No cell type distribution found under name {cell_type_keys[1]}. Trying categorical cell types.')
        one_hot_ctd = get_dummies(adata.obs[cell_type_keys[0]])
        aggregated_ctd = one_hot_ctd.groupby(adata.obs["pseudo_spot"]).sum()
        aggregated_ctd = (aggregated_ctd.T / aggregated_ctd.sum(axis=1)).T.fillna(0).values
    else:
        print(
            f'No cell type distribution found under name {cell_type_keys[1]}. No categorical cell types found under name {cell_type_keys[0]}')
        aggregated_ctd = None
    new_adata = AnnData(clustered_expression)
    new_adata.obsm['spatial'] = pseudo_spot_coords
    new_adata.obs["X"] = new_adata.obsm["spatial"][:, 0]
    new_adata.obs["Y"] = new_adata.obsm["spatial"][:, 1]
    new_adata.obs['cell_counts'] = cell_counts.values
    if aggregated_ctd is not None:
        new_adata.obsm['cell_type_distribution'] = aggregated_ctd
    adata.uns['voxelized_subdata'] = new_adata
    return adata

#HELPER FUNCTION 1
# Assumption: SCE.var, SRT.var and SCE.obs_names, SRT.obs_names have matching genes, but maybe in a different order
# This function checks these assumptions, non-matching elements result in an error, matching elements
# with different order result in a copy of input anndata objects reordered so that they match
def _reorder_mtx(adata_real: AnnData, adata_sim: AnnData, intersect_genes: bool = False) -> Tuple[AnnData, AnnData]:
    """
    Reorders two AnnData objects according to a mutually matching gene order.
    Parameters:
        adata_real (AnnData): The first input AnnData object, typically containing real gene expression data.
        adata_sim (AnnData): The second input AnnData object, typically containing simulated gene expression data.
        intersect_genes (bool): If False, raises an error when the gene sets do not exactly match.
                                If True, only common genes are retained and reordered.
    Returns:
        Tuple[AnnData, AnnData]: The two AnnData objects with matching gene orders (optionally subsetted genes in case of mismatch).
    """
    from numpy import intersect1d
    df_real = adata_real.copy()
    df_sim = adata_sim.copy()
    genes_real = df_real.var['gene_id'].values
    genes_sim = df_sim.var['gene_id'].values
    mtx_sim = df_sim.X
    common_genes, gene_idx_real, gene_idx_sim = intersect1d(genes_real, genes_sim, return_indices=True)
    if len(gene_idx_sim) != mtx_sim.shape[1] and not intersect_genes:
        raise ValueError('Some gene names occur only in one of the datasets')
    else:
        df_sim = df_sim[:, gene_idx_sim].copy()
        df_real = df_real[:, gene_idx_real].copy()
        return df_real, df_sim

#HELPER FUNCTION 2
# This function transforms the locations of spatial data into a bounding square along x and y with side length = scale
# Should be called before grid transformation according to use (e.g, 1 if no rotation, scale 1/sqrt(2) if we rotate)
def _square_normalize(adata: AnnData, scale: float = 1) -> AnnData:
    """
    Normalizes the spatial coordinates (X, Y) of an AnnData object so that they fit within a square bounding box.

    Parameters:
        adata (AnnData): Input AnnData object with 2D spatial (X, Y) coordinates stored in 'obs' under keys 'X' and 'Y' respectively.
        scale (float): Desired size of the square's sides (default is 1).
                       For example, use 1 for full normalization or 1/√2 if a rotation will follow to make sure they stay inside [0,1]^2.
    Returns:
        AnnData: A new AnnData object with normalized spatial coordinates for the cells.
    """
    from numpy import min, max
    normalized = adata.copy()
    x = normalized.obs['X'].values
    y = normalized.obs['Y'].values
    Tx = scale * (x - min(x)) / (max(x) - min(x)) + (1 - scale) / 2
    Ty = scale * (y - min(y)) / (max(y) - min(y)) + (1 - scale) / 2
    normalized.obs['X'] = Tx
    normalized.obs['Y'] = Ty
    return normalized

#HELPER FUNCTION 3
# This function adds expression matrix with only svgs to anndata, should be performed before grid_tranforms.
# Should use genes=None, threshold=1, if one wants every gene.
def _add_svg_matrix(adata_real: AnnData, adata_sim: AnnData, GP_real: Optional[list] = None,
                   GP_sim: Optional[ndarray] = None, alpha: float = 0.05, threshold: float = 0.5,
                   genes: Optional[ndarray] = None, intersect_genes: bool = True,
                   only_abundance1: bool = True, only_abundance2: bool = False) -> Tuple[AnnData, AnnData]:
    """
    Adds a spatially variable gene (SVG) expression matrix to the .obsm slot of both real and simulated AnnData objects.

    This should be called prior to grid transformations. Filters genes based on SVG significance (usually based on SpatialDE) and expression abundance.

    Parameters:
        adata_real (AnnData): Real gene expression data.
        adata_sim (AnnData): Simulated gene expression data.
        GP_real (Optional[ndarray]): Gene-Probability double vector for real data (2D array: gene IDs and p-values). Defaults to None.
        GP_sim (Optional[ndarray]): Gene-Probability double vector for simulated data (2D array: gene IDs and p-values). Defaults to None.
        alpha (float): Significance threshold for SVG detection (default: 0.05).
        threshold (float): Maximum proportion of cells in which a gene may be expressed to be retained.
        genes (Optional[ndarray]): Specific set of genes to include. If None, automatically intersect SVGs from both sets.
        intersect_genes (bool): Whether to require exact matching of genes before processing (via `reorder_mtx`).
        only_abundance1 (bool): If True, binarizes expression for filtering.
        only_abundance2 (bool): If True, filters using binarized presence only (disregards abundance).
    Returns:
        Tuple[AnnData, AnnData]: The input AnnData objects with `.obsm['SVG']` populated.
    """
    from numpy import vstack, zeros, intersect1d, sum, max, newaxis, array
    adata_real, adata_sim = _reorder_mtx(adata_real, adata_sim, intersect_genes=intersect_genes)
    gene_names_real = adata_real.var['gene_id'].values
    gene_names_sim = adata_sim.var['gene_id'].values
    if GP_real is None:
        GP_real = vstack((gene_names_real, zeros(len(gene_names_real))))
    else:
        GP_real = GP_real
    if GP_sim is None:
        GP_sim = vstack((gene_names_sim, zeros(len(gene_names_sim))))
    else:
        GP_sim = GP_sim
    if genes is not None:
        genes = genes
    else:
        genes = None

    def _SVG_significance_test(GP, alpha=0.05, versions = True):
        if versions:
            GP = tuple(array(gp) for gp in GP)
            keep = GP[1] <= alpha

            result = tuple(gp[keep] for gp in GP)
        else:
            keep = GP[1] <= alpha
            result = GP[:, keep]
        return result

    def _get_common_indices(genes):
        common_indices_real = intersect1d(gene_names_real, genes, return_indices=True)[1]
        common_indices_sim = intersect1d(gene_names_sim, genes, return_indices=True)[1]
        if len(common_indices_real) != len(common_indices_sim):
            raise ValueError('Some of the given genes appear in only one of the datasets')
        return common_indices_real, common_indices_sim

    def _remove_above_threshold(SVG_matrix_real, SVG_matrix_sim, threshold=1, only_abundance1=True,
                               only_abundance2=False):
        M = SVG_matrix_real.shape[0]
        if only_abundance1:
            if only_abundance2:
                SVG_matrix_real_copy = SVG_matrix_real.copy()
                SVG_matrix_real_copy = (SVG_matrix_real_copy > 0).astype(int)
                keep = sum(SVG_matrix_real_copy, axis=0) / M <= threshold
            else:
                keep = sum(SVG_matrix_real, axis=0) / M <= threshold
        else:
            keep = sum(SVG_matrix_real, axis=0) / max(sum(SVG_matrix_real, axis=0)) <= threshold
        return SVG_matrix_real[:, keep], SVG_matrix_sim[:, keep]

        adata_real.obsm['SVG'] = SVG_matrix_real
        adata_sim.obsm['SVG'] = SVG_matrix_sim
        return adata_real, adata_sim

    SVG_real, SVG_sim = _SVG_significance_test(GP_real,alpha=alpha), _SVG_significance_test(GP_sim, alpha=alpha)
    common_genes = intersect1d(SVG_real[0], SVG_sim[0])
    if genes is None:
        common_indices_real, common_indices_sim = _get_common_indices(genes=common_genes)
    else:
        common_indices_real, common_indices_sim = _get_common_indices(genes=genes)

    if only_abundance1:
        SVG_matrix_real = (adata_real.X[:, common_indices_real] > 0).astype(int)
        SVG_matrix_sim = (adata_sim.X[:, common_indices_sim] > 0).astype(int)
    else:
        SVG_matrix_real = adata_real.X[:, common_indices_real]
        SVG_matrix_real = SVG_matrix_real * (1 / sum(SVG_matrix_real, axis=1))[:, newaxis]
        SVG_matrix_sim = adata_sim.X[:, common_indices_sim]
        SVG_matrix_sim = SVG_matrix_sim * (1 / sum(SVG_matrix_sim, axis=1))[:, newaxis]
    SVG_matrix_real, SVG_matrix_sim = _remove_above_threshold(SVG_matrix_real, SVG_matrix_sim,
                                                             threshold=threshold,
                                                             only_abundance1=only_abundance1,
                                                             only_abundance2=only_abundance2)
    adata_real.obsm['SVG'] = SVG_matrix_real
    adata_sim.obsm['SVG'] = SVG_matrix_sim
    return adata_real, adata_sim

#HELPER FUNCTION 4
# This function performs the grid transformation. It creates a new anndata object with new 'region_coordinates' and
# 'Region_ID' indices, 'neighbours' for neighbour coordinates, 'cell_type_distribution', 'ETD', 'SVG' distributions and 'cell_counts'
# inside regions
# Input anndata should already contain cell types 'adata.obs['cell_type']' and matrix for only svgs
# 'adata.obs['SVG']'. If CTD=True 'adata.obs['cell_type']' categorical CTs are used to create distribution vectors,
# otherwise if CTD=False adata.obsm['cell_type_distribution'] distribution vectors are used.
def _grid_transform(adata: AnnData, CTD: bool = True, gridsize: int = 4, show: bool = False,
                   figsize: int = 16, SVGD: bool = True) -> AnnData:
    """
    Performs a grid transformation on spatial data and returns a new AnnData object summarizing spatial features per grid region instead of cells.

    Parameters:
        adata (AnnData): Input AnnData object containing cell-level data with:
                         - adata.obs['cell_type']: categorical labels or
                         - adata.obsm['cell_type_distribution']: precomputed distributions
                         - adata.obsm['SVG']: spatially variable gene matrix
        CTD (bool): If True, use categorical cell types; if False, use precomputed cell type distributions.
        gridsize (int): Number of grid divisions along one axis (effective grid is (gridsize+2)^2 including borders, but borders are usually removed later).
        show (bool): If True, plots the grid overlay and cell counts to visualize the transformation.
        figsize (int): Size of the plot if show=True.
        SVGD (bool): If False, binarizes the SVG matrix across the grid.

    Returns:
        AnnData: A new AnnData object where each observation corresponds to a grid region with aggregated features.
    """
    from numpy import zeros, floor, sum, float32, array
    from pandas import get_dummies
    expMtx = adata.X.T
    N = expMtx.shape[0]
    M = expMtx.shape[1]
    k = gridsize
    gridsize = gridsize + 2
    if CTD:
        if 'cell_type' in adata.obs:
            CT = adata.obs['cell_type']
            ctMtx = (get_dummies(CT).astype(int)).values
        elif 'cell_type_distribution' in adata.obsm and CTD:
            ValueError("Provided data has no categorical cell types under .obs['cell_type'] in order to force use of categorical cell types.")
        else:
            ValueError("Provided data has no categorical cell types or cell type distributions under .obs['cell_type'] and .obsm['cell_type_distribution'] respectively.")
    else:
        if isinstance(adata.obsm['cell_type_distribution'], DataFrame):
            ctMtx = adata.obsm['cell_type_distribution'].values
        else:
            ctMtx = adata.obsm['cell_type_distribution']
    svgMtx = adata.obsm['SVG']
    m = ctMtx.shape[1]
    s = svgMtx.shape[1]
    x = adata.obs['X'].values
    y = adata.obs['Y'].values
    Txy = array([x, y]).T
    TexpMtx = zeros((N, k ** 2))
    TexpMtx_with_outside = zeros((N, gridsize ** 2))
    TctMtx = zeros((k ** 2, m + 1))
    TsvgMtx = zeros((k ** 2, s))
    TctMtx_with_outside = zeros((gridsize ** 2, m + 1))
    TsvgMtx_with_outside = zeros((gridsize ** 2, s))
    ETDMtx_with_outside = zeros((gridsize ** 2, 2))
    ETDMtx_with_outside[:, 1] = 1
    Tr = 1 + floor(k * Txy).astype(int)
    cell_counts_with_outside = zeros(gridsize ** 2)
    borders = array([(i - 1) / k for i in range(gridsize + 1)])
    grid_mid_points = [[(i - 0.5) / k, (j - 0.5) / k] for j in range(gridsize) for i in range(gridsize)]
    region_coordinates = array([[i, j] for j in range(gridsize) for i in range(gridsize)])
    region_indices = array([c[0] + gridsize * c[1] for c in region_coordinates])
    neighbours = array([[int(i - 1), int(i + 1), int(i + gridsize), int(i - gridsize), int(i + gridsize - 1),
                            int(i + gridsize + 1), int(i - gridsize + 1), int(i - gridsize - 1)] for i in
                           region_indices])
    for index, value in enumerate(Tr):
        if value[0] == k + 1:
            value[0] = k
        if value[1] == k + 1:
            value[1] = k
    for index, value in enumerate(Tr):
        cell_counts_with_outside[value[0] + value[1] * gridsize] += 1
    for index, value in enumerate(Tr):
        TexpMtx_with_outside[:, value[0] + value[1] * gridsize] += expMtx[:, index]
        if cell_counts_with_outside[value[0] + value[1] * gridsize] != 0:
            TsvgMtx_with_outside[value[0] + value[1] * gridsize, 0:s] += svgMtx[index] * 1 / (
            cell_counts_with_outside[value[0] + value[1] * gridsize])
            TctMtx_with_outside[value[0] + value[1] * gridsize, 0:m] += ctMtx[index] * 1 / (
            cell_counts_with_outside[value[0] + value[1] * gridsize])
            ETDMtx_with_outside[value[0] + value[1] * gridsize, 0] = 1
            ETDMtx_with_outside[value[0] + value[1] * gridsize, 1] = 0
        else:
            TctMtx_with_outside[value[0] + value[1] * gridsize, m] = 1
    if not SVGD:
        TsvgMtx_with_outside = (TsvgMtx_with_outside > 0).astype(int)

    for i in range(TctMtx_with_outside.shape[0]):
        if sum(TctMtx_with_outside[i]) == 0:
            TctMtx_with_outside[i, m] = 1
    # TODO: Save it instead of showing it
    if show:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(figsize, figsize))
        plt.plot(x, y, '.', markersize=6, color='red')
        for i, p in enumerate(grid_mid_points):
            plt.text(p[0], p[1], str(cell_counts_with_outside[i]), fontsize=figsize, ha='center', weight="bold")
        for v in borders:
            plt.axvline(x=v, color='black', linestyle='--')
        for u in borders:
            plt.axhline(y=u, color='black', linestyle='--')
        plt.show()

    region_data = DataFrame(columns=['Region_ID', 'X', 'Y', 'm'])
    region_data['Region_ID'] = region_indices
    # for i in range(TctMtx_with_outside.shape[1]):
    #    region_data[str(i)] = TctMtx_with_outside[:,i]
    region_data['X'] = region_coordinates[:, 0]
    region_data['Y'] = region_coordinates[:, 1]
    genes = DataFrame(columns=['gene_id'])
    genes['gene_id'] = adata.var.index
    genes.index = adata.var.index

    result = AnnData(X=TexpMtx_with_outside.T.astype(float32), obs=region_data, var=genes)
    result.obsm['cell_type_distribution'] = TctMtx_with_outside
    # print(TctMtx_with_outside.shape)
    result.obsm['SVG'] = TsvgMtx_with_outside
    result.obsm['ETD'] = ETDMtx_with_outside
    result.obsm['neighbours'] = neighbours
    result.obs['cell_counts'] = cell_counts_with_outside
    result.k = k
    return result




