import contextlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from anndata import AnnData
from os import devnull, environ
from tqdm import tqdm
from BEASTsim.beast_data import BEAST_Data
from logging import getLogger, WARNING
from typing import List, Union, Optional
getLogger("matplotlib").setLevel(WARNING)


# TODO: Change directory from temp
#TODO: Fix parameters structure to be inside "Analysis/"

class Cell2Location():
    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.spatial_c2l_parameters = parameters["Analysis"]["Spatial"]["Cell_Mapping"]["Cell2Location"]
        self._initializeBenchmark()

    def _initializeBenchmark(self) -> None:
        from BEASTsim.utils.utils import _init_dir
        inits = [
            (self._errorHandling, ()),
            (_init_dir, (self.spatial_c2l_parameters["dir"],))
            # self.ensure_sparsity
        ]
        total_iterations = len(inits)
        with tqdm(
                total=total_iterations,
                desc="Initializing Cell2Location",
                unit="step",
                leave=False
        ) as progress_bar:
            for init, args in inits:
                with (
                        contextlib.redirect_stdout(open(devnull, "w"))
                        if self.spatial_c2l_parameters["suppress_warnings"]
                        else contextlib.nullcontext()
                ), (
                        contextlib.redirect_stderr(open(devnull, "w"))
                        if self.spatial_c2l_parameters["suppress_warnings"]
                        else contextlib.nullcontext()
                ): # TODO: Why is this here twice?
                    init(*args)
                    progress_bar.update(1)

    def run(self, sc_dataset, st_dataset) -> None:
        self._initializeBenchmark()
        benchmark_functions = [
            (self._batch_run_cell_regression_model, (sc_dataset,)),
            (self._batch_run_spatial_model, (st_dataset, sc_dataset)),
            (self._plot_qc_single_cell, (sc_dataset,)),
            (self._plot_qc_spatial, (st_dataset, sc_dataset)),
            (self.plot_training_curve_single_cell, (sc_dataset,)),
            (self._plot_training_curve_spatial, (st_dataset, sc_dataset)),
        ]
        total_iterations = len(benchmark_functions)
        with tqdm(
                total=total_iterations, desc="Running Cell2Location Benchmarks", unit="step"
        ) as progress_bar:
            for benchmark_function, args in benchmark_functions:
                with (
                        contextlib.redirect_stdout(open(devnull, "w"))
                        if self.spatial_c2l_parameters["supress_warnings"]
                        else contextlib.nullcontext()
                ), (
                        contextlib.redirect_stderr(open(devnull, "w"))
                        if self.spatial_c2l_parameters["supress_warnings"]
                        else contextlib.nullcontext()
                ):
                    benchmark_function(*args)
                    progress_bar.update(1)

    def _errorHandling(self) -> None:
        pass


    def _run_spatial_model(self, spatial_anndata: AnnData, single_cell_anndata: AnnData):
        environ["THEANO_FLAGS"] = 'device=cuda,floatX=float32,force_device=True'  # TODO: Use the parameters use_gpu
        from cell2location.models import Cell2location
        if (single_cell_anndata.varm and "means_per_cluster_mu_fg" in single_cell_anndata.varm.keys()  ):
            inf_aver = single_cell_anndata.varm["means_per_cluster_mu_fg"][
                [f"means_per_cluster_mu_fg_{i}"  for i in single_cell_anndata.uns["mod"]["factor_names"]]].copy()
        else:
            inf_aver = single_cell_anndata.var[[f"means_per_cluster_mu_fg_{i}" for i in single_cell_anndata.uns["mod"]["factor_names"]]].copy()
        inf_aver.columns = single_cell_anndata.uns["mod"]["factor_names"]
        intersect = np.intersect1d(spatial_anndata.var_names, inf_aver.index)
        assert (
                len(intersect) > 0
        ), "No intersection was found between the spatial data and single cell data, please check to see if the gene names for the datasets are correct"
        spatial_anndata = spatial_anndata[:, intersect].copy()
        inf_aver = inf_aver.loc[intersect, :].copy()
        Cell2location.setup_anndata(
            adata=spatial_anndata
            # , batch_key="sample"
        )
        mod = Cell2location(
            spatial_anndata,
            cell_state_df=inf_aver,
            # the expected average cell abundance: tissue-dependent
            # hyper-prior which can be estimated from paired histology:
            N_cells_per_location=self.spatial_c2l_parameters["n_cells_per_location"],
            # hyperparameter controlling normalisation of
            # within-experiment variation in RNA detection:
            detection_alpha=self.spatial_c2l_parameters["detection_alpha"],
        )
        mod.train(
            max_epochs=self.spatial_c2l_parameters["spatial_model_max_epochs"],
            batch_size=self.spatial_c2l_parameters["spatial_model_batch_size"],
            train_size=self.spatial_c2l_parameters["train_size"]
        )

        posterior = mod.export_posterior(
            spatial_anndata,
            sample_kwargs={
                "num_samples": 1000,
                "batch_size": mod.adata.n_obs,
            },
        )
        return posterior, mod

    def _plot_QC_second(self,
                        regression_model,
                        save_path: str,
                        summary_name: str = "means",
                        scale_average_detection: bool = True,
                        ):
        from scvi import REGISTRY_KEYS
        from matplotlib.colors import LogNorm
        # Taken from _reference_model.py from cell2location
        inf_aver = regression_model.samples[f"post_sample_{summary_name}"][
            "per_cluster_mu_fg"
        ].T
        if scale_average_detection and (
                "detection_y_c"
                in list(regression_model.samples[f"post_sample_{summary_name}"].keys())
        ):
            inf_aver = (
                    inf_aver
                    * regression_model.samples[f"post_sample_{summary_name}"][
                        "detection_y_c"
                    ].mean()
            )
        aver = regression_model._compute_cluster_averages(key=REGISTRY_KEYS.LABELS_KEY)
        aver = aver[regression_model.factor_names_]

        plt.hist2d(
            np.log10(aver.values.flatten() + 1),
            np.log10(inf_aver.flatten() + 1),
            bins=50,
            norm=LogNorm(),
        )
        plt.xlabel("Mean expression for every gene in every cluster")
        plt.ylabel("Estimated expression for every gene in every cluster")
        plt.savefig(save_path)

    def _plot_QC_first(self,
                       regression_model,
                       save_path: str,
                       summary_name: str = "means",
                       use_n_obs: int = 1000,
                       ):

        # Taken from _pyro_mixin.py.
        from scvi import REGISTRY_KEYS
        from scipy.sparse import issparse
        if getattr(regression_model, "samples", False) is False:
            raise RuntimeError(
                "self.samples is missing, please run self.export_posterior() first"
            )
        if use_n_obs is not None:
            ind_x = np.random.choice(
                regression_model.adata_manager.adata.n_obs,
                np.min((use_n_obs, regression_model.adata.n_obs)),
                replace=False,
            )
        else:
            ind_x = None

        regression_model.expected_nb_param = (
            regression_model.module.model.compute_expected(
                regression_model.samples[f"post_sample_{summary_name}"],
                regression_model.adata_manager,
                ind_x=ind_x,
            )
        )
        x_data = regression_model.adata_manager.get_from_registry(REGISTRY_KEYS.X_KEY)[
                 ind_x, :
                 ]
        if issparse(x_data):
            x_data = np.asarray(x_data.toarray())
        regression_model.plot_posterior_mu_vs_data(
            regression_model.expected_nb_param["mu"], x_data
        )
        plt.savefig(save_path)

    def _plot_qc_single_cell(self, sc_datasets: Union[List[BEAST_Data],BEAST_Data]) -> None:
        # TODO: Improve "batch_cell_reg_model" naming. Used to be "converted_data"
        environ["THEANO_FLAGS"] = 'device=cuda,floatX=float32,force_device=True'  # TODO: Use the parameters use_gpu
        from cell2location.models import RegressionModel
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]
        converted_sc = self._batch_run_cell_regression_model(sc_datasets)
        plt.ioff()
        for idx, single_cell_data in enumerate(converted_sc):
            print("Plotting qc for single cell data")
            mod: RegressionModel = (
                single_cell_data[1]
            )
            self._plot_QC_first(
                mod, f"{self.outdir}/{sc_datasets[idx].name}_single_cell_qc_plot1.png"
            )
            self._plot_QC_second(
                mod, f"{self.outdir}/{sc_datasets[idx].name}_single_cell_qc_plot2.png"
            )
            plt.clf()
        plt.ion()

    def _plot_qc_spatial(self, st_datasets: List[BEAST_Data], sc_datasets: List[BEAST_Data]):
        if not isinstance(st_datasets, list):
            st_datasets = [st_datasets]
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]
        converted_st = self._batch_run_spatial_model(st_datasets=st_datasets, sc_datasets=sc_datasets)
        plt.ioff()
        for idx, spatial_data in enumerate(converted_st):
            print("Plotting QC for spatial data")
            mod = spatial_data[1]
            mod.plot_QC()
            plt.savefig(f"{self.outdir}/{st_datasets[idx].name}_spatial_qc_plot.png")
            plt.clf()
        plt.ion()

    def _plot_training_curve_spatial(self, st_datasets: Union[BEAST_Data,List[BEAST_Data]], sc_datasets:Union[BEAST_Data, List[BEAST_Data]]):
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]
            if not isinstance(st_datasets, list):
                st_datasets = [st_datasets]
        converted_st = self._batch_run_spatial_model(st_datasets=st_datasets, sc_datasets=sc_datasets)

        plt.ioff()
        for idx, spatial_data in enumerate(converted_st):
            print("Plotting training curve for spatial data")
            mod = spatial_data[1]
            mod.plot_history()  # TODO make this generically configureable later
            plt.savefig(f"{self.outdir}/{st_datasets[idx].name}_spatial_learning_curve.png")
            plt.clf()
        plt.ion()

    def _run_reference_cell_regression_model(self, data: AnnData):
        environ["THEANO_FLAGS"] = 'device=cuda,floatX=float32,force_device=True'  # TODO: Use the parameters use_gpu
        from cell2location.models import RegressionModel
        RegressionModel.setup_anndata(
            adata=data,
            labels_key="cell_type",
        )
        reg_mod = RegressionModel(data)
        reg_mod.train(max_epochs=self.spatial_c2l_parameters["regression_model_max_epochs"], lr=self.spatial_c2l_parameters["lr"], train_size=self.spatial_c2l_parameters["train_size"])
        posterior_reg_mod=(
            reg_mod.export_posterior(
                data,
                sample_kwargs={
                    "num_samples": 1000,
                    "batch_size": self.spatial_c2l_parameters["regression_model_batch_size"],
                },
            ),
            reg_mod,
        )
        return posterior_reg_mod

    def _batch_run_cell_regression_model(self, sc_datasets: Union[BEAST_Data,List[BEAST_Data]]):
        batch_cell_reg_model = []
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]
        for singlecell_data in sc_datasets:
            batch_cell_reg_model.append(self._run_reference_cell_regression_model(
                 singlecell_data.data,
            #TODO: Fix cache loading
            ))
            batch_cell_reg_model[-1][1].save(
                self.outdir, prefix=f"reg_mod_{singlecell_data.name}", overwrite=True
            )
        return batch_cell_reg_model

    def _batch_run_spatial_model(self, st_datasets:  Union[BEAST_Data,List[BEAST_Data]], sc_datasets: Union[BEAST_Data,List[BEAST_Data]]):
        converted_data = []
        if not isinstance(st_datasets, list):
            st_datasets = [st_datasets]
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]

        for spatial_data, single_cell_data in zip(st_datasets, sc_datasets):
            converted_data.append(
                self._run_spatial_model(
                    spatial_data.data, single_cell_data.data)
            )
            converted_data[-1][1].save(
                self.spatial_c2l_parameters['dir'], prefix=f"spatial_model_{spatial_data.name}", overwrite=True
            )
        return converted_data

    def _convert_mapping_to_prob_distribution_in_place(self, sp, factor_name):
        def softmax(x):
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum()

        sp_cell_abundance: pd.DataFrame = sp.obsm[factor_name]
        sp_softmax = sp_cell_abundance.apply(lambda row: softmax(row), axis=1)
        sp.obsm["probabilities"] = sp_softmax

    def cell2location_robustness_benchmark_new_version(self, sc_dataset: Union[BEAST_Data, List[BEAST_Data]],
                                                       st_dataset: Union[BEAST_Data, List[BEAST_Data]],
                                                       cells: list = [], seed=42): #TODO: Decide where to place this
        from BEASTsim.utils.utils_plot import plot_robustness
        if not isinstance(sc_dataset, list):
            sc_dataset = [sc_dataset]
        if not isinstance(st_dataset, list):
            st_dataset = [st_dataset]

        for spatial, single in zip(st_dataset, sc_dataset):
            cell_abundance_list = []
            for i in range(self.spatial_c2l_parameters["n_runs"]):
                sc_regression_data = self._run_reference_cell_regression_model(single)[0]
                cell_abundance = self._run_spatial_model(
                    spatial, sc_regression_data
                )[0]
                self._convert_mapping_to_prob_distribution_in_place(
                    cell_abundance, "q05_cell_abundance_w_sf"
                )
                cell_abundance_list.append(cell_abundance)
            plot_robustness(
                cell_abundance_list,
                cells,
                f"{self.spatial_c2l_parameters['dir']}/robustness_benchmark_{single.name}.png",
            )

    def _calculate_cell_prob_distribution(self, single, spatial, name=""):
        sc_regression_data = self._run_reference_cell_regression_model(single)[0]
        cell_abundance = self._run_spatial_model(spatial, sc_regression_data)[0]
        self._convert_mapping_to_prob_distribution_in_place(
            cell_abundance, "q05_cell_abundance_w_sf"
        )
        return cell_abundance

    def plot_training_curve_single_cell(self, sc_datasets:Union[BEAST_Data, List[BEAST_Data]]): #TODO: Decide where to place this
        if not isinstance(sc_datasets, list):
            sc_datasets = [sc_datasets]
        converted_sc = self._batch_run_cell_regression_model(sc_datasets)
        plt.ioff()
        for idx, single_cell_data in enumerate(converted_sc):
            print("Plotting training curve for single cell data")
            mod = single_cell_data[1]
            mod.plot_history()
            plt.savefig(f"{self.outdir}/{sc_datasets[idx].name}_single_cell_learning_curve.png")
            plt.clf()
        plt.ion()

    @staticmethod
    def calc_cell_types(parameters, spatial_data: BEAST_Data, single_cell_data: Optional[BEAST_Data]=None, centroids=None, sc_regression_model=None):
        """
        Assigns cell-type labels at ``.obs['cell_type']`` and
        cell-type-distribution (CTD) vectors at
        ``.obs['cell_type_distribution']`` to observations (cells or voxels)
        of a spatial transcriptomics dataset.

        The following steps are performed
        ---------------------------------
        1. Skip single-cell datasets – the method is intended for spatial
           transcriptomics data.
        2. Default to existing annotations if ``obs["cell_type"]``,
           ``obsm["cell_type_distribution"]``, and ``uns["centroids"]`` are
           already present.
        3. Voxelize into Pseudo-spots – if the input consists of single
           cells (e.g. MERFISH) (without pre-existing voxelized sub-data),
           neighboring cells are spatially clustered into pseudo-spots
           before performing CTD clustering.
        4. cell2location model – otherwise (if the input is spot based)
           run cell2location to infer CTDs from a supplied single-cell
           reference; the reference regression model can be re-used via
           ``sc_regression_model``.
        5. K-means CTD clustering (silhouette + Davies–Bouldin weighted
           scoring) yields centroid vectors; each spot is assigned the index
           of its nearest centroid (based on Euclidean distance).

        Results are stored in the AnnData object of the input, at
        ----------------------------------------------------------
         ``obs["cell_type"]``               categorical centroid index
         ``obsm["cell_type_distribution"]`` per-spot probability vector
         ``uns["centroids"]``               centroid matrix (k × n_cell_types)
         ``uns["sc_regression_model"]``     reference model (stored only for real data)

        Parameters
        ----------
        parameters : dict
            Global parameters from the ``parameters.json`` file.
        spatial_data : BEAST_Data
            Spatial dataset to annotate (extended in place).
        single_cell_data : Optional[BEAST_Data], default None
            Single-cell reference used by cell2location when CTDs must be
            inferred (spot based dataset).
        centroids : Optional[numpy.ndarray], default None
            Pre-computed centroids to bypass the clustering step (required for
            simulated datasets if ``single_cell_data`` is absent).
        sc_regression_model : Optional[Any], default None
            Pre-fitted cell2location single-cell regression model; speeds up
            repeated calls.

        Returns
        -------
        None
            The ``spatial_data`` object is annotated in place.

        Raises
        ------
        ValueError
             If ``spatial_data.dataset_type == "single-cell"``.
             If neither ``single_cell_data`` nor ``centroids`` is supplied
              when new CTDs must be inferred.
             If a simulated dataset is processed without explicit
              ``centroids`` / ``sc_regression_model``.
        """
        from BEASTsim.utils.utils import _cluster_cells_into_pseudospots, _cluster_cell_distributions
        from scipy.spatial.distance import cdist
        def compute_cell_type_properties(mopitas_data: BEAST_Data, parameters, single_cell_data: BEAST_Data, centroids, sc_regression_model):
            if 'cell_type_distribution' not in mopitas_data.data.obsm:
                adata_with_probs, sc_regression_data = use_cell2_location(mopitas_data, parameters, single_cell_data, sc_regression_model)
                cell_type_distribution = adata_with_probs.obsm['probabilities']
            else:
                cell_type_distribution = mopitas_data.data.obsm['cell_type_distribution']
                sc_regression_data = None
            # TODO: Add parameters to json file
            if centroids is None:
                _, centroids = _cluster_cell_distributions(cell_type_distribution, k_start=2, k_end=20,
                                                           weights={"silhouette": 0.5, "davies": 0.5},
                                                           seed=42)
            if not isinstance(cell_type_distribution, np.ndarray):
                ct_dist_np = cell_type_distribution.to_numpy()
            else:
                ct_dist_np = cell_type_distribution
            distances = cdist(ct_dist_np, centroids)
            cell_type = np.argmin(distances, axis=1)
            return cell_type, cell_type_distribution, centroids, sc_regression_data

        def use_cell2_location(mopitas_data: BEAST_Data, parameters, single_cell_data: BEAST_Data, sc_regression_model): # TODO: We need to make use of log on CTD
            c2l = Cell2Location(parameters)
            if sc_regression_model is None:
                sc_regression_data = calc_regression_model(single_cell_data.data, c2l)
            else:
                sc_regression_data = sc_regression_model
            cell_abundance = c2l._run_spatial_model(mopitas_data.data, sc_regression_data[1].adata)[0]
            c2l._convert_mapping_to_prob_distribution_in_place(
                cell_abundance, "q05_cell_abundance_w_sf"
            )
            return cell_abundance, sc_regression_data

        def calc_regression_model(adata_ref, c2l):
            sc_regression_data = c2l._run_reference_cell_regression_model(adata_ref.copy())
            return sc_regression_data

        if spatial_data.dataset_type == "single-cell":
            raise ValueError("This function should only be run on spatial data.")
        elif 'cell_type' in spatial_data.data.obs and 'cell_type_distribution' not in spatial_data.data.obsm and 'centroids' not in spatial_data.data.uns:
            if "voxelized_subdata" not in spatial_data.data.uns:
                n_spots = int(spatial_data.data.X.shape[0]/parameters["Analysis"]["Spatial"]["Cell_Mapping"]["Cell2Location"]["cells_per_spot"])
                spatial_data.data = _cluster_cells_into_pseudospots(spatial_data.data,
                                                                    n_spots= n_spots,
                                                                    cell_type_keys=['cell_type', 'cell_type_distribution'])
                voxelized_subdata = spatial_data.data.uns['voxelized_subdata']
                cell_type_distribution = voxelized_subdata.obsm['cell_type_distribution']
                if centroids is None:
                    _, centroids = _cluster_cell_distributions(cell_type_distribution, k_start=2, k_end=20,
                                                               weights={"silhouette": 0.5, "davies": 0.5},
                                                               seed=42)
                if not isinstance(cell_type_distribution, np.ndarray):
                    ct_dist_np = cell_type_distribution.to_numpy()
                else:
                    ct_dist_np = cell_type_distribution
                distances = cdist(ct_dist_np, centroids)
                cell_type = np.argmin(distances, axis=1)
                voxelized_subdata.obs['cell_type'] = cell_type
                voxelized_subdata.obs['cell_type'] =  voxelized_subdata.obs['cell_type'].astype('category')
                voxelized_subdata.uns['centroids'] = centroids

        elif 'cell_type' not in spatial_data.data.obs or 'cell_type_distribution' not in spatial_data.data.obsm or 'centroids' not in spatial_data.data.uns:
            if single_cell_data is None and centroids is None:
                raise ValueError("Either sc or centroids must be provided.")

            if centroids is None and spatial_data.is_simulated:
                raise ValueError(f"{spatial_data.name} is a simulated dataset and requires centroids.")
            elif sc_regression_model is None and spatial_data.is_simulated:
                raise ValueError(f"{spatial_data.name} is a simulated dataset and requires sc_regression_model.")

            cell_type, cell_type_distribution, centroids, sc_regression_data = compute_cell_type_properties(spatial_data, parameters, single_cell_data, centroids, sc_regression_model)

            spatial_data.data.obs["cell_type"] = cell_type
            spatial_data.data.obs["cell_type"] = spatial_data.data.obs["cell_type"].astype("category")
            spatial_data.data.obsm["cell_type_distribution"] = cell_type_distribution
            spatial_data.data.uns["centroids"] = centroids
            if not spatial_data.is_simulated:
                spatial_data.data.uns["sc_regression_model"] = sc_regression_data

    @staticmethod
    def calc_cell_types_all(parameters, real_data: BEAST_Data, sim_data: Union[List[BEAST_Data], BEAST_Data], sc_data: Optional[BEAST_Data]=None):
        """
        Batch helper that assigns cell-type labels (``.obs['cell_type']``)
        and cell-type-distribution vectors (``.obsm['cell_type_distribution']``)
        to one real spatial dataset and one or more simulated datasets,
        guaranteeing that all simulations share the same centroid set /
        reference‐model parameters.

        Processing steps
        ----------------
        1. Run :py:meth:`Cell2Location.calc_cell_types` on real_data.
        2. If real_data is a copied ground-truth reference (name starts with
           ``"GT-"``) propagate its annotations directly to the matching
           simulation.
        3. Extract centroids and—if present—the single-cell regression model from
           the annotated real data; otherwise derive them on the fly from sc_data.
        4. Iterate over every simulation and call::
             Cell2Location.calc_cell_types(
                 parameters,
                 spatial_data=sim,
                 centroids=<shared>,
                 sc_regression_model=<shared>,
             )
           so that all simulations are embedded in the same reference space.

        A tqdm progress-bar keeps track of the runs; all results are written
        in-place into each dataset’s ``.data`` :class:`anndata.AnnData`.

        Parameters
        ----------
        parameters : dict
            Global parameters from the `parameters.json` file.
        real_data : BEAST_Data
            Real dataset; processed first and used to derive the
            shared centroids / regression model.
        sim_data : Union[List[BEAST_Data], BEAST_Data]
            One simulation or a list; a single instance is wrapped into
            a list automatically.
        sc_data : Optional[BEAST_Data], default ``None``
            Single-cell reference data required for the use of Cell2Location, used when the real dataset does not already
            store a ``sc_regression_model`` and centroids must be computed.

        Returns
        -------
        None – all datasets are annotated in place.
        """
        # TODO handle the following case: real has all annotations except for regression model and a simulated dataset is missing some data and therefore requires a regression model.
        if isinstance(sim_data, BEAST_Data):
            sim_data = [sim_data]

        total_runs = 1 + len(sim_data)
        pbar = tqdm(total=total_runs, desc="Annotating cell types.", leave=False)
        Cell2Location.calc_cell_types(parameters=parameters, spatial_data=real_data, single_cell_data=sc_data)
        if real_data.copied:
            for sim in sim_data:
                sim_name = sim.name
                if sim_name == f"GT-{real_data.name}":
                    if "voxelized_subdata" in real_data.data.uns:
                        sim.data.uns["voxelized_subdata"] = real_data.data.uns["voxelized_subdata"]
                    elif "cell_type" not in sim.data.obs or "cell_type_distribution" not in sim.data.obsm or "centroids" not in sim.data.uns:
                        sim.data.obs["cell_type"] = real_data.data.obs["cell_type"]
                        sim.data.obsm["cell_type_distribution"] = real_data.data.obsm["cell_type_distribution"]
                        sim.data.uns["centroids"] = real_data.data.uns["centroids"]

        pbar.update(1)
        if "voxelized_subdata" in real_data.data.uns:
            centroids = real_data.data.uns["voxelized_subdata"].uns['centroids']
            sc_regression_data = None
        else:
            centroids = real_data.data.uns["centroids"]
            if "sc_regression_model" in real_data.data.uns:
                sc_regression_data = real_data.data.uns["sc_regression_model"]
            else:
                sc_regression_data = None
                for sim in sim_data:
                    if 'cell_type' not in sim.data.obs or 'cell_type_distribution' not in sim.data.obsm or 'centroids' not in sim.data.uns:
                        print(f"WARNING: Cell type information not complete in {sim.name}. Recalculating cell types.")
                        c2l = Cell2Location(parameters)
                        sc_regression_data = c2l._run_reference_cell_regression_model(sc_data)
                        break

        for sim in sim_data:
            Cell2Location.calc_cell_types(parameters=parameters, spatial_data=sim, single_cell_data=sc_data, centroids=centroids, sc_regression_model=sc_regression_data)
            pbar.update(1)
        pbar.close()
