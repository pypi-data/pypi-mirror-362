import os

import pandas as pd
from BEASTsim.beast_data import *
import matplotlib.pyplot as plt

class SVGPlotting:
    def __init__(self, parameters):
        self.parameters = parameters
        self.spatial_analysis_parameters = self.parameters["Analysis"]["Spatial"]
        self.dir = self.spatial_analysis_parameters["output"]

    def plot_svg(self, real: BEAST_Data, sim: BEAST_Data, start = 0.001, end=0.5, N=1000, save=True, show=False, save_path=None, save_name=''):
        """
        Plotting the spatial variable gene benchmark dice score between real and simulated tissues, visualized as a function of the alpha significance threshold.
        The parameters `start` and `end` specify the range of significance levels we calculate the benchmark function for while `N` specifies the number of points of the spacing, the range follows a geometric progression.

        Parameters
        ----------
        real : BEAST_Data
            Input we consider as the real data to analyze and compare with the simulated data.
        sim : BEAST_Data
            Input we consider as the simulated data to analyze and compare with the real data.
        start : float, default 0.001
            Lower bound of the α range.
        end : float, default 0.5
            Upper bound of the α range.
        N : int, default 1000
            Number of α points (geometric progression) between *start* and *end*.
        save : bool, default True
            Indicating if we want to save the created plots at the set path.
        show : bool, default False
            Indicating if we want to show the created plots interactively.
        save_path : Optional[str], default self.dir
            Path string parameter pointing to where we want to save the created plots, in case `save` was set to `True`.
             If set to `None`, the default path from the `parameters.json` file will be used at `self.parameters["Analysis"]["Spatial"]["output"]`
        save_name : str, default ""
            Filename prefix for saved files.

        Returns
        -------
        Tuple[list, pandas.DataFrame]
            ``Full_List`` – raw arrays from ``_computeSVGs``
            ``plotting_df`` – α values, SVG counts and benchmark scores.
        """
        adata_real = real.data
        adata_real_name = real.name
        adata_sim = sim.data
        adata_sim_name = sim.name
        if save_path is None:
            save_path = self.dir
        Full_List, plotting_df = self._computeSVGs(adata_real, adata_sim, start = start, end = end, N=N)
        self._plot_2d_function(x = Full_List[3], y = Full_List[4], title=f'SVG Benchmark Significance Variation Plot \nReal: {adata_real_name}\nSim: {adata_sim_name}',
                               xlabel='α', ylabel='SVG Benchmark(α)', save=save, save_path=save_path, show=show, save_name=save_name, real_name=adata_real_name, sim_name=adata_sim_name)

    @staticmethod
    def _computeSVGs(adata_real, adata_sim, alpha=0.05, start = 0.001, end= 0.5, N=1000): #TODO solve to add back  -> tuple(List, pd.Series)
        """
        Compute the Spatially Variable Gene (SVG) similarity between a real and a
        simulated tissue and, optionally, generate a Dice-score curve that shows
        how similarity changes across a range of α significance thresholds.

        --------
        1. Run `SVG_SpatialDE.calc_SVGs` on *adata_real* and *adata_sim* to populate
           `var["q_val"]` with SpatialDE adjusted p-values.
        2. Build a 3 × k array (`full_array`) whose columns contain
           • gene ID,
           • q-value in *real*,
           • q-value in *sim* — for every gene present in either dataset.
           Here *n* = total union of genes; *k* = intersection.
        3. Compute a single Dice score at the chosen significance level *alpha*:
              Dice = 2·|SVG_real ∩ SVG_sim| / (|SVG_real| + |SVG_sim|)
        4. If *start*, *end* and *N* are provided, sweep α over a geometric
           progression for α and return the full curve.

        Parameters
        ----------
        adata_real : AnnData
            Real spatial transcriptomics dataset
        adata_sim : AnnData
            Simulated spatial dataset
        alpha : float, default 0.05
            Significance threshold for the single Dice score.
        start : float, default 0.001
            Upper-end α for the curve (if *start*, *end*, *N* are all not None).
        end : float, default 0.5
            Lower-end α for the curve.
        N : int, default 1000
            Number of α points (geometric spacing) in the curve.

        Returns
        -------
        If *start*, *end*, *N* are all not None
            Tuple[List, pandas.Series]::

                Full_List = [
                    full_array,          # 3 × k gene / q-value table
                    n, k,                # union size, intersection size
                    alpha_vec,           # α values used for the curve
                    dice_vec,            # Dice score at each α
                    single_dice_score    # Dice score at *alpha*
                ]
                plotting_df = pandas.Series(["SVG_DSC"] → single_dice_score)

        Else
            pandas.Series
                Same ``plotting_df`` object (single Dice score only).

        Notes
        -----
        * Dice scores of 0 mean no overlap in SVG gene sets; 1 means perfect match.
        * A warning is printed if neither dataset contains SVGs at the given α.
        """
        from BEASTsim.modules.analysis.spatial_module.SVG.SVG_SpatialDE import SVG_SpatialDE
        def get_full_array(real, sim):
            all_genes = np.unique(np.concatenate((real[0], sim[0])))
            n = len(all_genes)
            intersect = np.intersect1d(real[0], sim[0], return_indices=True)
            full_array = np.vstack((intersect[0], real[1][intersect[1]], sim[1][intersect[2]]))
            k = full_array.shape[1]
            return full_array, n, k

        def binary_test(full_array, alpha=0.05):
            return (full_array[1:3] <= alpha).astype(int)

        def dice_score(full_array, alpha=0.05):
            tested = binary_test(full_array=full_array, alpha=alpha)
            denominator = (np.sum(tested[0]) + np.sum(tested[1]))
            if denominator == 0:
                print('Neither the real nor the simulated data has SVGs')
                return 0  # Avoid division by zero
            result = 2 * np.sum(tested[0] * tested[1]) / denominator
            return (result)

        def dice_plot(full_array, alpha=None, start=0.1, end=0.01, N=10):
            if alpha is None:
                high, low = (start, end) if start > end else (end, start)
                alpha = np.geomspace(high, low, N)
            y = np.array([dice_score(full_array, alpha=a) for a in alpha])
            return alpha, y

        SVG_SpatialDE.calc_SVGs(adata_real)
        SVG_SpatialDE.calc_SVGs(adata_sim)

        genes_real = adata_real.var['q_val'].index.to_numpy()
        genes_sim = adata_sim.var['q_val'].index.to_numpy()
        values_real = adata_real.var['q_val'].values
        values_sim = adata_sim.var['q_val'].values
        GP_real = [genes_real, values_real]
        GP_sim = [genes_sim, values_sim]
        full_array, n, k = get_full_array(GP_real, GP_sim)
        dsc = dice_score(full_array, alpha=alpha)
        plotting_df = pd.Series([dsc], index=["SVG_DSC"])
        if start is not None and end is not None and N is not None:
            print("Calculating SVG benchmark function plot.")
            alpha, y = dice_plot(full_array, start=start, end=end, N=N)
            Full_List = [full_array, n, k, alpha, y, dsc]
            return Full_List, plotting_df
        else:
            return plotting_df

    def _plot_2d_function(self, x, y, title=None, xlabel='x', ylabel='f(x)', grid=True, figsize=(12, 8),
                          color='C0', linewidth=2, save=True, save_path=None, show=True, save_name='',
                          real_name='', sim_name=''):
        plt.style.use('seaborn-v0_8-whitegrid')  # clean default style
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(x, y, color=color, linewidth=linewidth)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        if title:
            ax.set_title(title, fontsize=14, weight='bold')

        if grid:
            ax.grid(True, which='both', linestyle='--', alpha=0.6)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        if save:
            filename = f"{save_name}_svg_plot_real_{real_name}_sim_{sim_name}.png"
            full_path = os.path.join(save_path, filename)
            plt.savefig(full_path, format='png')
        if show:
            plt.show()
            plt.close(fig)
        else:
            plt.close(fig)