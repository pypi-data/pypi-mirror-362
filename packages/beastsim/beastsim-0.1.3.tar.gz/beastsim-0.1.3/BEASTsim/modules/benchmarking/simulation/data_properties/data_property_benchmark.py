from anndata import AnnData
from typing import List, Dict, Union, Optional
from BEASTsim.beast_data import BEAST_Data
from tqdm import tqdm
from BEASTsim.utils.utils_cache import _use_cache
from pandas import DataFrame

class DataPropertyBenchmark:
    def __init__(self, parameters):
        self.parameters = parameters
        self.data_property_parameters = self.parameters["Benchmarking"]["Simulation"]["DataProperties"]

        # Imports
        from BEASTsim.modules.benchmarking.simulation.data_properties.generic_data_properties import GenericDataProperties
        from BEASTsim.modules.benchmarking.simulation.data_properties.kde_data_properties import KDE

        # Modules
        self.generic_data_properties = GenericDataProperties(self.parameters)
        self.kde = KDE(self.data_property_parameters) # TODO: DOUBLE CHECK IF ITS FIXED

        self.NAMES = [
            # genes related
            "mean_expression", "var_expression", "scaled_var_expression", "fraction_zero_genes", "pearson_correlation_genes", "spearman_correlation_genes",
            # cells related
            "lib_size", "effective_lib_size", "TMM", "fraction_zero_cells", "pearson_correlation_cells", "spearman_correlation_cells",
            # bivariate
            "mean_vs_variance", "mean_vs_fraction_zero", "lib_size_vs_fraction_zero"
        ]
        self.MIN_SCORE = self.data_property_parameters["min_score"]

        self._inititialize_benchmark()

    def _inititialize_benchmark(self):
        from BEASTsim.utils.utils import _init_dir
        from os import environ

        def _initR():
            if self.data_property_parameters["use_R"]:
                import os, warnings
                os.environ["RPY2_CFFI_MODE"] = "ABI"
                warnings.filterwarnings("ignore",
                                        message="Environment variable \"PATH\" redefined",
                                        module="rpy2.rinterface")
                environ['r_home'] = self.data_property_parameters["r_home"]
                environ['LANG'] = self.data_property_parameters["r_lang"]
                from rpy2.robjects import pandas2ri, numpy2ri
                from rpy2.robjects.packages import importr
                self.ks = importr('ks')
                self.stats = importr('stats')
                self.base = importr('base')

        inits = [
            (_initR, ()),
            (_init_dir, (self.data_property_parameters["dir"],)),
            (_init_dir, (self.data_property_parameters["cache_dir"],)),
        ]
        total_iterations = len(inits)
        with tqdm(
                total=total_iterations, desc="Initializing DataProperty Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for init, args in inits:
                init(*args)
                progress_bar.update(1)

    def run(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data], single_cell_data: Optional[BEAST_Data]=None, name: str = "data_property_benchmark.png") -> tuple[Dict[
        str, List[DataFrame]],List[BEAST_Data], List[Dict]]:
        """
        Compute **data-property benchmarks** for one or several simulations
        compared to the reference real dataset. Each metric is evaluated
        (i) on the full expression matrix and (ii) split *by cell types*.
        Results are converted into spider-chart inputs (raw & normalised) and
        saved together with a pickle that holds the raw numeric values.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset against which all the input simulations
            will be benchmarked.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            One or more simulated datasets to benchmark. A single instance is
            automatically wrapped in a list.
        single_cell_data : Optional[BEAST_Data], default None
            Single-cell data matching the biological origin of `real_data`
            used for post-simulation processing to calculate cell-type
            distributions in the spatial spots of the simulated spatial
            transcriptomics data given that datasets are in spot-resolution.
            Used only when the data-property benchmarks are configured to
            operate *by cell type*.
        name : str, default "data_property_benchmark.png"
            Base filename for the generated plots and the pickled score
            dictionary.

        Returns
        -------
        tuple[Dict[str, List[pandas.DataFrame]], List[BEAST_Data], List[Dict]]
            1. **result_dict** – maps each simulation name to a two-element
               list: ``[whole_dataset_df, by_celltype_df]``.
            2. **updated_simulated_data** – the (possibly modified) list of
               `BEAST_Data` simulations after optional addition of real
               reference as ground-truth.
            3. **plotting_data** – a list::

                   [
                     {"Data Properties": <normalized_scores_dict>},
                     {"Data Properties": <raw_scaled_scores_dict>}
                   ]

               ready for use by the ``create_spider_chart`` plotting function.
        """
        from BEASTsim.utils.utils_plot import create_spider_chart
        from BEASTsim.utils.utils import _normalize_benchmark_results, _use_ground_truth, _save_data
        from os.path import splitext
        from copy import deepcopy
        result_dictionary = {}

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        updated_simulated_data = _use_ground_truth(use_ground_truth=self.parameters["Benchmarking"]["use_ground_truth"],
                                                   real=real_data,
                                                   sim_data=simulated_data)
        if updated_simulated_data is not None:
            simulated_data = updated_simulated_data

        if self.data_property_parameters["by_cell_types"] or ('cell_type' in real_data.data.obs and 'centroids' not in real_data.data.obs):
            from BEASTsim.modules.analysis.spatial_module.cell_mapping.cell2location import Cell2Location
            Cell2Location.calc_cell_types_all(self.parameters, real_data, simulated_data, single_cell_data)

        total_iterations = len(simulated_data)
        with tqdm(
                total=total_iterations, desc="Running Data Property Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for sim in simulated_data:
                sim_name = sim.name
                result_dictionary[sim_name] = self.data_property_benchmark(real_data=real_data, simulated_data=sim)
                progress_bar.update(1)


            save_path = f"{self.parameters['Benchmarking']['Simulation']['dir']}/{splitext(name)[0]}"
            _save_data(data=result_dictionary, filename=save_path + "_results.pkl")
            result_dictionary_scaled = _normalize_benchmark_results(data=deepcopy(result_dictionary),
                                                                    min=self.MIN_SCORE,
                                                                    max=0)
            result_dictionary_normalized = _normalize_benchmark_results(result_dictionary)
            plotting_data = [
                {
                    "Data Properties": result_dictionary_normalized
                },
                {
                    "Data Properties": result_dictionary_scaled
                }
            ]
            create_spider_chart(data_dict=plotting_data[0],
                                save_path=save_path + "_normalized" + ".png")
            create_spider_chart(data_dict=plotting_data[1],
                                save_path=save_path + "_raw" + ".png")

            return result_dictionary, simulated_data, plotting_data

    def data_property_benchmark(self, real_data: BEAST_Data, simulated_data: BEAST_Data):

        """
        Return the **final data-property score vector** for a single simulation,
        optionally *by cell types* if
        ``data_property_parameters["by_cell_types"]`` is ``True``,
        and using the test selected in ``parameters["score_type"]``
        (``"kde"`` or ``"ks"``).  If scores are calculated *by cell types*,
        the separate scores are aggregated as a weighted average according to
        cell-type abundance.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset that provides the real gene-expression
            statistics.
        simulated_data : BEAST_Data
            One simulated dataset whose gene-expression properties are compared
            with `real_data`.

        Returns
        -------
        pandas.DataFrame
            A single-column frame (``"KDE_Score"`` **or** ``"KS_Score"``)
            indexed by the 15 data-property names
            (``mean_expression``, ``var_expression``, …,
            ``lib_size_vs_fraction_zero``).

        Raises
        ------
        ValueError
            If ``parameters["score_type"]`` is neither ``"kde"`` nor ``"ks"``.

        Notes
        -----
        The KS test is not applicable for bivariate benchmarks, but is included
        as an option to validate ``KDE_Score``. In practice, only one of the two
        statistics is used during benchmarking.
        """

        if self.data_property_parameters["by_cell_types"]:
            df = self.data_property_score_by_celltype(real_data, simulated_data)
            df.to_csv(f"{self.data_property_parameters['dir']}/DataPropertyTestByCelltype_{simulated_data.name}.csv")
        else:
            df = self.data_property_score(real_data, simulated_data,
                                          cache_path=f"{self.data_property_parameters['cache_dir']}/DataPropertyTest_{simulated_data.name}.pkl",
                                          use_cache=self.data_property_parameters['use_cache'])
            df.to_csv(f"{self.data_property_parameters['dir']}/DataPropertyTest_{simulated_data.name}.csv")
        SCORE_TYPE = self.data_property_parameters["score_type"].lower()
        if SCORE_TYPE == "kde":
            selected_df = df[["KDE_Score"]]
        elif SCORE_TYPE == "ks":
            selected_df = df[["KS_Score"]]
        else:
            raise ValueError(f"Invalid score_type: '{self.data_property_parameters['score_type']}'. Expected 'kde' or 'ks'.")
        if simulated_data.is_prenormalized:
            selected_df = self._exclude_prenormalized_datasets(selected_df)
        return selected_df

    def _exclude_prenormalized_datasets(self, df):
        rows_to_set_none = [
            "lib_size",
            "TMM",
            "effective_lib_size",
            "scaled_var_expression",
            "lib_size_vs_fraction_zero"
        ]

        df.loc[rows_to_set_none] = None

        return df

    def _empty_data_property_score(self) -> DataFrame:
        from numpy import zeros
        def _score_p_value(p):
            from numpy import log10
            if p is None:
                return None
            elif p == 0:
                return self.MIN_SCORE
            elif p < 0:
                return None
            else:
                return max(log10(p), self.MIN_SCORE)

        univariate_keys = [
            # genes related
            "mean_expression", "var_expression", "scaled_var_expression", "fraction_zero_genes", "pearson_correlation_genes", "spearman_correlation_genes",
            # cells related
            "lib_size", "effective_lib_size", "TMM", "fraction_zero_cells", "pearson_correlation_cells", "spearman_correlation_cells"
        ]

        bivariate_keys = [
            "mean_vs_variance", "mean_vs_fraction_zero", "lib_size_vs_fraction_zero"
        ]
        names = univariate_keys + bivariate_keys
        num_rows = len(names)
        data = {
            "KDE_Score": zeros(num_rows),
            "KS_Score": zeros(num_rows)
        }
        df = DataFrame(data, index=names)
        df = df.applymap(_score_p_value)
        return df

    @_use_cache
    def data_property_score(self, real_data: Union[BEAST_Data, AnnData], simulated_data: Union[BEAST_Data, AnnData]) -> DataFrame:
        """
        Compute the **KDE** and **KS** statistics for all 15 univariate / bivariate
        data-property benchmarks by calling
        ``GenericDataProperties.run()`` → ``KDE.run()``.
        Results are cached (via ``@use_cache``) so that repeated calls are fast
        if cache-loading is enabled.

        Parameters
        ----------
        real_data : Union[BEAST_Data, AnnData]
            Real reference dataset that provides the real gene-expression
            statistics, supplied as `BEAST_Data` **or** raw `AnnData`.
        simulated_data : Union[BEAST_Data, AnnData]
            Simulated dataset whose gene-expression properties are compared with
            `real_data`, supplied as `BEAST_Data` **or** `AnnData`.

        Returns
        -------
        pandas.DataFrame
            Two-column frame indexed by the 15 benchmark names.
            Columns::

                KDE_Score   – -log10 p-values (clipped at MIN_SCORE) from the KDE test
                KS_Score    – same, but from the two-sample Kolmogorov–Smirnov test

        Raises
        ------
        TypeError
            If either argument is not a `BEAST_Data` or `AnnData` instance.

        Notes
        -----
        The KS test is not applicable for bivariate benchmarks, but is included
        as an option to validate ``KDE_Score``. In practice, only one of the two
        statistics is used during benchmarking.
        """
        def _score_p_value(p):
            from numpy import log10
            if p is None:
                return None
            elif p == 0:
                return self.MIN_SCORE
            elif p < 0:
                return None
            else:
                return max(log10(p), self.MIN_SCORE)

        if isinstance(real_data, BEAST_Data):
            adata_real = real_data.data
        elif isinstance(real_data, AnnData):
            adata_real = real_data
        else:
            raise TypeError("real_data must be a MOPITAS_Dataset or AnnData object.")

        if isinstance(simulated_data, BEAST_Data):
            adata_sim = simulated_data.data
        elif isinstance(simulated_data, AnnData):
            adata_sim = simulated_data
        else:
            raise TypeError("simulated_data must be a MOPITAS_Dataset or AnnData object.")

        if "voxelized_subdata" in adata_real.uns:
            adata_real = adata_real.uns["voxelized_subdata"]
            adata_sim = adata_sim.uns["voxelized_subdata"]

        if 'univariate' not in adata_real.uns or 'bivariate' not in adata_real.uns:
            univariate_real, bivariate_real = self.generic_data_properties.run(adata_real)
            adata_real.uns['univariate'] = univariate_real
            adata_real.uns['bivariate'] = bivariate_real
        else:
            univariate_real = adata_real.uns['univariate']
            bivariate_real = adata_real.uns['bivariate']

        univariate_sim, bivariate_sim = self.generic_data_properties.run(adata_sim)

        df = self.kde.run(univariate_real, bivariate_real, univariate_sim, bivariate_sim, 2)
        df = df.apply(lambda col: col.map(_score_p_value))
        return df

    def data_property_score_by_celltype(self, real_data: BEAST_Data, simulated_data: BEAST_Data) -> DataFrame:
        """
        Compute data-property benchmarks **within each cell type**, weight the
        resulting scores by cell-type abundance in the real dataset, and return
        the weighted KDE / KS score vectors.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset whose ``obs["cell_type"]`` annotation defines
            the cell-type grouping.
        simulated_data : BEAST_Data
            Simulated dataset to compare with `real_data`; cell-type labels must
            match those in the reference (rare types with fewer than three cells
            contribute only minimal scores).

        Returns
        -------
        pandas.DataFrame
            One row per data-property benchmark with two columns::

                KDE_Score   – weighted mean of per-cell-type KDE statistics
                KS_Score    – weighted mean of per-cell-type KS statistics
                               (bivariate rows are NaN)

        Notes
        -----
        The KS test is not defined for bivariate benchmarks; it is included only
        to validate ``KDE_Score``. In practice, the pipeline uses one of the two
        statistics, never both, when scoring benchmarks.
        """
        from numpy import array, newaxis, sum, concatenate

        if "voxelized_subdata" in real_data.data.uns:
            adata_real = real_data.data.uns["voxelized_subdata"]
            adata_sim = simulated_data.data.uns["voxelized_subdata"]
        else:
            adata_real = real_data.data
            adata_sim = simulated_data.data
        exprsMtx_real = adata_real
        exprsMtx_sim = adata_sim
        cellTypes_real = adata_real.obs['cell_type']
        cellTypes_sim = adata_sim.obs['cell_type']
        k = len(cellTypes_real.cat.categories)
        l = len(cellTypes_real)
        data_frames = []
        data = []
        cell_types = adata_real.obs['cell_type'].cat.categories.tolist()
        num_cell_types = len(cell_types)
        rare_cell_types_real = set()
        rare_cell_types_sim = set()
        for i in range(num_cell_types):
            cell_type_real = adata_real.obs[adata_real.obs['cell_type'] == cell_types[i]]
            if len(cell_type_real) < 3:
                rare_cell_types_real.add(cell_types[i])
        for i in range(num_cell_types):
            cell_type_sim = adata_sim.obs[adata_sim.obs['cell_type'] == cell_types[i]]
            if len(cell_type_sim) < 3:
                rare_cell_types_sim.add(cell_types[i])
        for i in tqdm(range(k)):
            level = cellTypes_real.cat.categories[i]
            if (level in rare_cell_types_real) or (level in rare_cell_types_sim):
                data_frames.append(
                    self._empty_data_property_score()
                )
                data.append((None, None))
            else:
                adata_real_i = exprsMtx_real[cellTypes_real == level].copy()
                if "GenericDataProperties" in real_data.data.uns:
                    if real_data.data.uns["GenericDataProperties"][level][0] is not None:
                        adata_real_i.uns["univariate"] = real_data.data.uns["GenericDataProperties"][level][0]
                    if real_data.data.uns["GenericDataProperties"][level][1] is not None:
                        adata_real_i.uns["bivariate"] = real_data.data.uns["GenericDataProperties"][level][1]
                adata_sim_i = exprsMtx_sim[cellTypes_sim == level].copy()
                data_frames.append(
                    self.data_property_score(adata_real_i, adata_sim_i,
                                             cache_path=f"{self.data_property_parameters['cache_dir']}/DataPropertyTestByCelltype_{simulated_data.name}_{level}.pkl",
                                             use_cache=self.data_property_parameters['use_cache'])
                )
                data.append((adata_real_i.uns["univariate"], adata_real_i.uns["bivariate"]))

        real_data.data.uns["GenericDataProperties"] = data
        KDE_scores = array([data_frames[i].KDE_Score for i in range(k)])
        KS_scores = array([data_frames[i].KS_Score[0:12] for i in range(k)])

        weights = array(
            [len(exprsMtx_real[cellTypes_real == cellTypes_real.cat.categories[i]]) / l for i in range(k)])
        weights = weights[:, newaxis]

        weighted_KDE_score = sum(weights * KDE_scores, axis=0)
        weighted_KS_score = sum(weights * KS_scores, axis=0)

        weighted_KS_score = concatenate((weighted_KS_score, array([None, None, None])))

        data = {
            "KDE_Score": weighted_KDE_score,
            "KS_Score": weighted_KS_score
        }
        df = DataFrame(data, index=self.NAMES)
        return df
