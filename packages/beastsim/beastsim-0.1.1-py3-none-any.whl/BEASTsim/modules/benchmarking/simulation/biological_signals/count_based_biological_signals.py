import os, warnings
os.environ["RPY2_CFFI_MODE"] = "ABI"
warnings.filterwarnings("ignore",
                        message="Environment variable \"PATH\" redefined",
                        module="rpy2.rinterface")
from BEASTsim.beast_data import BEAST_Data
from numpy import array, ndarray
from pandas import DataFrame, Series
from statsmodels.stats.multitest import multipletests
import warnings
from typing import List, Optional
import mpmath
from anndata import AnnData
from tqdm import tqdm
# Suppress specific warning
warnings.filterwarnings('ignore', category=UserWarning, message='Transforming to str index.')
mpmath.mp.dps = 50

# TODO: We should call this type of benchmarks something else.
class CountBasedBiologicalSignals:
    def __init__(self, parameters):
        self.parameters = parameters
        self.count_based_bio_signals_parameters = parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]["nonSpatialBiologicalSignals"]


    def run(self, real_data: BEAST_Data, simulated_data: BEAST_Data) -> Series:
        """
        Run **count based biological signals** (DE, DV, DD, DP, BD) of a single
        simulated dataset against the real reference. Calls
        ``count_based_biological_signals_benchmark`` for benchmark calculation and
        returns the stacked SMAPE scores as one Series.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset against which the input simulation will be
            benchmarked.
        simulated_data : BEAST_Data
            Simulated dataset to benchmark.

        Returns
        -------
        pandas.Series
            SMAPE scores for all count-based signal metrics, indexed by benchmark
            name.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        Armstrong, J. S. *Long-Range Forecasting* (Wiley, 1978).
        """
        from pandas import concat
        # TODO potentially add decidability to perform benchmarks on raw MERFISH data
        if 'voxelized_subdata' in real_data.data.uns and 'voxelized_subdata' in simulated_data.data.uns:
            adata_real = real_data.data.uns['voxelized_subdata']
            adata_sim = simulated_data.data.uns['voxelized_subdata']
        elif 'voxelized_subdata' not in real_data.data.uns and 'voxelized_subdata' not in simulated_data.data.uns:
            adata_real = real_data.data
            adata_sim = simulated_data.data
        else:
            ValueError("Data mismatch causes undecidability. Real and simulated data both should or both should not contain .uns['voxelized_subdata'].")

        sim_name = simulated_data.name

        benchmarks = [(self.count_based_biological_signals_benchmark, (adata_real, adata_sim, sim_name)),
                               ]
        results = []

        total_iterations = len(benchmarks)
        with tqdm(
                total=total_iterations, desc="Running Non Spatial Biological Signal Benchmarks", unit="step"
        ) as progress_bar:
            for benchmark_function, args in benchmarks:
                results.append(benchmark_function(*args))
                progress_bar.update(1)

        return concat(results, axis=0)

    def count_based_biological_signals_benchmark(self, adata_real: AnnData, adata_sim: AnnData, sim_name: str) -> Series:
        """
        Compute the full set of count based biological-signal metrics for one
        simulation, save detailed CSV files, and return the SMAPE score vector.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset in raw AnnData format.
        adata_sim : AnnData
            Simulated dataset in raw AnnData format.
        sim_name : str
            Name used in output filenames.

        Returns
        -------
        pandas.Series
            SMAPE scores for the simulation.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        Armstrong, J. S. *Long-Range Forecasting* (Wiley, 1978).
        """
        smape_scores_df, real_scores_df, sim_scores_df = self.compute_count_based_biological_signals(adata_real, adata_sim)

        save_dir = self.parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]["dir"]
        smape_scores_df.to_csv(f"{save_dir}/countBasedBiologicalSignalsBenchmark-SMAPEScores-{sim_name}.csv", index=True, header=True)
        real_scores_df.to_csv(f"{save_dir}/countBasedBiologicalSignalsBenchmark-Real.csv", index=True, header=True)
        sim_scores_df.to_csv(f"{save_dir}/countBasedBiologicalSignalsBenchmark-{sim_name}..csv", index=True, header=True)

        return smape_scores_df

    def get_all_biological_signals(self, adata: AnnData, cell_type_comparison) -> tuple[ndarray, List[str]]:
        """
        Run six statistical tests for biological-signal detection
        (DE_Limma, DE_Scanpy, DV_Bartlett, DD_KS, DP_Chisq, BD) by comparing
        properties of genes in cells with a given cell type against the rest.
        The number of significant genes is divided by the number of genes tested,
        turning them into a proportion.

        Parameters
        ----------
        adata : AnnData
            Count matrix with cell types at ``obs["cell_type"]``.
        cell_type_comparison : Any
            Label of the chosen cell type to be compared against the rest.

        Returns
        -------
        tuple[ndarray, List[str]]
            ``(signals, names)``.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        biological_signal_functions = [
            ("DE_Limma", self.de_limma, (adata, cell_type_comparison)),
            ("DE_Scanpy", self.de_scanpy, (adata, cell_type_comparison)),
            ("DV_Bartlett", self.dv_bartlett, (adata, cell_type_comparison)),
            ("DD_KS", self.dd_ks, (adata, cell_type_comparison)),
            ("DP_Chisq", self.dp_chisq, (adata, cell_type_comparison)),
            ("BD", self.bd, (adata, cell_type_comparison)),
        ]

        biological_signals = []
        names = []
        for key, biological_signal, args in biological_signal_functions:
            results = biological_signal(*args)
            if results is not None:
                tt, exprsMat = results
                biological_signals.append(tt / exprsMat.shape[
                    0])  # We may want to divide by len(tt) here, if we want similar results across different algorithms and choices of parameters
                names.append(key)
        return array(biological_signals), names

    def compute_count_based_biological_signals(self, adata_real: AnnData, adata_sim: AnnData) -> tuple[Series, DataFrame, DataFrame]:
        """
        Iterate over all cell types, calculate the SMAPE score between each
        biological-signal proportion of the input datasets, and aggregate results
        across cell types.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset in raw AnnData format.
        adata_sim : AnnData
            Simulated dataset in raw AnnData format.

        Returns
        -------
        tuple[pandas.Series, pandas.DataFrame, pandas.DataFrame]
            ``(smape_scores, real_scores, sim_scores)``.

        Raises
        ------
        ValueError
            If only one of the datasets contains ``.uns["voxelized_subdata"]`` or
            other required metadata is missing.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        Armstrong, J. S. *Long-Range Forecasting* (Wiley, 1978).
        """
        from numpy import zeros
        from copy import deepcopy
        from pandas import concat
        smape_scores = []
        real_scores = []
        sim_scores = []
        cell_types = adata_real.obs['cell_type'].cat.categories.tolist()
        num_cell_types = len(cell_types)
        #remove rare celltypes, and those cells in both data here (celltype is rare if there are <2 cells from it)
        rare_cell_types_real = set()
        rare_cell_types_sim = set()
        for i in range(num_cell_types):
            cell_type_real = adata_real.obs[adata_real.obs['cell_type'] == cell_types[i]]
            if len(cell_type_real) < 2 :
                rare_cell_types_real.add(cell_types[i])
        for i in range(num_cell_types):
            cell_type_sim = adata_sim.obs[adata_sim.obs['cell_type'] == cell_types[i]]
            if len(cell_type_sim) < 2 :
                rare_cell_types_sim.add(cell_types[i])

        adata_real_filtered = adata_real[~adata_real.obs['cell_type'].isin(rare_cell_types_real)].copy()
        adata_sim_filtered = adata_sim[~adata_sim.obs['cell_type'].isin(rare_cell_types_sim)].copy()

        for i in tqdm(range(num_cell_types)):

            adata_r, adata_s = deepcopy(adata_real_filtered), deepcopy(adata_sim_filtered)

            if (cell_types[i] not in adata_r.obs['cell_type'].values) and (cell_types[i] not in adata_s.obs['cell_type'].values):
                continue
            elif (cell_types[i] in adata_r.obs['cell_type'].values) and (cell_types[i] not in adata_s.obs['cell_type'].values):
                F_t = adata_real.uns.get(f"nonSpatialSignals{i}")
                if F_t is None:
                    F_t, names = self.get_all_biological_signals(adata_r, cell_type_comparison=cell_types[i])
                    if "BiologicalSignalBenchmarks" not in adata_real.uns:
                        adata_real.uns["BiologicalSignalBenchmarks"] = names
                    adata_real.uns[f"nonSpatialSignals{i}"] = F_t
                elif "BiologicalSignalBenchmarks" in adata_real.uns:
                    names = adata_real.uns["BiologicalSignalBenchmarks"]
                else:
                    raise ValueError("adata_real.uns does not have BiologicalSignalBenchmarks")
                n_benchmarks = len(names)
                dataf = {
                    "Real Data": F_t,
                    "Simulated Data": zeros(n_benchmarks),
                    "SMAPE Score": zeros(n_benchmarks)
                }
                biological_signals = DataFrame(dataf, index=names)
                smape_scores.append(biological_signals['SMAPE Score'])
                real_scores.append(biological_signals['Real Data'])
                sim_scores.append(biological_signals['Simulated Data'])
            elif (cell_types[i] not in adata_r.obs['cell_type'].values) and (cell_types[i] in adata_s.obs['cell_type'].values):
                A_t, names = self.get_all_biological_signals(adata_s, cell_type_comparison=cell_types[i])
                dataf = {
                    "Real Data": zeros(n_benchmarks),
                    "Simulated Data": A_t,
                    "SMAPE Score": zeros(n_benchmarks)
                }
                biological_signals = DataFrame(dataf, index=names)
                smape_scores.append(biological_signals['SMAPE Score'])
                real_scores.append(biological_signals['Real Data'])
                sim_scores.append(biological_signals['Simulated Data'])
            else:
                # Perform biological signal calculation
                biological_signals = self.calc_biological_signals(adata_r, adata_s, cell_type_comparison=cell_types[i])
                smape_scores.append(biological_signals['SMAPE Score'])
                real_scores.append(biological_signals['Real Data'])
                sim_scores.append(biological_signals['Simulated Data'])

        smape_scores_df = concat(smape_scores, axis=1)
        smape_scores_df = smape_scores_df.mean(axis=1)
        smape_scores_df.name = "SMAPE Score"

        real_scores_df = concat(real_scores, axis=1)
        sim_scores_df = concat(sim_scores, axis=1)

        real_scores_df.columns = cell_types
        sim_scores_df.columns = cell_types

        return smape_scores_df, real_scores_df, sim_scores_df

    def calc_biological_signals(self, adata_real: AnnData, adata_sim: AnnData, cell_type_comparison) -> DataFrame:
        """
        Compute SMAPE scores for the six biological-signal metrics on the
        specified cell-type comparison and return a tidy DataFrame.

        Parameters
        ----------
        adata_real : AnnData
            Real reference dataset in raw AnnData format.
        adata_sim : AnnData
            Simulated dataset in raw AnnData format.
        cell_type_comparison : int | str
            Cell-type label or index.

        Returns
        -------
        pandas.DataFrame
            Columns ``Real Data``, ``Simulated Data``, ``SMAPE Score``.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        Armstrong, J. S. *Long-Range Forecasting* (Wiley, 1978).
        """
        from numpy import absolute
        def _smape_score() -> tuple[ndarray, ndarray, ndarray, List[str]]:
            F_t = adata_real.uns.get(f"nonSpatialSignals{cell_type_comparison}")
            if F_t is None:
                F_t, names = self.get_all_biological_signals(adata_real, cell_type_comparison=cell_type_comparison)
                adata_real.uns[f"nonSpatialSignals{cell_type_comparison}"] = F_t
                if "BiologicalSignalBenchmarks" not in adata_real.uns:
                    adata_real.uns["BiologicalSignalBenchmarks"] = names

            A_t, names = self.get_all_biological_signals(adata_sim, cell_type_comparison=cell_type_comparison)
            return 1 - (absolute(F_t - A_t) / (F_t + A_t)), F_t, A_t, names
        smape, real, sim, names = _smape_score()
        data = {
            "Real Data": real,
            "Simulated Data": sim,
            "SMAPE Score": smape
        }
        df = DataFrame(data, index=names)
        return df

    def de_limma(self, adata: AnnData, cell_type_comparison) -> Optional[tuple[int, ndarray]]:
        """
        Differential gene-expression analysis via the Limma R package
        (accessed through rpy2). Can be disabled via the ``use_R`` class
        parameter.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all other cell types.

        Returns
        -------
        Optional[tuple[int, ndarray]]
            ``None`` if Limma-based DE analysis is disabled; otherwise
            ``(n_DE_genes, exprs_T)``.

        References
        ----------
        Ritchie M.E. et al. (2015).
        Yue Cao, Pengyi Yang & Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        from os import environ
        from numpy import mean, sum, where
        from copy import deepcopy
        if not self.count_based_bio_signals_parameters["use_R"]:
            return None
        environ['R_HOME'] = self.count_based_bio_signals_parameters["r_home"]
        environ['LANG'] = self.count_based_bio_signals_parameters["r_lang"]
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        import rpy2.robjects as ro
        from rpy2.robjects import numpy2ri, pandas2ri
        from rpy2.robjects.conversion import localconverter

        np_pd_converter = ro.default_converter + numpy2ri.converter + pandas2ri.converter
        n_inf = ro.r('Inf')
        stats = importr('stats')
        limma = importr('limma')

        data = deepcopy(adata)
        exprsMat = data.X.T
        cellTypes = data.obs['cell_type']
        cellTypes = {'cellTypes': cellTypes}
        cellTypes = DataFrame(cellTypes)
        cellTypes['cellTypes'] = cellTypes['cellTypes'].astype('category')
        cellTypes['tmp_celltype'] = where(cellTypes['cellTypes'] == cell_type_comparison, 1, 0)
        cellTypes['intercept'] = 1
        design_matrix = cellTypes[['intercept', 'tmp_celltype']]
        # We only consider a gene in our DE identification if it's expressed in at least 5% (exprs_pct) of cells of the first type (where cellTypes['tmp_celltype'] == 1)
        # Set exprs_pct=0 if don't want this trimming
        meanPct = array([mean(exprsMat[:, cellTypes['tmp_celltype'] == 0] > 0, axis=1),
                            mean(exprsMat[:, cellTypes['tmp_celltype'] == 1] > 0, axis=1)])
        keep = meanPct[1] > self.count_based_bio_signals_parameters["exprs_pct"]
        exprsMat = exprsMat[keep]
        exprsMat = DataFrame(exprsMat)

        with localconverter(np_pd_converter):
            y = ro.conversion.py2rpy(exprsMat)
            design = ro.conversion.py2rpy(design_matrix)
        fit = limma.lmFit(y, design=design)
        fit = limma.eBayes(fit, trend=True, robust=True)
        tt = limma.topTable(fit, n=n_inf, adjust_method="BH", coef=2)
        with localconverter(np_pd_converter):
            tt = ro.conversion.rpy2py(tt)
        tt = sum(tt['adj.P.Val'] < self.count_based_bio_signals_parameters["pval"])
        return tt, adata.X.T

    # Uses the Scanpy (Single-Cell Analysis in Python) package to identify DE genes
    # The original documentation points out that Limma is much more powerful.
    # This is completely in Python
    def de_scanpy(self, adata: AnnData, cell_type_comparison) -> tuple[int, ndarray]:
        """
        Differential gene-expression analysis via the Scanpy package using the
        Wilcoxon rank-sum test on highly variable genes.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all other cell types.

        Returns
        -------
        tuple[int, ndarray]
            ``(n_DE_genes, exprs_T)``.

        References
        ----------
        Wolf, F.A., Angerer, P. & Theis, F.J. (2018).
        """
        from scanpy.preprocessing import normalize_total, log1p, highly_variable_genes
        from scanpy.tools import rank_genes_groups
        from numpy import sum
        from copy import deepcopy

        data = deepcopy(adata)
        index = data.obs['cell_type'].cat.categories.get_loc(cell_type_comparison)
        normalize_total(data, target_sum=1e4)
        log1p(data)
        # Keep only the 50% (highly_variable) most highly variable genes
        # Set highly_variable=1 if want to keep all
        highly_variable_genes(data, n_top_genes=int(data.X.shape[1] * self.count_based_bio_signals_parameters["highly_variable"]), subset=True)
        # sc.pp.scale(adata, max_value=10), This operation seems to mess up the variance calculation by setting a lot of things to 10, best remove it, or modify it if we really want this cap on the scale
        rank_genes_groups(data, 'cell_type',
                                method='wilcoxon')  # Original documentation recommends 'wilcoxon' for research papers
        tt = data.uns['rank_genes_groups']
        pvals_adj = tt['pvals_adj']
        tt = array([t[index] for t in pvals_adj])
        tt = sum(tt < self.count_based_bio_signals_parameters["pval"])
        return tt, adata.X.T

    # Uses the Bartlett’s test for equal variances (using scipy.stats package) to identify DV (Differentially Variable) genes, so genes that show a significant difference in variability across cell types
    # This is completely in Python
    def dv_bartlett(self, adata: AnnData, cell_type_comparison) -> tuple[int, ndarray]:
        """
        Detect differentially variable genes with Bartlett’s test for equal
        variances after filtering lowly expressed genes.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all other cell types.

        Returns
        -------
        tuple[int, ndarray]
            ``(n_DV_genes, exprs_T)``.

        References
        ----------
        Yue Cao, Pengyi Yang & Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        from numpy import mean, sum, where, nan, zeros
        from copy import deepcopy
        from scipy.stats import bartlett
        data = deepcopy(adata)
        exprsMat = data.X.T
        cellTypes = data.obs['cell_type']
        cellTypes = {'cellTypes': cellTypes}
        cellTypes = DataFrame(cellTypes)
        cellTypes['cellTypes'] = cellTypes['cellTypes'].astype('category')
        cellTypes['tmp_celltype'] = where(cellTypes['cellTypes'] == cell_type_comparison, 1, 0)
        meanPct = array([mean(exprsMat[:, cellTypes['tmp_celltype'] == 0] > 0, axis=1),
                            mean(exprsMat[:, cellTypes['tmp_celltype'] == 1] > 0, axis=1)])
        # We only keep genes that are similarly or more usually expressed in type 1 than type 0
        keep = (meanPct[1] - meanPct[0]) > 0.05
        exprsMat = exprsMat[keep, :]
        tt = zeros(exprsMat.shape[0])
        for i in range(exprsMat.shape[0]):
            x = exprsMat[i]
            tmp_celltype_factor = cellTypes['tmp_celltype']

            group1_data = x[tmp_celltype_factor == 0]
            group2_data = x[tmp_celltype_factor == 1]

            try:
                p_value = bartlett(group1_data, group2_data)[1]
                tt[i] = p_value
            except ValueError:
                tt[i] = nan
        tt = multipletests(tt, method='fdr_bh')[1]
        tt = sum(tt < self.count_based_bio_signals_parameters["pval"])
        return tt, adata.X.T

    # Uses the KS test to identify DD (differentially distributed) genes, so genes that are usually expressed in both cell types but more expressed in distribution in one of them, for at least some of the cells in that cell type
    # This is completely in Python
    def dd_ks(self, adata: AnnData, cell_type_comparison) -> tuple[int, ndarray]:
        """
        Identify differentially distributed genes via a one-sided
        Kolmogorov–Smirnov test.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all others.

        Returns
        -------
        tuple[int, ndarray]
            ``(n_DD_genes, exprs_T)``.

        References
        ----------
        Yue Cao, Pengyi Yang & Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        from numpy import mean, sum, where, empty
        from copy import deepcopy
        from scipy.stats import  kstest
        data = deepcopy(adata)
        exprsMat = data.X.T
        cellTypes = data.obs['cell_type']
        cellTypes = {'cellTypes': cellTypes}
        cellTypes = DataFrame(cellTypes)
        cellTypes['cellTypes'] = cellTypes['cellTypes'].astype('category')
        cellTypes['tmp_celltype'] = where(cellTypes['cellTypes'] == cell_type_comparison, 1, 0)
        meanPct = array([mean(exprsMat[:, cellTypes['tmp_celltype'] == 0] > 0, axis=1),
                            mean(exprsMat[:, cellTypes['tmp_celltype'] == 1] > 0, axis=1)])
        keep = (meanPct[1] - meanPct[0]) > 0.05
        exprsMat = exprsMat[keep, :]
        pvals = empty(exprsMat.shape[0])
        for i in range(exprsMat.shape[0]):
            x1 = exprsMat[i][cellTypes['tmp_celltype'] == 0]
            x2 = exprsMat[i][cellTypes['tmp_celltype'] == 1]
            result = kstest(x1, x2, alternative='greater',
                                        method='asymp')  # greater: The null hypothesis is that F(x) <= G(x) for all x; the alternative is that F(x) > G(x) for at least one x.
            pvals[i] = result.pvalue
        tt = multipletests(pvals, method='fdr_bh')[1]
        tt = sum(tt < self.count_based_bio_signals_parameters["pval"])
        return tt, adata.X.T

    # Uses the Chi-Square test of independence to identify DP (Differential proportion) genes, so genes that are more usually expressed (have less zero counts) in one cell type than another.
    # In this test H_0: independence, H_1: dependence.
    # This is completely in Python
    def dp_chisq(self, adata: AnnData, cell_type_comparison, threshold: int = 1) -> tuple[int, ndarray]:
        """
        Use the chi-square test of independence to identify differential-
        proportion (DP) genes—genes that are more frequently expressed in one
        cell type than another.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all others.
        threshold : int, default 1
            Count threshold above which a gene is considered expressed.

        Returns
        -------
        tuple[int, ndarray]
            ``(n_DP_genes, exprs_T)``.

        References
        ----------
        Yue Cao, Pengyi Yang & Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        from numpy import bincount, sum, where
        from copy import deepcopy
        from scipy.stats import chi2_contingency
        data = deepcopy(adata)
        exprsMat = data.X.T
        cellTypes = data.obs['cell_type']
        cellTypes = {'cellTypes': cellTypes}
        cellTypes = DataFrame(cellTypes)
        cellTypes['cellTypes'] = cellTypes['cellTypes'].astype('category')
        cellTypes['tmp_celltype'] = where(cellTypes['cellTypes'] == cell_type_comparison, 1, 0)
        zerosMat = where(exprsMat > threshold, 1, 0)
        p_values = []
        for i in range(zerosMat.shape[0]):
            x = zerosMat[i]
            tab = []
            for cell_type in [0, 1]:
                tmp = x[cellTypes['tmp_celltype'] == cell_type]
                tab.append(bincount(tmp, minlength=2))
            tab = array(tab)
            if not ((tab[0, 0] == 0 and tab[1, 0] == 0) or (tab[0, 1] == 0 and tab[1, 1] == 0)):
                chi2, p, _, _ = chi2_contingency(tab)
                p_values.append(p)
            else:
                p_values.append(1.0)
        adjusted_p_values = multipletests(p_values, method='fdr_bh')[1]
        tt = sum(adjusted_p_values < self.count_based_bio_signals_parameters["pval"])
        return tt, adata.X.T

    # Bimodally distributed genes
    # The output for this function is not a vector of adjusted p-values as for the other ones. Here we calculate the BI (Bimodality index) of each gene between two cell types, where a large BI implies the bimodal nature of the gene.
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2730180/
    # https://cran.r-project.org/web/packages/BimodalIndex/BimodalIndex.pdf
    # This is completely in Python
    def bd(self, adata: AnnData, cell_type_comparison) -> tuple[int, ndarray]:
        """
        Compute the **Bimodality Index (BI)** for every gene and count how many exceed
        the configured threshold, optionally allowing unequal variances between the two
        groups. Identifies bimodally distributed genes between the two cell groups:
        a large BI implies the gene is bimodal.

        Parameters
        ----------
        adata : AnnData
            Input dataset to analyse.
        cell_type_comparison : int | str
            Cell type to compare against all other cell types.

        Returns
        -------
        tuple[int, ndarray]
            (n_BD_genes, exprs_T).

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Lin, Y. et al. (2020).
        """
        from numpy import sqrt, std, mean, bincount, sum, absolute, var, where
        from copy import deepcopy
        data = deepcopy(adata)
        exprsMat = data.X.T
        cell_types = data.obs['cell_type']
        cell_types = {'cell_types': cell_types}
        cell_types = DataFrame(cell_types)
        cell_types['cell_types'] = cell_types['cell_types'].astype('category')
        cell_types['tmp_celltype'] = where(cell_types['cell_types'] == cell_type_comparison, 1, 0)
        p = bincount(cell_types['tmp_celltype'], minlength=2) / len(cell_types['tmp_celltype'])
        type_0 = exprsMat[:, cell_types['tmp_celltype'] == 0]
        type_1 = exprsMat[:, cell_types['tmp_celltype'] == 1]
        mu = array([mean(type_0, axis=1), mean(type_1, axis=1)])
        if self.count_based_bio_signals_parameters["diff_std"]:
            var = array([var(type_0, axis=1), var(type_1, axis=1)])
            den = sqrt(p[0] * var[0] + p[1] * var[1])
            num = sqrt(p[0] * p[1]) * absolute(mu[0] - mu[1])
            bi = num[den != 0] / den[den != 0]
        else:
            std = std(exprsMat, axis=1)
            num = sqrt(p[0] * p[1]) * absolute(mu[0] - mu[1])
            bi = num[std != 0] / std[std != 0]
        tt = sum(bi > self.count_based_bio_signals_parameters["bi_val"])
        return tt, adata.X.T
