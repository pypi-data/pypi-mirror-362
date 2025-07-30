
from tqdm import tqdm
from typing import List, Union, Dict, Literal
from BEASTsim.beast_data import  BEAST_Data

BenchmarkKeys = Literal["DataPropertyBenchmark", "BiologicalSignalsBenchmark", "SimilarityBenchmark"]

class SimulationBenchmark:
    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.SimulationParameters = parameters["Benchmarking"]["Simulation"]

        # Imports
        from BEASTsim.modules.benchmarking.simulation.data_properties.data_property_benchmark import DataPropertyBenchmark
        from BEASTsim.modules.benchmarking.simulation.biological_signals.biological_signals_benchmark import BiologicalSignalsBenchmark
        from BEASTsim.modules.benchmarking.simulation.similarity.similarity_benchmark import SimilarityBenchmark

        # Modules
        self.DataPropertyBenchmark = DataPropertyBenchmark(self.parameters)
        self.BiologicalSignalsBenchmark = BiologicalSignalsBenchmark(self.parameters)
        self.SimilarityBenchmark = SimilarityBenchmark(self.parameters)

        self._inititializeBenchmark()

    def _inititializeBenchmark(self):
        from BEASTsim.utils.utils import _init_dir
        inits = [
            (_init_dir, (self.SimulationParameters["dir"],)),
        ]
        total_iterations = len(inits)
        with tqdm(
                total=total_iterations, desc="Initializing Simulation Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for init, args in inits:
                init(*args)
                progress_bar.update(1)

    def run(self, real_data: BEAST_Data,
            simulated_data: Union[List[BEAST_Data],
            BEAST_Data],
            single_cell_data: BEAST_Data,
            names: Dict[str, str] = None,
            title: str = "Simulation Benchmark"):

        """
        Run all the three benchmark types, data-property, biological-signals,
        and similarity in one go. The method handles the benchmarks, aggregates
        their numeric output, builds summary *spider charts* (raw & normalized),
        and returns the per-type results so you can inspect or save them for
        further use.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset against which all the input simulations will
            be benchmarked.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            One or more simulated datasets to benchmark. A single instance is
            automatically wrapped in a list.
        single_cell_data : BEAST_Data
            Single-cell data matching the biological origin of the `real_data`
            used for post-simulation processing to calculate cell type
            distributions in the spatial spots of the simulated spatial
            transcriptomics data. The output is used by most of our benchmarks
            when the datasets are in spot-resolution.
        names : Optional[Dict[str, str]], default None
            Mapping from benchmark names to filenames for the created spider
            charts and saved raw data. When `None` the method uses::
                {
                    "DataPropertyBenchmark":   "DataPropertyBenchmark.png",
                    "BiologicalSignalsBenchmark": "BiologicalSignalsBenchmark.png",
                    "SimilarityBenchmark":        "SimilarityBenchmark.png",
                }
        title : str, default "Simulation Benchmark"
            Base label for the combined spider charts
            (`"<title> - normalized.png"` and `"<title> - raw.png"`).

        Returns
        -------
        List[Tuple[Dict[str, Any], List[Dict]]]
            A list with three entries, one per benchmark type in the same order
            as executed:

            1. **Data-property benchmark** – tuple ``(result_dict, plotting_data)``
            2. **Biological-signals benchmark** – tuple ``(result_dict, plotting_data)``
            3. **Similarity benchmark** – tuple ``(result_dict, plotting_data)``

            where ``result_dict`` maps each simulation name to its metric
            dataframe(s), and ``plotting_data`` is a two-element list
            ``[{normalized_scores}, {raw_scores}]`` ready for use in plotting.

        Raises
        ------
        ValueError
            If `names` is supplied but lacks any of the required keys
            ``{"DataPropertyBenchmark", "BiologicalSignalsBenchmark",
            "SimilarityBenchmark"}``.
        """

        from BEASTsim.utils.utils_plot import create_spider_chart
        # TODO: We need to make sure simulated_data always contains at least 2 in all run functions
        # TODO: Run spider charts plot normalized and non normalized
        required_keys = {"DataPropertyBenchmark", "BiologicalSignalsBenchmark", "SimilarityBenchmark"}

        if names is None:
            names = {
                "DataPropertyBenchmark": "DataPropertyBenchmark.png",
                "BiologicalSignalsBenchmark": "BiologicalSignalsBenchmark.png",
                "SimilarityBenchmark": "SimilarityBenchmark.png",
            }
        else:
            missing_keys = required_keys - names.keys()
            if missing_keys:
                raise ValueError(f"Missing keys in 'names': {missing_keys}. Expected keys: {required_keys}")

        results = []
        benchmark_functions = [
            (self.DataPropertyBenchmark.run, (real_data, simulated_data, single_cell_data, names["DataPropertyBenchmark"])),
            (self.BiologicalSignalsBenchmark.run, (real_data, simulated_data, single_cell_data, names["BiologicalSignalsBenchmark"])),
            (self.SimilarityBenchmark.run, (real_data, simulated_data, single_cell_data, names["SimilarityBenchmark"])),
        ]
        total_iterations = len(benchmark_functions)
        with tqdm(
                total=total_iterations, desc="Running Simulation Benchmarks", unit="step", leave=False
        ) as progress_bar:
            for benchmark_function, args in benchmark_functions:
                benchmark_result, updated_simulated_data, plotting_data = benchmark_function(*args)
                simulated_data = updated_simulated_data.copy()
                results.append((benchmark_result, plotting_data))
                progress_bar.update(1)

        normalized_plotting_data = {}
        raw_plotting_data = {}
        for _, plotting_data in results:
            normalized_plotting_data.update(plotting_data[0])
            raw_plotting_data.update(plotting_data[1])

        create_spider_chart(data_dict=normalized_plotting_data,
                            save_path=f"{self.parameters['Benchmarking']['Simulation']['dir']}/{title} - normalized.png",
                            title=f"{title} - (Normalized)")

        create_spider_chart(data_dict=raw_plotting_data,
                            save_path=f"{self.parameters['Benchmarking']['Simulation']['dir']}/{title} - raw.png",
                            title=f"{title} - (Raw)")

        return results