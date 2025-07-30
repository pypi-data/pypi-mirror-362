from anndata import AnnData
from pandas import Series
from tqdm import tqdm
import warnings
from typing import List, Optional
from BEASTsim.beast_data import BEAST_Data
from BEASTsim.utils.utils import _square_normalize, _add_svg_matrix, _grid_transform
from BEASTsim.modules.analysis.spatial_module.simulation.plotting.neighborhood_plotting import NeighborhoodPlotting
from BEASTsim.modules.analysis.spatial_module.simulation.plotting.SVG_plotting import SVGPlotting

warnings.filterwarnings('ignore', category=UserWarning, message='Transforming to str index.')

class SpatialBiologicalSignals:
    def __init__(self, parameters):
        self.parameters = parameters
        self.spatial_bio_signals_parameters = self.parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]["SpatialBiologicalSignals"]

    def run(self, real_data: BEAST_Data, simulated_data: BEAST_Data, alpha: Optional[float] = None) -> Series:
        """
        Compute the **spatial biological-signal benchmarks** for one simulation:

        1. **Neighbourhood benchmark** – χ² p-values / Dice scores comparing
           observed vs expected conditional distributions of neighbouring cell
           types.
        2. **SVG benchmark** – Dice loss between classifications of spatially
           variable genes (SpatialDE) in real vs simulated data.

        The method detects voxelised sub-datasets automatically, falls back to the
        spot-level matrices when absent, executes both benchmarks, concatenates
        their Series, and returns the stacked score vector.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset.
        simulated_data : BEAST_Data
            Simulated dataset to benchmark.
        alpha : Optional[float], default None
            Significance level for the SVG benchmark *p*-values. If None, the
            value from the JSON parameters is used.

        Returns
        -------
        pandas.Series
            All neighbourhood and SVG benchmark scores indexed by metric name.

        References
        ----------
        Svensson V., Teichmann S.A., Stegle O. (2018).
        """
        from pandas import concat
        adata_real = real_data.data
        adata_sim = simulated_data.data

        if "voxelized_subdata" in adata_real.uns:
            adata_real_voxel = adata_real.uns["voxelized_subdata"]
            adata_real_voxel.var['gene_id'] = adata_real.var.index
            adata_sim_voxel = adata_sim.uns["voxelized_subdata"]
            adata_sim_voxel.var['gene_id'] = adata_sim.var.index
        else:
            adata_real_voxel = adata_real
            adata_sim_voxel = adata_sim

        if alpha is None:
            alpha = self.spatial_bio_signals_parameters["alpha"]

        benchmarks = [(self.neighborhood_benchmark, (adata_real_voxel, adata_sim_voxel, None)),
                      (self.svg_benchmark, (adata_real, adata_sim, alpha))]
        results = []

        total_iterations = len(benchmarks)

        with tqdm(
                total=total_iterations, desc="Running Spatial Biological Signal Benchmarks", unit="step"
        ) as progress_bar:
            for benchmark_function, args in benchmarks:
                results.append(benchmark_function(*args))
                progress_bar.update(1)

        results_df = concat(results, axis=0)
        results_df.name = simulated_data.name
        return results_df

    # SPATIAL BIOLOGICAL SIGNALS

    # NEIGHBOURHOOD BENCHMARK
    # This function performs all necessary preprocessing steps and then uses the NEIGHBOURHOOD BENCHMARK
    def compute_neighborhoods(self, adata_real, adata_sim, gridsize=32):
        """
        End-to-end helper that:

        1. Adds SVG matrices to both datasets,
        2. Square-normalises spatial coordinates and rasterises each dataset to a
           regular grid of size *gridsize × gridsize*,
        3. Calls ``NeighborhoodPlotting._calculate_cell_type_neighborhood``,
        4. Returns both the detailed output list and the summary score list.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset.
        adata_sim : AnnData
            Simulated dataset.
        gridsize : int, default 32
            Grid resolution used for rasterisation.

        Returns
        -------
        tuple[list, list]
            (full_list, partial_list) where ``full_list`` contains conditional
            distribution matrices, raw χ² / Dice arrays, ordering etc., and
            ``partial_list`` holds the mean χ² and Dice scores that define the
            neighbourhood benchmark.
        """
        genes = None
        real, sim = _add_svg_matrix(adata_real, adata_sim, genes=genes, intersect_genes=True, only_abundance1=True,
                                         only_abundance2=False,
                                         threshold=1)
        real1 = _square_normalize(real, scale=1)
        sim1 = _square_normalize(sim, scale=1)
        grid_real = _grid_transform(real1, CTD=self.spatial_bio_signals_parameters["force_categorical"],
                                         gridsize=gridsize, show=False,  # TODO: REMOVE SHOW
                                         SVGD=True)
        grid_sim = _grid_transform(sim1, CTD=self.spatial_bio_signals_parameters["force_categorical"], gridsize=gridsize,
                                        show=False,  # TODO: REMOVE SHOW
                                        SVGD=True)
        full_list, partial_list = NeighborhoodPlotting._calculate_cell_type_neighborhood(grid_real, grid_sim,
                                                                         number_of_cells=self.spatial_bio_signals_parameters[
                                                                   "number_of_cells"],
                                                                         alpha=self.spatial_bio_signals_parameters["alpha"],
                                                                         two_sample=self.spatial_bio_signals_parameters[
                                                                   "two_sample"], use_dice_scores=self.spatial_bio_signals_parameters["use_dice_scores"], use_chi2_scores=self.spatial_bio_signals_parameters["use_chi2_scores"])
        return full_list, partial_list

    def neighborhood_benchmark(self, adata_real, adata_sim, gridsize=32) -> Series:
        """
        Thin wrapper around ``compute_neighborhoods``; runs the full neighbourhood
        benchmark pipeline and returns **only** the summary score Series.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset.
        adata_sim : AnnData
            Simulated dataset.
        gridsize : int, default 32
            Grid resolution; auto-scaled if None.

        Returns
        -------
        pandas.Series
            Neighbourhood-benchmark summary scores.
        """
        from numpy import floor, log2
        if gridsize is None:
            gridsize = int(floor(2**(log2(adata_real.X.shape[0])/2)))
        _, results = self.compute_neighborhoods(adata_real, adata_sim, gridsize=gridsize)
        return results

    def svg_benchmark(self, adata_real, adata_sim, alpha=0.05) -> Series:
        """
        Perform the **spatially variable genes** (SVG) benchmark by running
        ``SVGPlotting._computeSVGs`` on the two datasets and returning the score
        vector (Dice loss, overlap, etc.) at the chosen significance level α.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset.
        adata_sim : AnnData
            Simulated dataset.
        alpha : float, default 0.05
            *p*-value threshold applied to SpatialDE q-values when defining SVG
            sets.

        Returns
        -------
        pandas.Series
            SVG benchmark scores (one value per metric).

        References
        ----------
        Svensson V., Teichmann S.A., Stegle O. (2018).
        """
        plotting_df = SVGPlotting._computeSVGs(adata_real=adata_real, adata_sim=adata_sim, alpha=alpha, start=None, end=None, N=None)
        return plotting_df