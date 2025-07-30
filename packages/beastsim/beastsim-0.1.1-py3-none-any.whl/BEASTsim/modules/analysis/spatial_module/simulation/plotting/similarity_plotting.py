import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from BEASTsim.beast_data import *
from BEASTsim.utils.utils import _square_normalize, _add_svg_matrix, _grid_transform
from tqdm import tqdm

class SimilarityPlotting:
    def __init__(self, parameters):
        self.parameters = parameters
        self.spatial_analysis_parameters = self.parameters["Analysis"]["Spatial"]
        self.dir = self.spatial_analysis_parameters["output"]

    def run_plot_ctd_svg(self, real: BEAST_Data, sim: BEAST_Data, threshold=1, show=False, force_categorical=False, save=True,
                         save_name='similarity_plot', benchmark='cell_type_distribution', svg_distribution=True, find_rot='n',
                         gridsizes=None, gridsize_to_optimize=None, angle=20, genes=None, check_for_voxelized=False, save_path=None):
        """
           Comperative grid based analysis of cell type distribution or cell type neighborhood category distribution of regions in real and simulated data.
           Visualized as multi-resoultion heatmap plots of the two spatial tissue's grid-dissection placed on top of each other with customizable rotation.

           Calculates and visualises the similarity between real and sim in terms
           of the continuous Dice score between the average properties of cells (or
           voxels) falling into spatially overlapping square regions.

           Parameters
           ----------
           real : BEAST_Data
               Real dataset.
           sim : BEAST_Data
               Simulated dataset.
           threshold : int, default 1
               If smaller than 1, genes that are expressed in more that `threshold*100%` of cells are trimmed away as
               a processing step before the grid transformation.
           show : bool, default False
               Indicating if we want to show the created plots interactively.
           force_categorical : bool, default False
               If `True`, for both real and simulated data `adata.obs["cell_type"]` categories will be considered the
               cell types aggregated by the grid transformation into a distribution for each region and used in further steps.
               If `False`, for both real and simulated data `adata.obsm["cell_type_distributions"]` will be aggregated
               by the grid transformation into regional average distributions and used in further steps.
           save : bool, default True
               ndicating if we want to save the created plots at the set path.
           save_name : str, default "similarity_plot"
               Filename prefix for saved plots.
           benchmark : str { "cell_type_distribution", "SVG" }, default "cell_type_distribution"
               Decides if similarity should be assessed in terms of cell type distributions or spatially variable gene expressions.
               The two functionalities are similar in their design but in terms of the data and results, they are directly independent.
           svg_distribution : bool, default True
               If set to `False`, the grid transformation assigns for each region, for a each gene, 1 or 0 depending on
               if any cells inside the region contains the gene or not.
               If set to `True`, each cell gets assigned the value 1 or 0 depending on if the gene is expressed in the
               cell or not and the grid transformation assigns for each region the arithmetic average of the 0-1 vectors
               of the cells inside the regions.
           find_rot : str { "n", "y", "b" }, default "n"
               If set to `'y'`, additionally to the basic test, multiple rounds of similarity tests will be performed,
               rotating the simulated tissue by the chosen `angle` parameter `int(360/angle)` times and flipped along
               the `x=0.5` middle axis to find the combination of transformations which maximizes the average type overlap
               score (CT_overlap, or SVG_overlap) for the resolution layer with `gridsize_to_optimize` grid size, afterwards,
               the score maximizing transformation is plotted additionally to the basic plot.
               If set to `'b'`, the lowest score instance is also found and plotted. If set to `'n'`, this functionality
               is disabled completely.
           gridsizes : Optional[List[int]], default None
               Chooses the density of the grid partition of the grid transformation steps for each tested resolution layer.
               If set to `None`, the maximum grid size will be determined based on the number of cells in the real data
               according to the following formula `int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))` and the smaller
               grid sizes will follow powers of 2 starting from 1 up to the larges power that is smaller than the previously
               determined maximum.
           gridsize_to_optimize : Optional[int], default None
               As explained for the `find_rot` parameter. If set to `None`, the last grid size in `gridsizes` is chosen.
           angle : float, default 20
               As explained for the `find_rot` parameter. Interpreted as degrees.
           genes : Optional[List[str]], default None
               This parameter is generally should be set to `None`, in which case we select genes with SpatialDE
               adjusted p-value smaller than 0.05 from the real tissue and consider the subset of these genes that also
               exist in the simulated tissue for this similarity comparison.
               If not `None`, the full list of genes considered for this similarity comparison can be customized by
               listing them in the `genes` parameter, potentially disregarding spatial variablity.
           check_for_voxelized : bool, default False
               If `True` and for both real and simulated data the `adata.uns["voxelized_subdata"]` anndata part exists,
               then those will be the datasets analyzed and compared instead of the outside anndata object.
               If either subdata doesn't exist, then it defaults to the outside object. If `False`, the
               `adata.uns["voxelized_subdata"]` is disregarded even if it exists. The rest of the parameters refer to
               the real and simulated datasets picked in this step.
           save_path : Optional[str], default self.dir
               Directory in which to save plots.

           Returns
           -------
             If `find_rot == "n"`
              → `(adata_real_normalised, adata_sim_normalised)` — both datasets after
              square-normalisation.

             If `find_rot in {"y", "b"}`
              → `(adata_real_normalised, best_simulated_view)` where `best_simulated_view`
              is the `anndata` with the highest-similarity rotation/flipping of the simulation.
        """
        adata_real = real.data
        adata_real_name = real.name
        adata_sim = sim.data
        adata_sim_name = sim.name
        if save_path is None:
            save_path =  self.dir
        if benchmark == 'SVG':
            from BEASTsim.modules.analysis.spatial_module.SVG.SVG_SpatialDE import SVG_SpatialDE
            SVG_SpatialDE.calc_SVGs(adata_real)
            SVG_SpatialDE.calc_SVGs(adata_sim)
            genes_real = adata_real.var['q_val'].index.to_numpy()
            genes_sim = adata_sim.var['q_val'].index.to_numpy()
            values_real = adata_real.var['q_val'].values
            values_sim = adata_sim.var['q_val'].values
            GP_real = [genes_real, values_real]
            GP_sim = [genes_sim, values_sim]
            if check_for_voxelized:
                if "voxelized_subdata" in adata_real.uns:
                    q_val_real = adata_real.var['q_val']
                    adata_real = adata_real.uns["voxelized_subdata"]
                    adata_real.var['q_val'] = q_val_real
                    if 'gene_id' not in adata_real.var.columns:
                        adata_real.var['gene_id'] = adata_real.var.index
                else:
                    Warning('No voxelized real data was found, defaulting to outside dataset.')
                    adata_real = adata_real
                if "voxelized_subdata" in adata_sim.uns:
                    q_val_sim = adata_sim.var['q_val']
                    adata_sim = adata_sim.uns["voxelized_subdata"]
                    adata_sim.var['q_val'] = q_val_sim
                    if 'gene_id' not in adata_sim.var.columns:
                        adata_sim.var['gene_id'] = adata_sim.var.index
                else:
                    Warning('No voxelized simulated data was found, defaulting to outside dataset.')
                    adata_sim = adata_sim
        else:
            GP_real = None
            GP_sim = None
            if check_for_voxelized:
                if "voxelized_subdata" in adata_real.uns:
                    adata_real = adata_real.uns["voxelized_subdata"]
                    if 'gene_id' not in adata_real.var.columns:
                        adata_real.var['gene_id'] = adata_real.var.index
                else:
                    Warning('No voxelized real data was found, defaulting to outside dataset.')
                    adata_real = adata_real
                if "voxelized_subdata" in adata_sim.uns:
                    adata_sim = adata_sim.uns["voxelized_subdata"]
                    if 'gene_id' not in adata_sim.var.columns:
                        adata_sim.var['gene_id'] = adata_sim.var.index
                else:
                    Warning('No voxelized simulated data was found, defaulting to outside dataset.')
                    adata_sim = adata_sim
        if gridsizes is None:
            max_gridsize = int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))
            max_simple_layer_size = int(np.floor(np.log2(adata_real.X.shape[0]) / 2))
            gridsizes = [2 ** i for i in range(max_simple_layer_size + 1)]
            gridsizes.append(max_gridsize)
        if gridsize_to_optimize is None:
            gridsize_to_optimize = int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))
        adata_real = self._set_CTD_from_probabilities(adata_real)
        adata_sim = self._set_CTD_from_probabilities(adata_sim)
        adata_real, adata_sim = _add_svg_matrix(adata_real, adata_sim, GP_real=GP_real, GP_sim=GP_sim, genes=genes, intersect_genes=True, threshold=threshold)
        if find_rot == 'y':
            adata_real1 = _square_normalize(adata_real, scale=1 / (2 ** (1 / 2)))
            adata_sim1 = _square_normalize(adata_sim, scale=1 / (2 ** (1 / 2)))
            B, W, best, worst = self._find_best_view(adata_real1, adata_sim1, angle=angle, gridsize_to_optimize = gridsize_to_optimize, noCT=force_categorical, benchmark=benchmark)
            save_name_best = save_name + '_best_' + '_Flipped_' + str(B[1] == 1) + '_rotated_' + str(B[2]) + '_degrees'
            save_name_worst = save_name + '_worst_' + '_Flipped_' + str(B[1] == 1) + '_rotated_' + str(B[2]) + '_degrees'
            self._run_for_layers(adata_real1, best, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name_best, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            self._run_for_layers(adata_real1, worst, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name_worst, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            return adata_real1, best
        elif find_rot == 'n':
            adata_real2 = _square_normalize(adata_real, scale=1)
            adata_sim2 = _square_normalize(adata_sim, scale=1)
            self._run_for_layers(adata_real2, adata_sim2, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, threshold=threshold, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            return adata_real2, adata_sim2
        else:
            adata_real1 = _square_normalize(adata_real, scale=1 / (2 ** (1 / 2)))
            adata_sim1 = _square_normalize(adata_sim, scale=1 / (2 ** (1 / 2)))
            B, W, best, worst = self._find_best_view(adata_real1, adata_sim1, angle=angle, gridsize_to_optimize = gridsize_to_optimize, noCT=force_categorical, benchmark=benchmark)
            save_name_best = save_name + '_best_' + '_Flipped_' + str(B[1] == 1) + '_rotated_' + str(B[2]) + '_degrees'
            save_name_worst = save_name + '_worst_' + '_Flipped_' + str(B[1] == 1) + '_rotated_' + str(B[2]) + '_degrees'
            self._run_for_layers(adata_real1, best, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name_best, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            self._run_for_layers(adata_real1, worst, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name_worst, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            adata_real2 = _square_normalize(adata_real, scale=1)
            adata_sim2 = _square_normalize(adata_sim, scale=1)
            self._run_for_layers(adata_real2, adata_sim2, show=show, noCTreal=force_categorical, noCTsim=force_categorical, save=save,
                                 save_name=save_name, benchmark=benchmark, svg_distribution=svg_distribution, gridsizes=gridsizes, threshold=threshold, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            return adata_real1, best

    # SPATIAL DICE SCORES  (OVERLAP/AVERAGE for CTD/ETD/SVG) (possible extension to add CHi2-test scores):
    # This function compares differences in cell type, svg, empty/non-empty distributions between
    # two grid-transformed spatial data using the continuous dice score.
    # Works only with anndata outputs of the grid_transform function
    @staticmethod
    def _spatial_similarity_benchmark(df_real, df_sim, p=2, empty_when_one_empty=True, benchmark='cell_type_distribution'):
        """
        Compute Dice-score similarity metrics
        between two grid-transformed spatial datasets for a chosen resolution
        layer, for a benchmarked characteristic:

        cell_type_distribution – regional CT-probability vectors
        SVG – regional occurrence/occurrence proportion vectors for spatially variable genes

        Steps
        -----
        1. Slice out the inner (k−2)² regions to avoid padded borders.
        2. Build per-region 2-D matrices for the chosen benchmark and for the
           empty/non-empty map (ETD).
        3. For each region compute Dice scores
           comparing real vs simulated distributions (row-wise).
        4. Aggregate region-level metrics to give four mean scores:
           Dice_CT, Dice_Cell, Dice_ET, Dice_Cell_ET.
        5. Return a “full” list with per-row details and a “partial” list
           containing only the four mean scores (ready for plotting/ranking).

        Parameters
        ----------
        df_real : AnnData
            Grid-transformed real dataset produced by ``grid_transform``; must contain
            ``obsm[benchmark]`` and ``obsm["ETD"]``.
        df_sim : AnnData
            Grid-transformed simulated dataset with the same fields.
        p : int, default 2
            Power parameter in the continuous Dice score formula
        empty_when_one_empty : bool, default True
            For cell-wise Dice on ETD: ignore regions where one patch is empty and
            the other is not.
        benchmark : str { "cell_type_distribution", "SVG" }
            Chooses which characteristic is benchmarked
        use_dice_scores : bool, default True
            Include Dice scores in the output lists.
        use_chi2_scores : bool, default True
            Include χ² statistics / p-values in the output.
        result_order : bool, default False
            Re-order rows by abundance before returning probability matrices. The exact index ordering is later saved.

        Returns
        -------
        tuple[list, pandas.Series]
            full_list
                ``[[dice_CT_rows, mean_dice_CT], [dice_Cell_rows, mean_dice_Cell],``
                ``[dice_ET_rows, mean_dice_ET], [dice_Cell_ET_rows, mean_dice_Cell_ET]]``
            partial_list
                Series with four values:
                ``["Dice_CT", "Dice_Cell", "Dice_ET", "Dice_Cell_ET"]``

        Notes
        -----
         NaNs (e.g. rows with zero denominator) are replaced by zero in both
          full_list and partial_list.
        """
        from BEASTsim.utils.utils import _replace_nan_with_zero
        def no_empty(mtx_real, mtx_sim, m):
            no_empty_mtx_real = np.empty(((k - 2) ** 2, m))
            no_empty_mtx_sim = np.empty(((k - 2) ** 2, m))
            for j in range(1, k - 1):
                for i in range(1, k - 1):
                    no_empty_mtx_real[(i - 1) + (j - 1) * (k - 2)] = mtx_real[i + j * k][
                                                                     0:m]
                    no_empty_mtx_sim[(i - 1) + (j - 1) * (k - 2)] = mtx_sim[i + j * k][
                                                                    0:m]
            return no_empty_mtx_real, no_empty_mtx_sim
        M = df_real.X.shape[0]
        k = int(M ** (1 / 2))
        CT_mtx_real = df_real.obsm[benchmark]
        CT_mtx_sim = df_sim.obsm[benchmark]
        ET_mtx_real = df_real.obsm['ETD']
        ET_mtx_sim = df_sim.obsm['ETD']
        if benchmark == 'cell_type_distribution':
            m = CT_mtx_real.shape[1] - 1
        elif benchmark == 'SVG':
            m = CT_mtx_real.shape[1]
        no_empty_CT_mtx_real, no_empty_CT_mtx_sim = no_empty(CT_mtx_real, CT_mtx_sim, m)
        no_empty_ET_mtx_real, no_empty_ET_mtx_sim = no_empty(ET_mtx_real, ET_mtx_sim, 2)
        def get_dice_score(real, sim, axis=0, p=2, empty_when_one_empty=False, ET=False):
            if not len(real.shape) < 2:
                numerator = np.sum((real - sim) ** p, axis=axis)
                denominator = np.sum(real ** p, axis=axis) + np.sum(sim ** p, axis=axis)
            else:
                numerator = np.sum((real - sim) ** p)
                denominator = np.sum(real ** p) + np.sum(sim ** p)
            if axis == 1:
                with np.errstate(divide='ignore', invalid='ignore'):
                    if empty_when_one_empty:
                        no_cells_in_one = no_empty_ET_mtx_real[:, 0] * no_empty_ET_mtx_sim[:, 0]
                        numerator2 = numerator[no_cells_in_one != 0]
                        denominator2 = denominator[no_cells_in_one != 0]
                        numerator2 = numerator2[denominator2 != 0]
                        denominator2 = denominator2[denominator2 != 0]
                    else:
                        numerator2 = numerator[denominator != 0]
                        denominator2 = denominator[denominator != 0]
                    score2 = 1 - (numerator2 * 1 / denominator2)
                    if empty_when_one_empty:
                        denominator[no_cells_in_one == 0] = 0
                    if ET:
                        S = np.vstack((real, sim)).T
                        result = np.zeros(S.shape[0])
                        result[(S == (1, 0)).all(axis=1)] = 1
                        result[(S == (0, 1)).all(axis=1)] = 0
                        result[(S == (0, 0)).all(axis=1)] = float('inf')
                        result[(S == (1, 1)).all(axis=1)] = float('inf')
                    else:
                        result = 1 - (numerator * 1 / denominator)
                    no_empty_mean = np.mean(score2)
            elif axis == 0:
                score = 1 - (numerator * 1 / denominator)
                result = score
                no_empty_mean = np.mean(score)
            return result, no_empty_mean

        dice_score_per_CT, mean_dice_score_CT = get_dice_score(no_empty_CT_mtx_real,no_empty_CT_mtx_sim, axis=0,p=p)
        dice_score_per_Cell, mean_dice_score_Cell = get_dice_score(
            no_empty_CT_mtx_real[:, 0:m], no_empty_CT_mtx_sim[:, 0:m],
            axis=1, p=p, empty_when_one_empty=empty_when_one_empty)
        dice_score_per_ET, mean_dice_score_ET = get_dice_score(no_empty_ET_mtx_real[:, 0],
                                                                              no_empty_ET_mtx_sim[:, 0], axis=0, p=p)
        dice_score_per_Cell_ET, mean_dice_score_Cell_ET = get_dice_score(no_empty_ET_mtx_real[:, 0],
                                                                         no_empty_ET_mtx_sim[:, 0], axis=1, p=p, ET=True)
        Full_List = [[dice_score_per_CT, mean_dice_score_CT], [dice_score_per_Cell, mean_dice_score_Cell],
                     [dice_score_per_ET, mean_dice_score_ET], [dice_score_per_Cell_ET, mean_dice_score_Cell_ET]]

        Partial_List = [mean_dice_score_CT, mean_dice_score_Cell, mean_dice_score_ET, mean_dice_score_Cell_ET]

        Partial_List = _replace_nan_with_zero(Partial_List)
        Full_List= _replace_nan_with_zero(Full_List)
        return Full_List, Partial_List

    def _set_CTD_from_probabilities(self, adata):
        if 'probabilities' in adata.obsm:
            adata.obsm['CTD'] = adata.obsm['probabilities']
        elif 'cell_type_distribution' in adata.obsm:
            adata.obsm['CTD'] = adata.obsm['cell_type_distribution']
        return adata

    def _trunc(self, values, decs=0):
        return np.trunc(values * 10 ** decs) / (10 ** decs)

    def _rot_matrix(self, angle):
        rad = np.deg2rad(angle)
        R = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
        return R

    def _resize_rotations_and_flip(self, adata, angle):
        List_anndatas = []
        number_of_rotations = int(360 / angle)
        for i in range(2):
            for j in range(number_of_rotations):
                if i == 0:
                    current_angle = j / number_of_rotations * 360
                    adata_ij = adata.copy()
                    coords = np.vstack((adata_ij.obs['X'].values, adata_ij.obs['Y'].values))
                    coords = coords - 1 / 2
                    new_coords = self._rot_matrix(current_angle) @ coords
                    adata_ij.obs['X'] = new_coords[0] + 1 / 2
                    adata_ij.obs['Y'] = new_coords[1] + 1 / 2
                    List_anndatas.append(adata_ij)
                else:
                    current_angle = j / number_of_rotations * 360
                    adata_ij = adata.copy()
                    xmax = np.max(adata_ij.obs['X'].values)
                    adata_ij.obs['X'] = 1 - adata_ij.obs['X'].values
                    coords = np.vstack((adata_ij.obs['X'].values, adata_ij.obs['Y'].values))
                    coords = coords - 1 / 2
                    new_coords = self._rot_matrix(current_angle) @ coords
                    adata_ij.obs['X'] = new_coords[0] + 1 / 2
                    adata_ij.obs['Y'] = new_coords[1] + 1 / 2
                    List_anndatas.append(adata_ij)
        return List_anndatas

    def _find_best_view(self, real, sim, angle, gridsize_to_optimize, noCT=False, benchmark='CTD'):
        number_of_rotations = int(360 / angle)
        results = []
        simulation_views = self._resize_rotations_and_flip(sim, angle)
        grid_real = _grid_transform(real, CTD=noCT, gridsize=gridsize_to_optimize, show=False)
        for sim_view in tqdm(simulation_views):
            grid_sim = _grid_transform(sim_view, CTD=noCT, gridsize=gridsize_to_optimize, show=False)
            full, partial = self._spatial_similarity_benchmark(df_real=grid_real, df_sim=grid_sim, benchmark=benchmark)
            results.append(partial[0])
        array_results = np.array(results)
        best_score = np.max(array_results)
        best_view = np.argmax(array_results).astype(int)
        best_flip = (best_view // number_of_rotations).astype(int)
        best_angle = (best_view % number_of_rotations) * angle
        worst_score = np.min(array_results)
        worst_view = np.argmin(array_results).astype(int)
        worst_flip = (worst_view // number_of_rotations).astype(int)
        worst_angle = (worst_view % number_of_rotations) * angle
        B = [best_score, best_flip, best_angle]
        W = [worst_score, worst_flip, worst_angle]
        return B, W, simulation_views[best_view], simulation_views[worst_view]

    def _run_for_layers(self, adata_real, adata_sim, show=True, noCTreal=False, noCTsim=False, save=False,
                       save_name='1.pdf', benchmark='CTD', svg_distribution=True, threshold=1, gridsizes=None, save_path=None, real_name='', sim_name='', figsize=5):
        import matplotlib as mpl
        with mpl.rc_context():
            mpl.rcParams['axes.grid'] = False
            if gridsizes is None:
                max_gridsize = int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))
                max_simple_layer_size = int(np.floor(np.log2(adata_real.X.shape[0]) / 2))
                gridsizes = [2 ** i for i in range(max_simple_layer_size + 1)]
                gridsizes.append(max_gridsize)

            if benchmark == 'cell_type_distribution':
                benchmark_name = 'CTD'
            elif benchmark == 'SVG':
                benchmark_name = 'SVG'

            L=len(gridsizes)
            rows=int(np.ceil(L / 3))
            colnum = min(L, 3)
            fig, axes = plt.subplots(rows, colnum, figsize=(1+figsize*(colnum+1), 0.3+rows*figsize))
            axes = np.array(axes)
            if rows == 1:
                axes = np.expand_dims(axes, axis=0)
            for l, gridsize in enumerate(gridsizes):
                grid_real = _grid_transform(adata=adata_real, CTD=noCTreal, gridsize=gridsize, show=False, SVGD=svg_distribution)
                grid_sim = _grid_transform(adata=adata_sim, CTD=noCTsim, gridsize=gridsize, show=False, SVGD=svg_distribution)
                full, partial = self._spatial_similarity_benchmark(df_real=grid_real, df_sim=grid_sim, benchmark=benchmark)
                score1 = full[1][0]
                score2 = full[3][0]
                k = int(grid_real.X.shape[0] ** (1 / 2)) - 2
                cmap1 = 'plasma'
                start_color2 = (131 / 255, 221 / 255, 236 / 255)
                end_color2 = (146 / 255, 231 / 255, 155 / 255)
                cmap2 = LinearSegmentedColormap.from_list('new', [start_color2, end_color2])
                values1 = np.empty((k, k))
                values2 = np.empty((k, k))
                for j in range(k):
                    for i in range(k):
                        values1[i, j] = score1[i + j * k]
                        values2[i, j] = score2[i + j * k]
                if colnum == 1:
                    g3 = axes[l].imshow(values1.T, cmap=cmap1, origin='lower', extent=[0, 1, 0, 1], vmin=0, vmax=1)
                    g4 = axes[l].imshow(values2.T, cmap=cmap2, origin='lower', extent=[0, 1, 0, 1], vmin=0, vmax=1)
                    axes[l].tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
                    #axes[l].tick_params(axis='both', which='major', labelsize=3*figsize)
                    axes[l].set_title(f"{benchmark_name} Overlap DSC: " + str(
                        self._trunc(partial[0], decs=2)) + "\n" + f"{benchmark_name} Region Mean DSC: " + str(
                        self._trunc(partial[1], decs=2)) + "\n" + "Structure DSC: " + str(self._trunc(partial[2], decs=2)), fontsize=2.5*figsize, weight="bold")
                else:
                    g3 = axes[l // 3, l % colnum].imshow(values1.T, cmap=cmap1, origin='lower', extent=[0, 1, 0, 1], vmin=0, vmax=1)
                    g4 = axes[l // 3, l % colnum].imshow(values2.T, cmap=cmap2, origin='lower', extent=[0, 1, 0, 1], vmin=0, vmax=1)
                    axes[l // 3, l % colnum].tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
                    #axes[l // 3, l % colnum].tick_params(axis='both', which='major', labelsize=3*figsize)
                    axes[l // 3, l % colnum].set_title(f"{benchmark_name} Overlap DSC: " + str(
                        self._trunc(partial[0], decs=2)) + "\n" + f"{benchmark_name} Region Mean DSC: " + str(
                        self._trunc(partial[1], decs=2)) + "\n" + "Structure DSC: " + str(self._trunc(partial[2], decs=2)), fontsize=2.5*figsize, weight="bold")
            for i in range(L, rows * 3):
                if colnum > 1:
                    row = i // 3
                    col = i % colnum
                    axes[row, col].axis('off')
            black_patch = mpatches.Patch(color=start_color2, label='Only Sim Cells')
            blue_patch = mpatches.Patch(color=end_color2, label='Only Real Cells')
            white_patch = mpatches.Patch(facecolor='white', edgecolor='black', label='No Cells')
            cbar = fig.colorbar(g3, ax=axes, shrink=1, aspect=10, orientation='vertical', pad=0.02)
            cbar.set_label('DSC', fontsize=4.5*figsize, labelpad=20, rotation=0, weight="bold")
            cbar.ax.yaxis.set_label_position('left')
            cbar.ax.yaxis.set_label_coords(0.5, 1)
            fig.legend(handles=[blue_patch, black_patch, white_patch], loc='center right', fontsize=3.5*figsize, handleheight=2.5,
                       handlelength=2.5, prop={'size': 3.5*figsize, 'weight': 'bold'})
            if colnum == 1:
                fig.suptitle(f'{benchmark_name}  Similarity Analysis \nReal: {real_name}\nSim: {sim_name}',
                             fontsize=5*figsize, weight='bold',
                             x=0.75,
                             y=1.1,
                             ha='center')
            elif colnum == 2:
                fig.suptitle(f'{benchmark_name}  Similarity Analysis \nReal: {real_name}\nSim: {sim_name}',
                             fontsize=5*figsize, weight='bold',
                             x=0.5,
                             y=1.1,
                             ha='center')
            elif colnum == 3:
                fig.suptitle(f'{benchmark_name}  Similarity Analysis \nReal: {real_name}\nSim: {sim_name}',
                             fontsize=5*figsize, weight='bold',
                             x=0.5,
                             y=1.1,
                             ha='center')
            else:
                fig.suptitle(f'{benchmark_name}  Similarity Analysis \nReal: {real_name}\nSim: {sim_name}',
                             fontsize=5*figsize, weight='bold',
                             x=0.5,
                             y=1.1,
                             ha='center')
            if save:
                if benchmark_name == 'SVG':
                    filename = f"{save_name}_{benchmark_name}_threshold_{threshold}_svg_distribution_{svg_distribution}_real_{real_name}_sim_{sim_name}.png"
                    full_path = os.path.join(save_path, filename)
                    plt.savefig(full_path, format='png', bbox_inches='tight')
                else:
                    filename = f"{save_name}_{benchmark_name}_real_{real_name}_sim_{sim_name}.png"
                    full_path = os.path.join(save_path, filename)
                    plt.savefig(full_path, format='png', bbox_inches='tight')
            if show:
                plt.show()
                plt.close()
            else:
                plt.close()