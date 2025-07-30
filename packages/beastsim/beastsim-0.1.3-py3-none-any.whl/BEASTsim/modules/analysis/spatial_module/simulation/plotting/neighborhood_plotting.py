import os
import matplotlib.pyplot as plt
from pandas import Series
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from BEASTsim.beast_data import *
from BEASTsim.utils.utils import _square_normalize, _add_svg_matrix, _grid_transform

parameters_path = "BEASTsim/parameters.json"

class NeighborhoodPlotting:
    def __init__(self, parameters):
        self.parameters = parameters
        self.spatial_bio_signals_parameters = self.parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]["SpatialBiologicalSignals"]
        self.spatial_analysis_parameters = self.parameters["Analysis"]["Spatial"]
        self.dir = self.spatial_analysis_parameters["output"]

    def run_plot_neighbourhood(self, real: BEAST_Data, sim: BEAST_Data, save_name='neighbourhood_plot', force_categorical=False, gridsize=32, order=False,
                               show=False, save=True, check_for_voxelized=False, save_path = None, two_sample = True, use_dice_scores=True, use_chi2_scores=True, threshold=5):
        """
        Comperative grid based analysis of conditional neighborhood cell type distribution of regions in real and simulated data.
        Visualized as heatmap plots of the calculated conditional probability distribution matrix, row-wise comparison scores and statistical test p-values (χ²-test).

        Parameters
        ----------
        real : BEAST_Data
            Input we consider as the real data to analyze and compare with the simulated data.
        sim : BEAST_Data
            Input we consider as the simulated data to analyze and compare with the real data.
        save_name : str, default "neighbourhood_plot"
            String parameter setting the name prefix saved output files will start with, in case `save` was set to `True`.
        force_categorical : bool, default False
            If `True`, for both real and simulated data `adata.obs["cell_type"]` categories will be considered the cell
            types aggregated by the grid transformation into a distribution for each region and used in further steps.
            If `False`, for both real and simulated data `adata.obsm["cell_type_distributions"]` will be aggregated by
            the grid transformation into regional average distributions and used in further steps.
        gridsize : int, default 32
            Chooses the density of the grid partition for the grid transformation step, if `None`,
            the grid size will be determined based on the number of cells in the real data according to the following
            formula `int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))`.
        order : bool, default False
            If `True`, rows (cell types) are ordered according to their abundance in the real tissue, decreasing top to bottom.
            This option is only effecting the visualization, adds additional interpretability to the results, but
            the same rows are being compared as before and the same scores are calculated.
        show : bool, default False
            Indicating if we want to show the created plots interactively.
        save : bool, default True
            Indicating if we want to save the created plots at the set path.
        check_for_voxelized : bool, default False
            If `True` and for both real and simulated data the `adata.uns["voxelized_subdata"]` anndata part exists,
            then those will be the datasets analyzed and compared instead of the outside anndata object.
            If either subdata doesn't exist, then it defaults to the outside object.
            If `False`, the `adata.uns["voxelized_subdata"]` is disregarded even if it exists. The rest of the
            parameters refer to the real and simulated datasets picked in this step.
        save_path : Optional[str], default self.dir
            Path string parameter pointing to where we want to save the created plots, in case `save` was set to `True`.
            If set to `None`, the default path from the `parameters.json` file will be used at
            `self.parameters["Analysis"]["Spatial"]["output"]`
        two_sample : bool, default True
            If `True`, the two-sample Chi-squared test is performed, otherwise the calculated probabilities for the
            `real` data is considered as the ground truth distribution for the one-sample test.
        use_dice_scores : bool, default True
            If `True`, rows of the conditional distribution matrices are compared using the continuous dice score and
            plotted on the right side of the plot.
        use_chi2_scores : bool, default True
            If `True`, rows of the conditional distribution matrices are compared using the Chi-squared statistical test,
            taking into account the differing sample sizes for each cell type.
            The p-values from the test are plotted on the right side of the plot colored using a logarithmic color range
            but showing the actual p-values.
            This test is much stricter on distributional differences between the neighborhoods than the dice score.
            This test is better applicable to high similarity simulations but less interpretable for reference-free
            methods and highly dissimilar cases.
        threshold : float, default 5
            The Chi-squared test can only be applied if there were observed samples in every category, and is generally
            more accurate when a decent number of samples are observed from every category,
            therefore the `threshold` parameter is used to group together or in extreme cases remove sparse categories
            according to sample abundance in the real tissue,
            therefore achieving a more accurate test. (e.g. if `threshold = 5`, we force for all i `p_i > 5/N`)
        Returns
        -------
        (The function might save and/or show the generated plots but otherwise has no returns)
        """
        adata_real = real.data
        adata_real_name = real.name
        adata_sim = sim.data
        adata_sim_name = sim.name
        if save_path is None:
            save_path =  self.dir
        used_voxelized = False
        if check_for_voxelized:
            if "voxelized_subdata" in adata_real.uns and "voxelized_subdata" in adata_sim.uns:
                q_val_real = adata_real.var['q_val']
                adata_real = adata_real.uns["voxelized_subdata"]
                adata_real.var['q_val'] = q_val_real
                if 'gene_id' not in adata_real.var.columns:
                    adata_real.var['gene_id'] = adata_real.var.index
                used_voxelized = True
            else:
                Warning('No voxelized real data was found, defaulting to outside dataset.')
                adata_real = adata_real
            if "voxelized_subdata" in adata_sim.uns:
                q_val_sim = adata_sim.var['q_val']
                adata_sim = adata_sim.uns["voxelized_subdata"]
                adata_sim.var['q_val'] = q_val_sim
                if 'gene_id' not in adata_sim.var.columns:
                    adata_sim.var['gene_id'] = adata_sim.var.index
                used_voxelized = True
            else:
                Warning('No voxelized simulated data was found, defaulting to outside dataset.')
                adata_sim = adata_sim
        if gridsize is None:
            gridsize = int(np.floor(2 ** (np.log2(adata_real.X.shape[0]) / 2)))
        adata_real = self._set_CTD_from_probabilities(adata_real)
        adata_sim = self._set_CTD_from_probabilities(adata_sim)
        adata_real, adata_sim = _add_svg_matrix(adata_real, adata_sim, genes=None, intersect_genes=True) #TODO remove these dummy calculations
        adata_real = _square_normalize(adata_real, scale=1)
        adata_sim = _square_normalize(adata_sim, scale=1)
        grid_real = _grid_transform(adata_real, CTD=force_categorical, gridsize=gridsize, show=False, SVGD=True)
        grid_sim = _grid_transform(adata_sim, CTD=force_categorical, gridsize=gridsize, show=False, SVGD=True)
        full, partial = self._calculate_cell_type_neighborhood(grid_real, grid_sim, number_of_cells=True, alpha=0.05,
                                                               two_sample=two_sample, use_dice_scores=use_dice_scores,
                                                               use_chi2_scores=use_chi2_scores, threshold=threshold)
        self._neighbourhood_plot(Full_List=full, show=show, save=save, save_name=save_name, order=order, save_path=save_path,
                                 gridsize = gridsize, used_voxelized = used_voxelized, forceCategorical=force_categorical,
                                 use_dice_scores=use_dice_scores, use_chi2_scores=use_chi2_scores, two_sample = two_sample, threshold=threshold, real_name=adata_real_name, sim_name=adata_sim_name)

    # Works only with anndata outputs of the 'grid_transform' function
    @staticmethod
    def _calculate_cell_type_neighborhood(adata_real: AnnData, adata_sim: AnnData, number_of_cells: bool =True,
                                          alpha: float =0.05, two_sample: bool=True, use_dice_scores=True,
                                          use_chi2_scores=True, result_order=False, threshold=1) -> tuple[list, Series]:
        """
        For a spatial dataset calculates the matrix
        P(A neighbour of random region R has cell type k | random region R has cell type m) for all combinations k,m
        For a spatial dataset calculates the matrix
        P(A neighbour of random region R is empty/non-empty | random region R has cell type m) for all combinations empty/non-empty, m
        Calculates the above for `adata_real`, `adata_sim`
        Calculates Dice score between the rows of above two matrix for both cases
        Calculates Chi squared test statistic and p-value comparing rows of the above two matrix for both cases
        Calculates average Dice score, Chi squared test results across rows for both cases

        Args:
            adata_real (AnnData): Grid transformed Real spatial transcriptomics dataset
            adata_sim (AnnData): Grid transformed Simulated spatial transcriptomics dataset
            number_of_cells (bool, optional): If True, individual probabilities are weighted by cell counts inside regions.
                                              If False, uniform weights are used. Defaults to True.
            alpha (float, optional): Significance level for Chi-square tests. Defaults to 0.05.
            two_sample (bool, optional): Indicates whether to use a two-sample Chi-square test.
                                         Defaults to True.
            use_dice_scores : bool, default True
                Include Dice scores in the output lists / plotting Series.
            use_chi2_scores : bool, default True
                Include χ² statistics and binary accept/reject test results in the output.
            result_order : bool, default False
                If True, re-order rows/columns by abundance before returning
            threshold : int, default 1
                Minimum expected count per category when computing χ²; sparse
                categories are merged or removed.

        Returns
        -------
        tuple[list, pandas.Series]
            full_list
                ``[[CT_chi2, CT_dice, ET_chi2, ET_dice],
                  [CT_real, ET_real, CT_sim, ET_sim]]`` where each element
                contains the raw matrices, per-row scores, means, and ordering. Everything necessary to
                reconstruct the plots
            plotting_series
                Series whose index contains the selected averaged metric names
                (“CellType_Neighborhood_DSC”, “Empty_Neighborhood_CHI2”, …) and
                whose values are the corresponding averaged scores.
        """
        from numpy import sum, newaxis, zeros, ones, outer, argsort, mean, absolute, array
        from scipy.stats import chi2
        CTD_real, CTD_sim = adata_real.obsm['cell_type_distribution'], adata_sim.obsm['cell_type_distribution']
        ETD_real, ETD_sim = adata_real.obsm['ETD'], adata_sim.obsm['ETD']
        neighbours_real, neighbours_sim = adata_real.obsm['neighbours'], adata_sim.obsm[
           'neighbours']
        cell_counts_real, cell_counts_sim = adata_real.obs['cell_counts'].values, adata_sim.obs[
           'cell_counts'].values
        k = adata_real.k
        gridsize = k + 2
        inregion_coordinates = [[i + 1, j + 1] for j in range(k) for i in range(k)]
        inregion_indices = array([c[0] + gridsize * c[1] for c in inregion_coordinates])
        m = CTD_real.shape[1] - 1

        def get_inregion_CTD(CTD): # TODO: Are we even using this?
           inregion_CTD = array([CTD[i, 0:m] for i in inregion_indices])
           return inregion_CTD

        def _get_inregion_parameters(index, neighbours, CTD1, CTD2, region_choose_probs,
                                   region_neighbour_choose_probs):
           choose_prob = region_choose_probs[index]
           distrib = CTD1[index]
           neighbour_choose_probs = region_neighbour_choose_probs[index]
           neighbour_CTDs = array([CTD2[l] for l in neighbours[index]])
           return choose_prob, distrib, neighbour_choose_probs, neighbour_CTDs

        def _get_choose_probs(neighbours, cell_counts): # TODO: Rename
           region_choose_probs = cell_counts * 1 / sum(cell_counts)
           temp_inregion_indices = inregion_indices.copy()
           inregion_neighbour_counts = array(
               [[cell_counts[l] for l in neighbours[i]] for i in temp_inregion_indices])
           temp_inregion_indices = temp_inregion_indices[sum(inregion_neighbour_counts, axis=1) > 0]
           inregion_neighbour_counts = inregion_neighbour_counts[sum(inregion_neighbour_counts, axis=1) > 0]
           inregion_neighbour_choose_probs = inregion_neighbour_counts * (1 / sum(inregion_neighbour_counts,
                                                                                     axis=1))[:, newaxis]
           region_neighbour_choose_probs = zeros((gridsize ** 2, 8))
           region_neighbour_choose_probs[temp_inregion_indices] = inregion_neighbour_choose_probs
           return region_choose_probs, region_neighbour_choose_probs

        def _calc(CTD1, CTD2, neighbours, cell_counts, ET=False, number_of_cells=True): # TODO: Rename
           if ET:
               if number_of_cells:
                   region_choose_probs, _ = _get_choose_probs(neighbours, cell_counts)
               else:
                   region_choose_probs = ones(gridsize ** 2) * 1 / k ** 2
               region_neighbour_choose_probs = ones((gridsize ** 2, 8)) * 1 / 8
           else:
               if number_of_cells:
                   region_choose_probs, region_neighbour_choose_probs = _get_choose_probs(neighbours, cell_counts)
               else:
                   region_choose_probs, region_neighbour_choose_probs = ones(
                       gridsize ** 2) * 1 / k ** 2, ones((gridsize ** 2, 8)) * 1 / 8
           num = zeros((CTD1.shape[1], CTD2.shape[1]))
           denom = zeros(CTD1.shape[1])
           for index in inregion_indices:
               choose_prob, distrib, neighbour_choose_probs, neighbour_CTDs =\
                   _get_inregion_parameters(index,neighbours, CTD1, CTD2,
                                             region_choose_probs, region_neighbour_choose_probs)
               ct_hat_star = sum(neighbour_CTDs * neighbour_choose_probs[:, newaxis], axis=0)
               ct_hat = distrib * choose_prob
               num += outer(ct_hat, ct_hat_star)
               denom += ct_hat
           result = num * 1 / denom[:, newaxis]
           order = argsort(-denom * sum(cell_counts))
           if result_order:
               result = result[order]
               if not ET:
                   result = result[:, order]
           return result, denom * sum(cell_counts), num * sum(cell_counts), order

        CT_benchmark_real, denom_CT_real, num_CT_real, order_CT_real = _calc(
           CTD1=CTD_real[:, 0:m], CTD2=CTD_real[:, 0:m], neighbours=neighbours_real,
           cell_counts=cell_counts_real, number_of_cells=number_of_cells)
        ET_benchmark_real, denom_ET_real, num_ET_real, order_ET_real = _calc(
           CTD1=CTD_real[:, 0:m], CTD2=ETD_real, neighbours=neighbours_real,
           cell_counts=cell_counts_real, ET=True, number_of_cells=number_of_cells)
        CT_benchmark_sim, denom_CT_sim, num_CT_sim, order_CT_sim = _calc(
           CTD1=CTD_sim[:, 0:m], CTD2=CTD_sim[:, 0:m], neighbours=neighbours_sim,
           cell_counts=cell_counts_sim, number_of_cells=number_of_cells)
        ET_benchmark_sim, denom_ET_sim, num_ET_sim, order_ET_sim = _calc(
           CTD1=CTD_sim[:, 0:m], CTD2=ETD_sim, neighbours=neighbours_sim,
           cell_counts=cell_counts_sim, ET=True, number_of_cells=number_of_cells)

        def _dice_score(p, q, pi=2):
           numerator = sum(absolute(p - q) ** pi, axis=1)
           denominator = sum(p ** pi, axis=1) + sum(q ** pi, axis=1)
           score = 1 - (numerator * 1 / denominator)
           mean_score = mean(score)
           return score, mean_score

        def _chisq_rows(p, q, alpha=0.05, Np=1000, Nq=1000, two_sample=True, threshold=1):
            rare_p = p < threshold / Np
            abundant_p = p >= threshold / Np
            if np.sum(rare_p) != 0:
                if np.sum(p[rare_p]) < 1 / Np:
                    p_effective = p[abundant_p] / np.sum(p[abundant_p])
                    q_effective = q[abundant_p] / np.sum(q[abundant_p])
                    Np = np.sum(p[abundant_p])*Np
                    Nq = np.sum(q[abundant_p])*Nq
                    dgf_effective = len(p_effective)
                else:
                    p_effective = np.empty(len(p[abundant_p]) + 1)
                    q_effective = np.empty(len(p[abundant_p]) + 1)
                    p_effective[0:len(p[abundant_p])] = p[abundant_p]
                    q_effective[0:len(q[abundant_p])] = q[abundant_p]
                    p_effective[-1] = np.sum(p[rare_p])
                    q_effective[-1] = np.sum(q[rare_p])
                    dgf_effective = len(p_effective)
            else:
                p_effective = p
                q_effective = q
                dgf_effective = len(p_effective)
            #if np.sum(p_effective) > 1 + 10**(-18) or np.sum(p_effective) < 1 - 10**(-18):
            #    print(np.sum(p_effective))
            if two_sample:
                E_p = Np*(p_effective*Np+q_effective*Nq)/(Np+Nq)
                E_q = Nq*(p_effective*Np+q_effective*Nq)/(Np+Nq)
                stat = np.sum((p_effective*Np - E_p)**2 * 1/E_p) + np.sum((q_effective*Nq - E_q)**2 * 1/E_q)
                c = 1
            else:
                stat = Nq * sum(((p_effective - q_effective) ** 2) / p_effective)
                c = 1
            quantile = chi2.ppf(1 - alpha, dgf_effective - c, loc=0, scale=1)
            if stat > quantile:
                res = 0
            else:
                res = 1
            pval = chi2.sf(stat, dgf_effective - c, loc=0, scale=1)
            return pval, res, stat

        def _chisq_score(real_condProb, sim_condProb, N_real, N_sim, alpha=0.05, two_sample=True, threshold=1):
           M = [[], [], [], [], []]
           for i in range(m):
               pval, res, stat = _chisq_rows(real_condProb[i], sim_condProb[i], alpha=alpha, Np=N_real[i],
                                                 Nq=N_sim[i], two_sample=two_sample, threshold=threshold)
               M[0].append(res)
               M[1].append(pval)
               M[2].append(stat)
           mean_M = sum(M[0]) / m
           return M, mean_M

        CT_chi2_scores, CT_chi2_score_mean = _chisq_score(CT_benchmark_real,
                                                                       CT_benchmark_sim, denom_CT_real,
                                                                       denom_CT_sim, alpha=alpha,
                                                                       two_sample=two_sample, threshold=threshold)
        CT_dice_scores, CT_dice_score_mean = _dice_score(CT_benchmark_real, CT_benchmark_sim)
        ET_chi2_scores, ET_chi2_score_mean = _chisq_score(ET_benchmark_real,
                                                                       ET_benchmark_sim, denom_ET_real,
                                                                       denom_ET_sim, alpha=alpha,
                                                                       two_sample=two_sample, threshold=threshold)
        ET_dice_scores, ET_dice_score_mean = _dice_score(ET_benchmark_real,ET_benchmark_sim)

        full_list = [[[CT_chi2_scores, CT_chi2_score_mean], [CT_dice_scores, CT_dice_score_mean],
                     [ET_chi2_scores, ET_chi2_score_mean], [ET_dice_scores, ET_dice_score_mean]],
                    [[CT_benchmark_real, order_CT_real],[ET_benchmark_real, order_ET_real],
                     [CT_benchmark_sim, order_CT_sim], [ET_benchmark_sim, order_ET_sim]]]
        plotting_list = []
        names = []
        if use_dice_scores:
            plotting_list.extend([CT_dice_score_mean, ET_dice_score_mean])
            names.extend(["CellType_Neighborhood_DSC", "Empty_Neighborhood_DSC"])
        if use_chi2_scores:
            plotting_list.extend([CT_chi2_score_mean, ET_chi2_score_mean])
            names.extend(["CellType_Neighborhood_CHI2", "Empty_Neighborhood_CHI2"])
        plotting_df = Series(plotting_list, index=names)
        return full_list, plotting_df

    def _add_numbers(self, ax, matrix):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if abs(matrix[i, j]) < 0.01 and matrix[i, j] != 0:
                    ax.text(j, i, f"{matrix[i, j]:.0e}", ha="center", va="center", color="green", fontsize=14,
                            weight="bold")
                else:
                    ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="green", fontsize=14,
                            weight="bold")

    def _set_CTD_from_probabilities(self, adata):
        if 'probabilities' in adata.obsm:
            adata.obsm['CTD'] = adata.obsm['probabilities']
        elif 'cell_type_distribution' in adata.obsm:
            adata.obsm['CTD'] = adata.obsm['cell_type_distribution']
        return adata

    def _neighbourhood_plot1(self, Full_List, show=False, save=True,
                            save_name='neighbourhood_plot', order=False, save_path=None, gridsize = None,
                            used_voxelized = None, forceCategorical=None, use_dice_scores=True,
                            use_chi2_scores=True, two_sample = True, threshold=1, real_name='', sim_name=''):
        (chi2_CT, chi2_CT_mean), (dice_CT, dice_CT_mean), \
            (chi2_ET, chi2_ET_mean), (dice_ET, dice_ET_mean) = Full_List[0]
        (mat_CT_real, order_CT_real), (mat_ET_real, order_ET_real), \
            (mat_CT_sim, order_CT_sim), (mat_ET_sim, order_ET_sim) = Full_List[1]
        if order:
            mat_CT_real = mat_CT_real[order_CT_real]
            mat_CT_real = mat_CT_real[:,order_CT_real]
            mat_CT_sim = mat_CT_sim[order_CT_real]
            mat_CT_sim = mat_CT_sim[:,order_CT_real]
            matrices = [mat_CT_real, mat_CT_sim, mat_ET_real[order_CT_real], mat_ET_sim[order_CT_real]]
            matrix5_list = []
            labels_scores = []
            if use_dice_scores:
                matrix5_list.append(Full_List[0][1][0][order_CT_real])
                matrix5_list.append(Full_List[0][3][0][order_CT_real])
                labels_scores.append('CTdsc')
                labels_scores.append('ETdsc')
            if use_chi2_scores:
                matrix5_list.append(np.array(chi2_CT[1])[order_CT_real])
                matrix5_list.append(np.array(chi2_ET[1])[order_CT_real])
                labels_scores.append('CTchi2')
                labels_scores.append('ETchi2')
            matrix5 = np.vstack(matrix5_list).T
        else:
            matrices = [mat_CT_real, mat_CT_sim, mat_ET_real, mat_ET_sim]
            matrix5_list = []
            labels_scores = []
            if use_dice_scores:
                matrix5_list.append(Full_List[0][1][0])
                matrix5_list.append(Full_List[0][3][0])
                labels_scores.append('CTdsc')
                labels_scores.append('ETdsc')
            if use_chi2_scores:
                matrix5_list.append(np.array(chi2_CT[1]))
                matrix5_list.append(np.array(chi2_ET[1]))
                labels_scores.append('CTchi2')
                labels_scores.append('ETchi2')
            matrix5 = np.vstack(matrix5_list).T
        titles = ['CT Real', 'CT Sim', 'ET Real', 'ET Sim']
        m = mat_CT_real.shape[0]
        labels_ct = np.array([f'CT{i + 1}' for i in range(m)])
        ordered_labels_ct = np.array([f'CT{order_CT_real[i] + 1}' for i in range(m)])
        labels_et = ['!E', 'E']
        fig = plt.figure(figsize=(2 * m + 2 + len(labels_scores)*2, m + 1)) #10, 6
        gs = gridspec.GridSpec(1, 5, width_ratios=[m, m, 2, 2, len(labels_scores)]) #2,4
        axes = [fig.add_subplot(gs[0, idx]) for idx in range(5)]
        for ax, mat, ttl in zip(axes[:4], matrices, titles):
            im = ax.imshow(mat, cmap='plasma', vmin=0, vmax=1)
            ax.set_title(ttl, fontsize=int(2*m), weight='bold')
            self._add_numbers(ax, mat)
        im5 = axes[4].imshow(matrix5, cmap='plasma', vmin=0, vmax=1)
        axes[4].set_title('Scores', fontsize=int(2*m), weight='bold')
        self._add_numbers(axes[4], matrix5)
        def set_ticks(ax, x_ticks, x_labels, y_labels):
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, fontsize=12, weight='bold')
            ax.set_yticks(np.arange(len(y_labels)))
            ax.set_yticklabels(y_labels, fontsize=12, weight='bold')
            ax.xaxis.set_ticks_position('top')
        for idx, ax in enumerate(axes):
            if idx < 2:
                xt = np.arange(m)
                xl = ordered_labels_ct if order else labels_ct
                set_ticks(ax, xt, xl, xl)
            elif idx < 4:
                xt = np.arange(2)
                yl = ordered_labels_ct if order else labels_ct
                set_ticks(ax, xt, labels_et, yl)
            else:
                xt = np.arange(len(labels_scores)) #2,4
                yl = ordered_labels_ct if order else labels_ct
                set_ticks(ax, xt, labels_scores, yl)
        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.69])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.ax.tick_params(labelsize=16)
        title = (
            f'CT Neighbourhood Analysis'
        )
        fig.suptitle(title, fontsize=4*m, weight='bold', y=0.92)
        if save:
            path = os.path.join(save_path,
                                f"NeighbourhoodBenchmark_{save_name}_gridsize_{gridsize}_used_voxelized_{used_voxelized}_abundance_ordered_{order}_forceCategorical_{forceCategorical}_two_sample_{two_sample}_use_dice_scores_{use_dice_scores}_use_chi2_scores_{use_chi2_scores}_threshold_{threshold}_real_{real_name}_sim_{sim_name}.png")
            plt.savefig(path, format='png', bbox_inches='tight')
        if show:
            plt.show()
        else:
            plt.close(fig)

    def _neighbourhood_plot(
            self,
            Full_List,
            show=False,
            save=True,
            save_name='neighbourhood_plot',
            order=False,
            save_path=None,
            gridsize=None,
            used_voxelized=None,
            forceCategorical=None,
            use_dice_scores=True,
            use_chi2_scores=True,
            two_sample=True,
            threshold=1,
            real_name='',
            sim_name=''
    ):
        (chi2_CT, chi2_CT_mean), (dice_CT, dice_CT_mean), \
            (chi2_ET, chi2_ET_mean), (dice_ET, dice_ET_mean) = Full_List[0]

        (mat_CT_real, order_CT_real), (mat_ET_real, order_ET_real), \
            (mat_CT_sim, order_CT_sim), (mat_ET_sim, order_ET_sim) = Full_List[1]

        if order:
            mat_CT_real = mat_CT_real[order_CT_real][:, order_CT_real]
            mat_CT_sim = mat_CT_sim[order_CT_real][:, order_CT_real]
            mat_ET_real = mat_ET_real[order_CT_real]
            mat_ET_sim = mat_ET_sim[order_CT_real]
        matrices = [mat_CT_real, mat_CT_sim, mat_ET_real, mat_ET_sim]
        titles = [f'CT Real: {real_name}', f'CT Sim: {sim_name}', 'ET Real', 'ET Sim']

        matrix5_list, labels_scores = [], []

        def _append(arr, lbl):
            matrix5_list.append(arr)
            labels_scores.append(lbl)

        get_arr = (lambda arr: arr[order_CT_real]) if order else (lambda arr: arr)

        if use_dice_scores and use_chi2_scores:
            _append(get_arr(Full_List[0][1][0]), 'CTdsc')
            _append(get_arr(np.array(chi2_CT[1])), 'CTchi2')
            _append(get_arr(Full_List[0][3][0]), 'ETdsc')
            _append(get_arr(np.array(chi2_ET[1])), 'ETchi2')
        elif use_dice_scores:
            _append(get_arr(Full_List[0][1][0]), 'CTdsc')
            _append(get_arr(Full_List[0][3][0]), 'ETdsc')
        elif use_chi2_scores:
            _append(get_arr(np.array(chi2_CT[1])), 'CTchi2')
            _append(get_arr(np.array(chi2_ET[1])), 'ETchi2')

        matrix5 = np.vstack(matrix5_list).T  # shape (m, n_scores)

        m = mat_CT_real.shape[0]
        labels_ct = np.array([f'CT{i + 1}' for i in range(m)])
        ordered_labels_ct = np.array([f'CT{order_CT_real[i] + 1}' for i in range(m)])
        labels_et = ['!E', 'E']

        fig = plt.figure(figsize=(2 * m + 4 + len(labels_scores) * 2,
                                  m + 1))
        gs = gridspec.GridSpec(1, 5,
                               width_ratios=[m, m, 2, 2, len(labels_scores)])
        axes = [fig.add_subplot(gs[0, idx]) for idx in range(5)]

        for ax, mat, ttl in zip(axes[:4], matrices, titles):
            im_real = ax.imshow(mat, cmap='plasma', vmin=0, vmax=1)
            ax.set_title(ttl, fontsize=int(2 * m), weight='bold')
            self._add_numbers(ax, mat)

        ax_scores = axes[4]
        ax_scores.set_title('Scores', fontsize=int(2 * m), weight='bold')

        im_dsc = None
        im_chi2 = None

        for j, lbl in enumerate(labels_scores):
            col = matrix5[:, j].reshape(-1, 1)
            extent = [j - 0.5, j + 0.5, m - 0.5, -0.5]

            if 'chi2' in lbl.lower():
                col = np.clip(col, 1e-5, 1.0)
                im_chi2 = ax_scores.imshow(
                    col,
                    cmap='Blues_r',
                    norm=mpl.colors.LogNorm(vmin=1e-5, vmax=1.0),
                    extent=extent,
                    aspect='auto',
                    interpolation='nearest'
                )
            else:
                im_dsc = ax_scores.imshow(
                    col,
                    cmap='plasma',
                    vmin=0.0,
                    vmax=1.0,
                    extent=extent,
                    aspect='auto',
                    interpolation='nearest'
                )

        ax_scores.set_xlim(-0.5, len(labels_scores) - 0.5)
        ax_scores.set_ylim(m - 0.5, -0.5)
        ax_scores.set_aspect('equal')

        self._add_numbers(ax_scores, matrix5)

        def _set_ticks(ax, x_ticks, x_labels, y_labels):
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, fontsize=12, weight='bold')
            ax.set_yticks(np.arange(len(y_labels)))
            ax.set_yticklabels(y_labels, fontsize=12, weight='bold')
            ax.xaxis.set_ticks_position('top')

        for idx, ax in enumerate(axes):
            if idx < 2:
                xt = np.arange(m)
                xl = ordered_labels_ct if order else labels_ct
                _set_ticks(ax, xt, xl, xl)
            elif idx < 4:
                xt = np.arange(2)
                yl = ordered_labels_ct if order else labels_ct
                _set_ticks(ax, xt, labels_et, yl)
            else:
                xt = np.arange(len(labels_scores))
                yl = ordered_labels_ct if order else labels_ct
                _set_ticks(ax, xt, labels_scores, yl)

        for extra_ax in fig.axes:
            if extra_ax not in axes:
                fig.delaxes(extra_ax)

        if im_dsc is not None:
            cbar_ax_plasma = fig.add_axes([0.92, 0.15, 0.02, 0.69])
            cb_dsc = fig.colorbar(im_dsc, cax=cbar_ax_plasma)
            #cb_dsc.set_label('DSC', rotation=0, labelpad=15, fontsize=16, loc='top', weight='bold')
            cb_dsc.ax.set_title('DSC', fontsize=int(1.5 * m), pad=16, weight='bold')
            cb_dsc.ax.tick_params(labelsize=12)

        if im_chi2 is not None:
            cbar_ax_chi2 = fig.add_axes([0.96, 0.15, 0.02, 0.69])
            cb_chi2 = fig.colorbar(im_chi2, cax=cbar_ax_chi2)
            #cb_chi2.set_label('Chi² p-val', rotation=0, labelpad=18, fontsize=16, loc='top', weight='bold')
            cb_chi2.ax.set_title('Chi²\np-val', fontsize=int(1.5 * m), pad=16, weight='bold')
            cb_chi2.set_ticks([1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5])
            cb_chi2.set_ticklabels(['1', '0.1', '0.01',
                                    '0.001', '0.0001', '≤1e-5'])
            cb_chi2.ax.tick_params(labelsize=16)

        for ax in axes:  # axes you created with GridSpec
            ax.grid(False)

        fig.suptitle('CT Neighbourhood Analysis',
                     fontsize=4 * m, weight='bold', y=0.98)

        if save:
            path = os.path.join(
                save_path,
                f"NeighbourhoodBenchmark_{save_name}"
                f"_gridsize_{gridsize}"
                f"_used_voxelized_{used_voxelized}"
                f"_abundance_ordered_{order}"
                f"_forceCategorical_{forceCategorical}"
                f"_two_sample_{two_sample}"
                f"_use_dice_scores_{use_dice_scores}"
                f"_use_chi2_scores_{use_chi2_scores}"
                f"_threshold_{threshold}_real_{real_name}_sim_{sim_name}.png"
            )
            plt.savefig(path, format='png', bbox_inches='tight')
        if show:
            plt.show()
            plt.close(fig)
        else:
            plt.close(fig)
