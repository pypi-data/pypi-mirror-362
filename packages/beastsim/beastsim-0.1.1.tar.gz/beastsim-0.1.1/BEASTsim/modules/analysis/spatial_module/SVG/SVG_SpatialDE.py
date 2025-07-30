import logging
import NaiveDE
import SpatialDE
import contextlib
from BEASTsim.beast_data import *
from BEASTsim.utils.utils_cache import _use_cache
from copy import deepcopy
from tqdm import tqdm
from typing import Dict,List
import os
import pandas as pd
from pandas import DataFrame
from anndata import AnnData

logging.getLogger("matplotlib").setLevel(logging.WARNING)

class SVG_SpatialDE():
    def __init__(self, parameters):
        self.parameters = parameters
        self.parameters_SpatialDE=parameters["Analysis"]["Spatial"]["SVG"]["SpatialDE"]
        self.rng = np.random.default_rng()
        self.kernel_space: Optional[Dict[str, float]] = None
        self.genes: Optional[List[str]] = None

    @staticmethod
    def calc_SVGs(spatial_data: Union[BEAST_Data, AnnData]):
        """
        Calculates Spatially Variable Gene (SVG) statistics for a spatial
        transcriptomics dataset with SpatialDE and stores the results in
        the AnnData `.var` table under the columns ``"p_val"`` and
        ``"q_val"`` (Benjamini–Hochberg–adjusted).

        Processing steps
        ----------------
        1. Accept either a :class:`BEAST_Data` wrapper or a raw
           :class:`anndata.AnnData`.
        2. Remove genes that are expressed in zero cells.
        3. If the columns ``"p_val"`` / ``"q_val"`` are missing, build a count
           matrix, apply NaiveDE normalisation + residualisation
           (``total_counts`` covariate, following the SpatialDE tutorial),
           and run SpatialDE on the residuals.
        4. Write the resulting per-gene statistics into ``.var``; any genes not
           tested are filled with 1 so that downstream filters behave
           consistently.

        All calculations are performed on a copy of the input AnnData; only
        the final ``.var`` columns are written back to spatial_data.

        Parameters
        ----------
        spatial_data : Union[BEAST_Data, AnnData]
            Spatial dataset (cells × genes) to annotate with SVG p-values.

        Returns
        -------
        None
            spatial_data is annotated in place.

        Raises
        ------
        ValueError
            If spatial_data is neither a :class:`BEAST_Data` nor an
            :class:`anndata.AnnData` instance.

        References
        ----------
        Svensson V., Teichmann S. A., Stegle O.
        SpatialDE: identification of spatially variable genes.
        Nature Methods 15, 343–346 (2018).
        doi:10.1038/nmeth.4636
        """
        if isinstance(spatial_data, BEAST_Data):
            adata = deepcopy(spatial_data.data)
        elif isinstance(spatial_data, AnnData):
            adata = deepcopy(spatial_data)
        else:
            raise ValueError("calcSVGs can only take MOPITAS_Dataset or AnnData.")
        nonZeroCells = adata.X.sum(axis=1) > 0
        adata = adata[nonZeroCells]
        if "p_val" not in adata.var or "q_val" not in adata.var:
            counts = DataFrame(
                adata.X.toarray() if not isinstance(adata.X, np.ndarray) else adata.X,
                index=adata.obs_names,
                columns=adata.var_names
            )
            counts = counts.T[counts.sum(0) >= 3].T
            sample_info = DataFrame({
                'x': adata.obs['X'],
                'y': adata.obs['Y'],
                'total_counts': np.sum(counts, axis=1)
            })
            counts = counts.loc[sample_info.index]
            norm_expr = NaiveDE.stabilize(counts.T).T
            resid_expr = NaiveDE.regress_out(sample_info, norm_expr.T, 'np.log(total_counts)').T
            results = SpatialDE.run(X=np.array(sample_info[['x', 'y']]), exp_tab=resid_expr)
            GP = results[['g', 'pval', 'qval']].values.T
            if isinstance(spatial_data, BEAST_Data):
                spatial_data.data.var["p_val"] = results.set_index("g")["pval"]
                spatial_data.data.var["q_val"] = results.set_index("g")["qval"]
            else:
                spatial_data.var["p_val"] = results.set_index("g")["pval"]
                spatial_data.var["q_val"] = results.set_index("g")["qval"]

        if isinstance(spatial_data, BEAST_Data):
            spatial_data.data.var["p_val"] = spatial_data.data.var["p_val"].fillna(1)
            spatial_data.data.var["q_val"] = spatial_data.data.var["q_val"].fillna(1)
        else:
            spatial_data.var["p_val"] = spatial_data.var["p_val"].fillna(1)
            spatial_data.var["q_val"] = spatial_data.var["q_val"].fillna(1)

    @staticmethod
    def calc_SVGs_all(spatial_datasets: Union[BEAST_Data, List[BEAST_Data]]):
        """
        Batch wrapper around ``SVG_SpatialDE.calc_SVGs``.
        For **every** spatial dataset in spatial_datasets the function computes
        Spatially-Variable-Gene statistics (``"p_val"``, ``"q_val"``) and writes
        them into the dataset’s ``.var`` table.

        Special handling for *ground-truth* copies
        If the first dataset in the list is a copied reference
        (``dataset.copied is True``) the resulting ``p_val`` / ``q_val`` columns
        are propagated to the matching simulation whose ``.name`` equals
        ``"GT-<real_dataset.name>"`` — avoiding redundant re-computations.

        A tqdm progress-bar shows overall progress.

        Parameters
        ----------
        spatial_datasets : Union[BEAST_Data, List[BEAST_Data]]
            One spatial dataset or a list; a single instance is wrapped into a
            list automatically.

        Returns
        -------
        None
            All datasets are annotated in place.
        """
        if not isinstance(spatial_datasets, List):
            spatial_datasets = [spatial_datasets]
        pbar = tqdm(total=len(spatial_datasets), desc="Annotating SVGs.", leave=False)
        for idx, spatial_data in enumerate(spatial_datasets):
            SVG_SpatialDE.calc_SVGs(spatial_data)
            if idx == 0:
                if spatial_data.copied:
                    for sim in spatial_datasets:
                        sim_name = sim.name
                        if sim_name == f"GT-{spatial_data.name}":
                            if "p_val" not in sim.data.var or "q_val" not in sim.data.var:
                                sim.data.var["p_val"] = spatial_data.data.var["p_val"]
                                sim.data.var["q_val"] = spatial_data.data.var["q_val"]
            pbar.update(1)
        pbar.close()
