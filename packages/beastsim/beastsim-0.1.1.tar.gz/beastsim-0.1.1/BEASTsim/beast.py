from typing import Union, List, Optional
from BEASTsim.beast_data import BEAST_Data

#TODO: Maybe call this something different?
class BEAST:
    """
    MOPITAS_Benchmark is a benchmarking tool for spatial transcriptomics analysis.
    It initializes both the analysis and benchmarking module,
    and provides a method for annotating spatial data.
    """
    def __init__(self, parameters_file_path: Optional[str] = None):
        parameters_file_path = (
            "parameters.json" if parameters_file_path == None else parameters_file_path
        )
        from json import load
        with open(parameters_file_path, "r") as f:
            self.parameters = load(f)

        # Imports
        from BEASTsim.modules.analysis.analysis import Analysis
        from BEASTsim.modules.benchmarking.benchmarking import Benchmarking

        # Modules
        self.Analysis = Analysis(self.parameters)
        self.Benchmarking = Benchmarking(self.parameters)

    def annotate_data(self, real_data: BEAST_Data, sc_data: Optional[BEAST_Data] = None, sim_data: Optional[Union[BEAST_Data, List[BEAST_Data]]] = None, output_dir: Optional[str] = None):
        """
        Performs spatially variable gene (SVG) analysis and cell type deconvolution
        on spatial transcriptomics datasets, optionally including simulated data.

        Args:
            real_data (BEAST_Data):
                The real spatial transcriptomics dataset to analyze.
            sc_data (BEAST_Data):
                Single-cell reference dataset used for cell type mapping.
            sim_data (Optional[Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]], default=None):
                Optional simulated datasets for benchmarking. If provided, they are also annotated
            output_dir (Optional[str], default=None):
                Directory where processed datasets will be saved in `.h5ad` format.
                If None, results are not saved.

        Functionality:
            - Conducts spatially variable gene (SVG) analysis using `SpatialDE`.
            - Performs cell type mapping using `Cell2Location`.
            - Saves processed datasets in `.h5ad` format if `output_dir` is provided.
        """
        import os
        from tqdm import tqdm
        from BEASTsim.utils.utils import _init_dir

        _init_dir(path=output_dir)

        if sim_data is None:
            spatial_data = [real_data]
        else:
            if not isinstance(sim_data, List):
                sim_data = [sim_data]
            spatial_data = [real_data] + sim_data

        if sim_data is None:

            self.Analysis.spatial_analysis.cell_mapping_analysis.cell2location.calc_cell_types(parameters=self.parameters,
                                                                                               spatial_data=real_data,
                                                                                               single_cell_data=sc_data)
        else:
            self.Analysis.spatial_analysis.cell_mapping_analysis.cell2location.calc_cell_types_all(parameters=self.parameters,
                                                                                                   real_data=real_data,
                                                                                                   sim_data=sim_data,
                                                                                                   sc_data=sc_data)

        self.Analysis.spatial_analysis.SVG_Analysis.SVG_SpatialDE.calc_SVGs_all(spatial_datasets=spatial_data)

        if output_dir is not None:
            pbar = tqdm(total=len(spatial_data), desc="Saving annotated data.", leave=False)
            for data in spatial_data:
                name = f"{data.name}.h5ad"
                save_path = os.path.join(output_dir, name)
                if "sc_regression_model" in data.data.uns:
                    del data.data.uns["sc_regression_model"]
                data.data.write_h5ad(save_path, compression="gzip")
                pbar.update(1)
            pbar.close()
