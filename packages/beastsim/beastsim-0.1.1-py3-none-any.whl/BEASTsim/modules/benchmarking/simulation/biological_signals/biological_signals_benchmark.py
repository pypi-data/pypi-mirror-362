from typing import List, Dict, Union, Optional
from BEASTsim.beast_data import BEAST_Data
from tqdm import tqdm
from pandas import Series

class BiologicalSignalsBenchmark:
    def __init__(self, parameters):
        self.parameters = parameters
        self.biological_signals_parameters = parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]

        # Imports
        from BEASTsim.modules.benchmarking.simulation.biological_signals.count_based_biological_signals import CountBasedBiologicalSignals
        from BEASTsim.modules.benchmarking.simulation.biological_signals.spatial_biological_signals import SpatialBiologicalSignals

        # Modules
        self.count_based_biological_signals = CountBasedBiologicalSignals(self.parameters)
        self.spatial_biological_signals = SpatialBiologicalSignals(self.parameters)

        self._inititialize_benchmark()

    def _inititialize_benchmark(self):
        from BEASTsim.utils.utils import _init_dir
        inits = [
            (_init_dir, (self.biological_signals_parameters["dir"],)),
        ]
        total_iterations = len(inits)
        with tqdm(
                total=total_iterations, desc="Initializing DataProperty Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for init, args in inits:
                init(*args)
                progress_bar.update(1)

    def run(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data], single_cell_data: Optional[BEAST_Data] = None, name: str = "biological_signals.png") -> tuple[Dict[
        str, Series],List[BEAST_Data], List[Dict]]:
        """
        Run **all biological-signal benchmarks**—*count-based* and *spatial*—in
        one call.

        Steps
        -----
        1. Copy ground-truth annotations from *real_data* into every simulation
           (``use_ground_truth``).
        2. Infer cell-type proportions via
           ``Cell2Location.calcCellTypesAll`` when required.
        3. Execute the non-spatial and spatial benchmark suites.
        4. Merge their score Series into one dictionary.
        5. Normalise the scores and render two spider charts
           (``"<name>_normalized.png"`` and ``"<name>_raw.png"``).

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset against which the simulations are benchmarked.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            One or more simulated datasets; a single object is wrapped in a list.
        single_cell_data : Optional[BEAST_Data], default None
            Single-cell data matching the biological origin of *real_data*,
            used to derive cell-type distributions when inputs are spot-level.
        name : str, default "biological_signals.png"
            Base filename used for the raw-score pickle and the two spider-plot
            PNGs.

        Returns
        -------
        tuple[Dict[str, pandas.Series], List[BEAST_Data], List[Dict]]
            1. ``result_dictionary`` – maps each simulation name to a Series of
               biological-signal scores.
            2. ``updated_simulated_data`` – list of simulations (possibly modified
               by ground-truth insertion).
            3. ``plotting_data`` – ::

                   [
                       {"Biological Signals": <normalized_scores_dict>},
                       {"Biological Signals": <raw_scores_dict>}
                   ]

               used by ``create_spider_chart``.

        References
        ----------
        *count based bilogical signals:* Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
          *A benchmark study of simulation methods for single-cell rna sequencing data.*
          Nature Communications, 12(1):6911, Nov 2021.

          *scClassify: sample size estimation and multiscale classification of cells using single and multiple reference.*
          Mol. Syst. Biol. 16, e9389 (2020).
        """
        from BEASTsim.modules.analysis.spatial_module.cell_mapping.cell2location import Cell2Location
        from BEASTsim.utils.utils import _normalize_benchmark_results, _use_ground_truth, _merge_results, _save_data
        from BEASTsim.utils.utils_plot import create_spider_chart
        from os.path import splitext
        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        updated_simulated_data = _use_ground_truth(use_ground_truth=self.parameters["Benchmarking"]["use_ground_truth"],
                                                   real=real_data,
                                                   sim_data=simulated_data)
        if updated_simulated_data is not None:
            simulated_data = updated_simulated_data

        results = []
        benchmark_functions = [
            (Cell2Location.calc_cell_types_all, (self.parameters, real_data, simulated_data, single_cell_data)),
            (self.run_count_based_biological_signals, (real_data, simulated_data)),
            (self.run_spatial_biological_signals, (real_data, simulated_data)),
        ]
        total_iterations = len(benchmark_functions)
        with tqdm(
                total=total_iterations, desc="Running Biological Signal Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for benchmark_function, args in benchmark_functions:
                result = benchmark_function(*args)
                if result is not None:
                    results.append(result)
                progress_bar.update(1)
        result_dictionary = _merge_results(results, "Scores")
        save_path = f"{self.parameters['Benchmarking']['Simulation']['dir']}/{splitext(name)[0]}"
        _save_data(data=result_dictionary, filename=save_path + "_results.pkl")
        result_dictionary_normalized = _normalize_benchmark_results(result_dictionary)
        plotting_data = [
            {
                "Biological Signals": result_dictionary_normalized
            },
            {
                "Biological Signals": result_dictionary
            }
        ]

        create_spider_chart(data_dict=plotting_data[0],
                            save_path=save_path + "_normalized" + ".png")
        create_spider_chart(data_dict=plotting_data[1],
                            save_path=save_path + "_raw" + ".png")

        return result_dictionary, simulated_data, plotting_data

    def run_count_based_biological_signals(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data]) -> Dict[str, List]:
        """
        Perform **count based biological signals** benchmarks (DE Limma/Scanpy,
        DV, DD, DP, BD) for each simulation by calling
        ``CountBasedBiologicalSignals.run`` and return the results as a
        dictionary keyed by simulation name.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset providing the ground-truth signal counts.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            One or many simulations; wrapped in a list if necessary.

        Returns
        -------
        Dict[str, List]
            ``{simulation_name: count_based_signals_series}`` for every
            simulation processed.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).
        Lin, Y. et al.
            *scClassify: sample size estimation and multiscale classification of
            cells using single and multiple reference.* Mol. Syst. Biol. 16, e9389
            (2020).
        """
        from copy import deepcopy
        result_dictionary = {}
        real = deepcopy(real_data)

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        total_iterations = len(simulated_data)
        with tqdm(
                total=total_iterations, desc="Running Count Based Biological Signal Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for sim in simulated_data:
                sim_name = sim.name
                count_based_signals = self.count_based_biological_signals.run(real, deepcopy(sim))
                result_dictionary[sim_name] = count_based_signals
                progress_bar.update(1)
        return result_dictionary

    def run_spatial_biological_signals(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data]) -> Dict[str, List]:
        """
        Perform **spatial biological signals** benchmarks (neighbourhood
        structure, SVG overlap, etc.) for each simulation by applying
        ``SpatialBiologicalSignals.run``. All individual Series are concatenated
        into a CSV file, and a dictionary of per-simulation Series is returned.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            Simulation(s) to evaluate.

        Returns
        -------
        Dict[str, List]
            ``{simulation_name: spatial_signals_series}`` for every simulation
            processed.
        """
        from pandas import concat
        from copy import deepcopy
        result_dictionary = {}
        real = deepcopy(real_data)
        results = []
        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        total_iterations = len(simulated_data)
        with tqdm(
                total=total_iterations, desc="Running Spatial Biological Signal Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for sim in simulated_data:
                sim_name = sim.name
                spatial_signals = self.spatial_biological_signals.run(real, deepcopy(sim))
                results.append(spatial_signals)
                result_dictionary[sim_name] = spatial_signals
                progress_bar.update(1)
        results_df = concat(results, axis=1)
        results_df.columns = [s.name for s in results]
        save_dir = self.parameters["Benchmarking"]["Simulation"]["BiologicalSignals"]["dir"]
        results_df.to_csv(f"{save_dir}/SpatialBiologicalSignalsBenchmark.csv", index=True, header=True)
        return result_dictionary
