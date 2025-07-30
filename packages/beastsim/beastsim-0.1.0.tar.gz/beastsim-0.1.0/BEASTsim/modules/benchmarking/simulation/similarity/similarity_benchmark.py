from typing import List, Union, Dict
import numpy as np
from pandas import DataFrame
from tqdm import tqdm
import pandas as pd
from BEASTsim.beast_data import BEAST_Data
from BEASTsim.utils.utils import _square_normalize, _add_svg_matrix, _grid_transform
from BEASTsim.modules.analysis.spatial_module.simulation.plotting.similarity_plotting import SimilarityPlotting

class SimilarityBenchmark:
    def __init__(self, parameters):
        self.parameters = parameters
        self.SimilarityParameters = self.parameters["Benchmarking"]["Simulation"]["Similarity"]

        # JASON PARAMETERS
        self.show = False # TODO: Needs to be saved instead

    def run(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data], single_cell_data: BEAST_Data=None, name: str = "SimilarityBenchmark.png") -> tuple[Dict[
        str, List[DataFrame]],List[BEAST_Data], List[Dict]]:
        """
        Perform **spatial similarity** benchmarks in terms of SVG gene expression
        and cell-type distributions across regions between a grid-transformed real
        dataset and one or more grid-transformed simulated datasets.

        For every simulation the method

        1. Optionally copies ground-truth annotations from the real data
           (``use_ground_truth``) and, if requested, (re)calculates cell-type
           distributions with Cell2Location.
        2. Calls the private helper ``_one_col_spatial_similarity_benchmark``,
           which returns Dice-score summaries for

              • global / local / average *cell-type distribution* (CT)
              • global / local / average *spatially variable gene distribution* (SVG)
              • global / local / average *tissue-shape* overlap.

        3. Collects all per-simulation DataFrames in a dictionary.
        4. Normalises the scores, renders raw and normalised spider charts, and
           pickles the raw results.

        Parameters
        ----------
        real_data : BEAST_Data
            Real reference dataset against which all the input simulations are
            benchmarked.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            One or more simulated datasets to benchmark. A single instance is
            automatically wrapped in a list.
        single_cell_data : BEAST_Data
            Single-cell data matching the biological origin of `real_data`.
            Used to calculate cell-type distributions in spot-resolution datasets.
        name : str, default "SimilarityBenchmark.png"
            Stem for all outputs:
            ``"<name> - normalized.png"``, ``"<name> - raw.png"``,
            and ``"<name>-Results.pkl"``.

        Returns
        -------
        tuple[Dict[str, List[pandas.DataFrame]], List[BEAST_Data], List[Dict]]
            1. **result_dict** – ``{simulation_name: DataFrame}``; each DataFrame
               has one column ``"Dice_Scores"`` and nine indexed rows
               (``CT_Global``, ``SVG_Global``, ``Shape_Global``,
               ``CT_Local``, …, ``Shape_Average``).
            2. **updated_simulated_data** – list of `BEAST_Data` objects
               (possibly modified by ground-truth insertion).
            3. **plotting_data** – ::

                   [
                       {"Similarity": <normalised_score_dict>},
                       {"Similarity": <raw_score_dict>}
                   ]

               Passed directly to ``create_spider_chart``.
        """

        from BEASTsim.utils.utils_plot import create_spider_chart
        from BEASTsim.utils.utils import _use_ground_truth, _normalize_benchmark_results, _save_data
        from os.path import splitext

        updated_simulated_data = _use_ground_truth(use_ground_truth=self.parameters["Benchmarking"]["use_ground_truth"],
                                                   real=real_data,
                                                   sim_data=simulated_data)
        if updated_simulated_data is not None:
            simulated_data = updated_simulated_data
        # TODO: SpatialDE does not store correctly pvalues etc. in the data between bio signals and similarity.
        if self.SimilarityParameters["calc_cell_types"]:
            from BEASTsim.modules.analysis.spatial_module.cell_mapping.cell2location import Cell2Location
            Cell2Location.calc_cell_types_all(self.parameters, real_data, simulated_data, single_cell_data)

        result_dictionary = {}

        from copy import deepcopy
        sim_data = deepcopy(simulated_data)
        real = deepcopy(real_data)

        if not isinstance(sim_data, list):
            sim_data = [sim_data]

        total_iterations = len(sim_data)
        with tqdm( total=total_iterations, desc="Running Similarity Benchmarks", unit="step", leave=False) as progress_bar:
            for sim in sim_data:
                sim_name = sim.name

                result_dictionary[sim_name] = self._one_col_spatial_similarity_benchmark(adata_real=real.data, adata_sim=sim.data)
                progress_bar.update(1)
            save_path = f"{self.parameters['Benchmarking']['Simulation']['dir']}/{splitext(name)[0]}"
            _save_data(data=result_dictionary, filename=save_path + "-Results.pkl")
            result_dictionary_normalized = _normalize_benchmark_results(result_dictionary)
            plotting_data = [
                {
                    "Similarity": result_dictionary_normalized
                },
                {
                    "Similarity": result_dictionary
                }
            ]
            create_spider_chart(data_dict=plotting_data[0],
                                save_path=save_path + " - normalized" + ".png")
            create_spider_chart(data_dict=plotting_data[1],
                                save_path=save_path + " - raw" + ".png")

            return result_dictionary, simulated_data, plotting_data

    # SPATIAL SIMILARITY BENCHMARK
    # COLLECTING FUNCTION 1
    def _easy_run_multiple_spatial_similarity_benchmark(self, adata_real, adata_sim):
        genes = None
        print(f'Running SpatialDE')
        from BEASTsim.modules.analysis.spatial_module.SVG.SVG_SpatialDE import SVG_SpatialDE
        SVG_SpatialDE.calc_SVGs(adata_real)
        SVG_SpatialDE.calc_SVGs(adata_sim)

        genes_real = adata_real.var['q_val'].index.to_numpy()
        genes_sim = adata_sim.var['q_val'].index.to_numpy()
        values_real = adata_real.var['q_val'].values
        values_sim = adata_sim.var['q_val'].values
        GP_real = [genes_real, values_real]
        GP_sim = [genes_sim, values_sim]

        if "voxelized_subdata" in adata_real.uns:
            q_val_real = adata_real.var['q_val']
            q_val_sim = adata_sim.var['q_val']
            adata_real = adata_real.uns["voxelized_subdata"]
            adata_sim = adata_sim.uns["voxelized_subdata"]
            adata_real.var['q_val'] = q_val_real
            adata_sim.var['q_val'] = q_val_sim

            if 'gene_id' not in adata_real.var.columns:
                adata_real.var['gene_id'] = adata_real.var.index
            if 'gene_id' not in adata_sim.var.columns:
                adata_sim.var['gene_id'] = adata_sim.var.index

        real, sim = _add_svg_matrix(adata_real, adata_sim, GP_real=GP_real, GP_sim=GP_sim, genes=genes, intersect_genes=True, only_abundance1=True,
                                        only_abundance2=False, threshold=self.SimilarityParameters["threshold"])
        real1 = _square_normalize(real, scale=1)
        sim1 = _square_normalize(sim, scale=1)
        Full_results_CT = []
        Full_results_SVG = []
        Joint_Pratial_results = []

        max_gridsize = int(np.floor(2**(np.log2(adata_real.X.shape[0])/2)))
        max_simple_layer_size = int(np.floor(np.log2(adata_real.X.shape[0])/2))
        layers = [2**i for i in range(max_simple_layer_size + 1)]
        layers.append(max_gridsize)

        print(f'Running for {len(layers)} layers')
        for gridsize in tqdm(layers):
            grid_real = _grid_transform(real1, CTD=self.SimilarityParameters["force_categorical"], gridsize=gridsize, show=self.show,
                                                            SVGD=self.SimilarityParameters["svg_distribution"])
            grid_sim = _grid_transform(sim1, CTD=self.SimilarityParameters["force_categorical"], gridsize=gridsize, show=self.show,
                                                           SVGD=self.SimilarityParameters["svg_distribution"])
            Full_List_CT, Partial_List_CT = SimilarityPlotting._spatial_similarity_benchmark(grid_real, grid_sim, p=self.SimilarityParameters["p"],
                                                                                             empty_when_one_empty=self.SimilarityParameters["empty_when_one_empty"], benchmark='cell_type_distribution')
            Full_List_SVG, Partial_List_SVG = SimilarityPlotting._spatial_similarity_benchmark(grid_real, grid_sim, p=self.SimilarityParameters["p"],
                                                                                               empty_when_one_empty=self.SimilarityParameters["empty_when_one_empty"], benchmark='SVG')
            Joint_Pratial_List = [Partial_List_CT[0], Partial_List_CT[1], Partial_List_SVG[0], Partial_List_SVG[1], Partial_List_CT[2], Partial_List_CT[3]]
            Full_results_CT.append(Full_List_CT)
            Full_results_SVG.append(Full_List_SVG)
            Joint_Pratial_results.append(Joint_Pratial_List)

        index_names_CT = ['CT_mean_dice_score_type', 'CT_mean_dice_score_cell', 'SVG_mean_dice_score_type', 'SVG_mean_dice_score_cell', 'Shape_mean_dice_score', 'Shape_mean_dice_score_cell']
        #index_names_SVG = ['SVG_mean_dice_score_type', 'SVG_mean_dice_score_cell', 'mean_dice_score_empty', 'mean_dice_score_cell_empty']
        row_names = [f'gridsize: {gridsize}' for gridsize in layers]
        row_names.append('average')
        average = np.mean(Joint_Pratial_results, axis=0)
        Joint_Pratial_results.append(average)
        df = pd.DataFrame(Joint_Pratial_results, index=row_names, columns=index_names_CT)
        #df_CT.to_csv(f"{self.SimilarityParameters['dir']}/SimilarityTest_{simulated_data.name}_cell_type_similarity.csv")
        #df_SVG.to_csv(f"{self.SimilarityParameters['dir']}/SimilarityTest_{simulated_data.name}_svg_similarity.csv")
        return [df, Full_results_CT, Full_results_SVG]

    # COLLECTING FUNCTION 2
    def _small_spatial_similarity_benchmark(self, adata_real, adata_sim):
        df = self._easy_run_multiple_spatial_similarity_benchmark(adata_real, adata_sim)[0]
        cols_wanted = ["CT_mean_dice_score_type", "SVG_mean_dice_score_type", "Shape_mean_dice_score"]
        rows = df.index.values
        rows_wanted = []
        if not (self.SimilarityParameters["all"] or self.SimilarityParameters["first_layer"] or  self.SimilarityParameters["last_layer"] or self.SimilarityParameters["average"]):
            ValueError("No rows given for output")
        else:
            if self.SimilarityParameters["all"]:
                rows_wanted = rows
            else:
                if self.SimilarityParameters["first_layer"]:
                    rows_wanted.append(rows[0])
                if self.SimilarityParameters["last_layer"]:
                    rows_wanted.append(rows[-2])
                if self.SimilarityParameters["average"]:
                    rows_wanted.append("average")
        wanted_measures = np.empty((len(rows_wanted), len(cols_wanted)))
        for i, row in enumerate(rows_wanted):
            for j, col in enumerate(cols_wanted):
                wanted_measures[i, j] = df[col][row]
        wanted_df = pd.DataFrame(wanted_measures, index=rows_wanted, columns=cols_wanted)
        return wanted_df

    # COLLECTING FUNCTION 3
    def _one_col_spatial_similarity_benchmark(self, adata_real, adata_sim):
        wanted_df = self._small_spatial_similarity_benchmark(adata_real, adata_sim)
        df_one_column = wanted_df.stack().reset_index(drop=True).to_frame(name='Dice_Scores')
        df_one_column.index = ["CT_Global", "SVG_Global", "Shape_Global", "CT_Local", "SVG_Local", "Shape_Local", "CT_average", "SVG_average", "Shape_Average"]
        return df_one_column