from logging import getLogger, WARNING
from BEASTsim.beast_data import BEAST_Data
from tqdm import tqdm
from typing import List, Union
from numpy import ndarray
from pandas import DataFrame, Series
getLogger("matplotlib").setLevel(WARNING)

class GeneExpressionAnalysis():
    def __init__(self, parameters):
        self.parameters = parameters
        self.GeneExpressionAnalysisParameters = self.parameters["Analysis"]["GeneExpressions"]
        self._initializeBenchmark()

    def _initializeBenchmark(self) -> None:
        from BEASTsim.utils.utils import _init_dir
        inits = [
            (_init_dir, (self.GeneExpressionAnalysisParameters["output"],))
        ]

        total_iterations = len(inits)
        with tqdm(
                total=total_iterations,
                desc="Initializing Gene Expression Analysis",
                unit="step",
                leave=False,
        ) as progress_bar:
            for init, params in inits:
                init(*params)
                progress_bar.update(1)

    def run(self, real_data: BEAST_Data, simulated_data: Union[List[BEAST_Data], BEAST_Data]) -> None:
        """
        Executes all gene expression analysis.
        """
         # TODO: What do we about this?
        if isinstance(simulated_data, BEAST_Data):
            simulated_data = [simulated_data]
        data = [real_data] + simulated_data

        analysis_functions = [
            (self.dim_red_analysis, ("UMAP", data)),
            (self.dim_red_analysis, ("PCA", data)),
            (self.statistical_base_analysis, (real_data, simulated_data)),
            (self.statistical_gene_n_cell_analysis, (real_data, simulated_data)),
            (self.comparison_analysis, (real_data, simulated_data)),
            (self.pearson_correlation_analysis, (data,)),
        ]
        total_iterations = len(analysis_functions)
        with tqdm(
                total=total_iterations, desc="Running Gene Expression Analysis", unit="step"
        ) as progress_bar:
            for analysis_function, args in analysis_functions:
                analysis_function(*args)
                progress_bar.update(1)


    def _compute_general_statistics(self, real_data: BEAST_Data,
                                    simulated_data: Union[BEAST_Data, List[BEAST_Data]]
                                    ):
        """
        Computes general statistics between a real dataset and simulated datasets.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_data (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]):
                A list of simulated datasets or a single simulated dataset to compare with the real dataset.

        Returns:
            dict:
                A dictionary containing the computed statistics:
                - "data_statistics": General data statistics.
                - "correlations": Statistical correlations between the datasets.
                - "cell_distances": Distances between cells in the datasets.
                - "frequencies": Frequencies of features in the datasets.
        """

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        all_stats = []
        for sim in simulated_data:
            correlations = self._init_correlations(real_data, sim)
            cell_distances = self._init_cell_distances(real_data, sim)
            frequencies = self._init_frequencies(real_data, sim)

            all_stats.append({
                "correlations": correlations,
                "cell_distances": cell_distances,
                "frequencies": frequencies,
            })

        return all_stats

    def _compute_data_statistics(
            self,
            real_data: BEAST_Data,
            simulated_datas: Union[BEAST_Data, List[BEAST_Data]]
    ) -> dict:
        """
        Computes general data statistics between a real dataset and simulated datasets.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_datas (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]):
                A list of simulated datasets or a single simulated dataset to compare with the real dataset.

        Returns:
            dict:
                A dictionary containing the computed data statistics:
                - "mean_expression_real": Mean expression levels for the real dataset.
                - "variance_real": Variance in expression levels for the real dataset.
                - "library_size_real": Library size for the real dataset.
                - "mean_expression_simulated_datas": Mean expression levels for the simulated datasets.
                - "diff_mean_expression_simulated_datas": Difference in mean expression between the real and simulated datasets.
                - "variance_simulated_datas": Variance in expression levels for the simulated datasets.
                - "diff_variance_simulated_datas": Difference in variance between the real and simulated datasets.
                - "library_size_simulated_datas": Library size for the simulated datasets.
                - "diff_library_size_simulated_datas": Difference in library size between the real and simulated datasets.
        """
        from numpy import log2, var
        from scipy.sparse import issparse
        # Convert real dataset to array
        real_data_matrix = real_data.data.X
        if issparse(real_data_matrix):
            real_data_matrix = real_data_matrix.toarray()

        # Compute statistics for the real dataset
        mean_expression_real = log2(real_data_matrix.mean(axis=1) + 1)
        variance_real = log2(var(real_data_matrix, axis=1) + 1)
        library_size_real = log2(real_data_matrix.sum(axis=0) + 1)

        # Ensure simulated_datas is a list
        if not isinstance(simulated_datas, list):
            simulated_datas = [simulated_datas]

        # Initialize lists to store statistics for simulated datasets
        mean_expression_simulated_datas = []
        diff_mean_expression_simulated_datas = []
        variance_simulated_datas = []
        diff_variance_simulated_datas = []
        library_size_simulated_datas = []
        diff_library_size_simulated_datas = []

        # Compute statistics for each simulated dataset
        for simulated_data in simulated_datas:
            sim_data_matrix = simulated_data.data.X
            if issparse(sim_data_matrix):
                sim_data_matrix = sim_data_matrix.toarray()

            # Mean expression
            mean_expression = log2(sim_data_matrix.mean(axis=1) + 1)
            mean_expression_simulated_datas.append(mean_expression)

            # Difference in mean expression
            diff_expression = mean_expression_real - mean_expression
            diff_mean_expression_simulated_datas.append(diff_expression)

            # Variance
            variance = log2(var(sim_data_matrix, axis=1) + 1)
            variance_simulated_datas.append(variance)

            # Difference in variance
            diff_variance = variance_real - variance
            diff_variance_simulated_datas.append(diff_variance)

            # Library size
            library_size = log2(sim_data_matrix.sum(axis=0) + 1)
            library_size_simulated_datas.append(library_size)

            # Difference in library size
            diff_library_size = library_size_real - library_size
            diff_library_size_simulated_datas.append(diff_library_size)

        # Return computed statistics
        return {
            "mean_expression_real": mean_expression_real,
            "variance_real": variance_real,
            "library_size_real": library_size_real,
            "mean_expression_simulated_datas": mean_expression_simulated_datas,
            "diff_mean_expression_simulated_datas": diff_mean_expression_simulated_datas,
            "variance_simulated_datas": variance_simulated_datas,
            "diff_variance_simulated_datas": diff_variance_simulated_datas,
            "library_size_simulated_datas": library_size_simulated_datas,
            "diff_library_size_simulated_datas": diff_library_size_simulated_datas,
        }

    def _init_correlations(self, real_data: BEAST_Data,
                           simulated_data: Union[BEAST_Data, List[BEAST_Data]]
                           ) -> dict:
        """
        Computes correlations between genes and cells for both real and simulated datasets.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_data (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]):
                A list of simulated datasets or a single simulated dataset to compare with the real dataset.

        Returns:
            dict:
                A dictionary containing the computed correlations:
                - "real_correlations_gene": Correlations between genes for the real dataset.
                - "real_correlations_cell": Correlations between cells for the real dataset.
                - "sim_correlations_gene": Correlations between genes for the simulated datasets.
                - "sim_correlations_cell": Correlations between cells for the simulated datasets.
        """
        from numpy import corrcoef
        from scipy.sparse import issparse
        real_data = real_data.data.X
        if issparse(real_data):
            real_data = real_data.toarray()
        real_correlations_gene = corrcoef(real_data, rowvar=False).flatten()
        real_correlations_cell = corrcoef(real_data.T, rowvar=False).flatten()
        sim_data = simulated_data.data.X
        if issparse(sim_data):
            sim_data = sim_data.toarray()
        sim_correlations_gene = corrcoef(sim_data, rowvar=False).flatten()
        sim_correlations_cell = corrcoef(sim_data.T, rowvar=False).flatten()
        return {
            "real_correlations_gene": real_correlations_gene,
            "real_correlations_cell": real_correlations_cell,
            "sim_correlations_gene": sim_correlations_gene,
            "sim_correlations_cell": sim_correlations_cell
        }

    def _init_cell_distances(self, real_data: BEAST_Data,
                             simulated_data: Union[BEAST_Data, List[BEAST_Data]]
                             ) -> dict:
        """
        Computes the Euclidean distances between cells for both real and simulated datasets.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_data (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]):
                A list of simulated datasets or a single simulated dataset to compare with the real dataset.

        Returns:
            dict:
                A dictionary containing the computed cell distances:
                - "real_cell_distances": Euclidean distances between cells for the real dataset.
                - "sim_cell_distances": Euclidean distances between cells for the simulated datasets.
        """
        from scipy.spatial.distance import pdist
        from numpy import log2
        from scipy.sparse import issparse
        real_data_matrix = real_data.data.X
        if issparse(real_data_matrix):
            real_data_matrix = real_data_matrix.toarray()
        self.real_cell_distances = log2(pdist(real_data_matrix, metric="euclidean") + 1)

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        sim_cell_distances = []
        for sim in simulated_data:
            sim_data_matrix = sim.data.X
            if issparse(sim_data_matrix):
                sim_data_matrix = sim_data_matrix.toarray()
            sim_cell_distances.append(
                log2(pdist(sim_data_matrix, metric="euclidean") + 1)
            )

        real_data_matrix = real_data.data.X
        if issparse(real_data_matrix):
            real_data_matrix = real_data_matrix.toarray()
        real_cell_distances = log2(pdist(real_data_matrix, metric="euclidean") + 1)

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        sim_cell_distances_list = []
        for sim in simulated_data:
            sim_data_matrix = sim.data.X
            if issparse(sim_data_matrix):
                sim_data_matrix = sim_data_matrix.toarray()
            sim_cell_distances_list.append(log2(pdist(sim_data_matrix, metric="euclidean") + 1))

        return {
            "real_cell_distances": real_cell_distances,
            "sim_cell_distances": sim_cell_distances_list
        }


    def _init_frequencies(
            self,
            real_data: BEAST_Data,
            simulated_data: Union[BEAST_Data, List[BEAST_Data]]) -> dict:
        """
        Computes the detection frequencies of genes and cells for both real and simulated datasets.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_data (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]):
                A list of simulated datasets or a single simulated dataset to compare with the real dataset.

        Returns:
            dict:
                A dictionary containing the computed detection frequencies:
                - "real_gene_detection_frequency": The frequency of gene detections in the real dataset.
                - "real_cell_detection_frequency": The frequency of cell detections in the real dataset.
                - "sim_detection_gene_frequencies": A list of detection frequencies for genes in the simulated datasets.
                - "sim_detection_cell_frequencies": A list of detection frequencies for cells in the simulated datasets.
        """
        from numpy import sum
        from scipy.sparse import issparse
        real_data_matrix = real_data.data.X
        if issparse(real_data_matrix):
            real_data_matrix = real_data_matrix.toarray()
        total_cells = real_data_matrix.shape[0]
        total_genes = real_data_matrix.shape[1]
        gene_detection_count = sum(real_data_matrix > 0, axis=0)
        cell_detection_count = sum(real_data_matrix > 0, axis=1)
        real_gene_detection_frequency = gene_detection_count / total_cells
        real_cell_detection_frequency = cell_detection_count / total_genes

        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        sim_detection_gene_frequencies_list = []
        sim_detection_cell_frequencies_list = []
        for sim in simulated_data:
            sim_data_matrix = sim.data.X
            if issparse(sim_data_matrix):
                sim_data_matrix = sim_data_matrix.toarray()
            total_cells = sim_data_matrix.shape[0]
            total_genes = sim_data_matrix.shape[1]
            gene_detection_count = sum(sim_data_matrix > 0, axis=0)
            cell_detection_count = sum(sim_data_matrix > 0, axis=1)
            sim_detection_gene_frequencies_list.append(gene_detection_count / total_cells)
            sim_detection_cell_frequencies_list.append(cell_detection_count / total_genes)

        return {
            "real_gene_detection_frequency": real_gene_detection_frequency,
            "real_cell_detection_frequency": real_cell_detection_frequency,
            "sim_detection_gene_frequencies": sim_detection_gene_frequencies_list,
            "sim_detection_cell_frequencies": sim_detection_cell_frequencies_list
        }



    def dim_red_analysis(self, dimRedType: str, datas: Union[List[BEAST_Data], BEAST_Data]) -> None:
        """
        Benchmark dimensionality reduction (PCA or UMAP) across multiple datasets.

        Args:
            dimRedType (str):
                The type of dimensionality reduction to use. Can be either "PCA" or "UMAP".
            datas (Union[List[MOPITAS_Data], MOPITAS_Data]):
                A list of datasets or a single dataset to apply dimensionality reduction on.
        Returns:
            None:
                This function does not return any value. It generates a plot of the dimensionality reduction
                for the provided datasets and saves the plot to the output directory.
        """
        from matplotlib.pyplot import subplots, tight_layout, savefig
        from seaborn import scatterplot

        def dim_red_scatter_plot(
                x: ndarray,
                y: ndarray,
                cell_types: Series,
                axes: ndarray,
                title: str,
                ax: int,
                show_legend: bool,
                label: str,
        ) -> None:

            scatterplot(x=x, y=y, hue=cell_types, ax=axes[ax], legend=show_legend)
            axes[ax].set_title(title)
            axes[ax].set_xlabel(label + "1")
            axes[ax].set_ylabel(label + "2")

        ndata = len(datas)
        names = [data.name for data in datas] if isinstance(datas, list) else [datas.name]

        if dimRedType != "UMAP" and dimRedType != "PCA":
            raise ValueError("dimRedBenchmark can only generate UMAP or PCA.")

        # Check if PCA or UMAP is already computed, if not, call the respective function
        if dimRedType == "UMAP":
            for data in datas:
                if "umap" not in data.data.obsm:
                    data.init_umap()  # Compute UMAP if not already done
        elif dimRedType == "PCA":
            for data in datas:
                if "pca" not in data.data.obsm:
                    data.init_pca()  # Compute PCA if not already done

        # Continue with plotting the dimensionality reduction
        if ndata == 1:
            fig, ax = subplots(figsize=(4, 4))
            axes = [ax]
        else:
            fig, axes = subplots(ncols=ndata, figsize=(4 * ndata, 4))

        for i, data in enumerate(datas):
            if dimRedType == "UMAP":
                x = data.data.obsm["umap"][:, 0]
                y = data.data.obsm["umap"][:, 1]
            elif dimRedType == "PCA":
                x = data.data.obsm["pca"][:, 0]
                y = data.data.obsm["pca"][:, 1]
            else:
                raise ValueError("dimRedBenchmark can only generate UMAPS or PCA.")

            # Plot the scatter plot without enabling the legend
            dim_red_scatter_plot(
                x=x,
                y=y,
                cell_types=data.data.obs["cell_type"],
                axes=axes,
                title=names[i],
                ax=i,
                show_legend=i == 0,  # Disable legends in subplots
                label=dimRedType,
            )
        tight_layout()
        formatting = [0, 0.30, 0.4, 0.45, 0.475, 0.5]
        n_cells = 6 * ndata
        bbox = (0.5 + ndata * formatting[ndata - 1], -0.2)

        axes[0].legend(
            bbox_to_anchor=bbox, loc="upper center", title="Cell Types", ncol=n_cells
        )

        savename = f'{self.GeneExpressionAnalysisParameters["output"]}/{dimRedType}.png'
        savefig(savename, bbox_inches="tight")


    def statistical_base_analysis(
            self, real_data: BEAST_Data,
            simulated_data: Union[BEAST_Data, list[BEAST_Data]],
            dot_opacity: float = 0.2, line_opacity: float = 0.5,
            dot_size: int = 6
    ) -> None:
        """
        Performs a statistical benchmark by comparing real and simulated datasets
        using various metrics such as mean expression, variance, and library size.

        This function generates visualizations including boxplots and scatter plots
        to highlight the similarities and differences between the real and simulated data.

        Args:
            real_data (BEAST_Data):
                The real dataset to compare against the simulated datasets.
            simulated_data (Union[MOPITAS_Dataset, list[MOPITAS_Dataset]]):
                A single simulated dataset or a list of simulated datasets for comparison.
            dot_opacity (float, optional):
                Opacity level for scatter plot dots. Default is 0.2.
            line_opacity (float, optional):
                Opacity level for regression lines. Default is 0.5.
            dot_size (int, optional):
                Size of dots in scatter plots. Default is 6.

        Returns:
            None
        """
        from seaborn import boxplot, scatterplot, regplot
        from matplotlib.pyplot import subplots, tight_layout, subplots_adjust, savefig
        from BEASTsim.utils.utils import _init_colors, _build_statistical_dataframe
        from numpy import isscalar
        names = [data.name for data in simulated_data] if isinstance(simulated_data, list) else [simulated_data.name]
        colors = _init_colors(names)

        statistical_values = self._compute_general_statistics(real_data, simulated_data)
        if len(statistical_values) == 0:
            raise ValueError("No statistical values provided")

        data_stats = statistical_values["data_statistics"]
        mean_expression_real = data_stats["mean_expression_real"]
        mean_expression_simulated_datas = data_stats["mean_expression_simulated_datas"]
        diff_mean_expression_simulated_datas = data_stats["diff_mean_expression_simulated_datas"]
        variance_real = data_stats["variance_real"]
        variance_simulated_datas = data_stats["variance_simulated_datas"]
        diff_variance_simulated_datas = data_stats["diff_variance_simulated_datas"]
        library_size_real = data_stats["library_size_real"]
        library_size_simulated_datas = data_stats["library_size_simulated_datas"]
        diff_library_size_simulated_datas = data_stats["diff_library_size_simulated_datas"]

        # Ensure that each data array is wrapped with a list for single values or 1D arrays
        if isscalar(mean_expression_real):
            mean_expression_real = [mean_expression_real]  # Wrap it in a list if scalar

        if isscalar(variance_real):
            variance_real = [variance_real]  # Wrap it in a list if scalar

        # Create dataframes
        df_mean_expression = _build_statistical_dataframe(simulated_data=mean_expression_simulated_datas,
                                                          real_data=mean_expression_real, names=names)
        df_diff_mean_expression = _build_statistical_dataframe(simulated_data=diff_mean_expression_simulated_datas,
                                                               names=names)
        df_variance = _build_statistical_dataframe(simulated_data=variance_simulated_datas, real_data=variance_real,
                                                   names=names)
        df_diff_variance = _build_statistical_dataframe(simulated_data=diff_variance_simulated_datas, names=names)
        df_library_size = _build_statistical_dataframe(simulated_data=library_size_simulated_datas,
                                                       real_data=library_size_real, names=names)
        df_diff_library_size = _build_statistical_dataframe(simulated_data=diff_library_size_simulated_datas,
                                                            names=names)

        # Create plot 1
        fig, axes = subplots(nrows=4, ncols=2, figsize=(14, 12))

        # Plot boxplots of the distribution of mean expression
        boxplot(data=df_mean_expression, ax=axes[0, 0], palette=colors)
        axes[0, 0].set_title("Distribution of Mean Expression")
        axes[0, 0].set_ylabel("Mean log2")

        # Plot boxplots of the differences in mean expression
        boxplot(data=df_diff_mean_expression, ax=axes[0, 1], palette=colors)
        axes[0, 1].set_title("Differences in Mean Expression")
        axes[0, 1].set_ylabel("Rank difference mean\n log2")

        # Plot boxplots of the distribution of variance
        boxplot(data=df_variance, ax=axes[1, 0], palette=colors)
        axes[1, 0].set_title("Distribution of Variance")
        axes[1, 0].set_ylabel("Variance log2")

        # Plot boxplots of the differences in variance
        boxplot(data=df_diff_variance, ax=axes[1, 1], palette=colors)
        axes[1, 1].set_title("Differences in Variance")
        axes[1, 1].set_ylabel("Rank difference variance\n log2")

        # Add scatter plot of variance vs. mean for each method
        scatterplot(
            x=mean_expression_real,
            y=variance_real,
            label="Real",
            ax=axes[2, 0],
            color=colors["Real"],
            alpha=dot_opacity,
            s=dot_size,
        )
        regplot(
            x=mean_expression_real,
            y=variance_real,
            scatter=False,
            ax=axes[2, 0],
            color=colors["Real"],
            order=2,
            line_kws={"alpha": line_opacity},
        )
        for i, mean_expression in enumerate(mean_expression_simulated_datas):
            method_name = names[i]
            scatterplot(
                x=mean_expression,
                y=variance_simulated_datas[i],
                label=method_name,
                ax=axes[2, 0],
                color=colors[method_name],
                alpha=dot_opacity,
                s=dot_size,
            )
            regplot(
                x=mean_expression,
                y=variance_simulated_datas[i],
                scatter=False,
                ax=axes[2, 0],
                color=colors[method_name],
                order=2,
                line_kws={"alpha": line_opacity},
            )
        axes[2, 0].set_title("Mean-Variance Relationship")
        axes[2, 0].set_ylabel("Variance log2")
        axes[2, 0].legend()

        for i, diff_mean_expression in enumerate(
                diff_mean_expression_simulated_datas
        ):
            method_name = names[i]
            scatterplot(
                x=diff_mean_expression,
                y=diff_variance_simulated_datas[i],
                label=method_name,
                ax=axes[2, 1],
                color=colors[method_name],
                alpha=dot_opacity,
                s=dot_size,
            )
            regplot(
                x=diff_mean_expression,
                y=diff_variance_simulated_datas[i],
                scatter=False,
                ax=axes[2, 1],
                color=colors[method_name],
                line_kws={"alpha": line_opacity},
                robust=True,
            )
        axes[2, 1].set_title("Difference in Mean-Variance Relationship")
        axes[2, 1].set_ylabel("Difference in variance\n log2")
        axes[2, 1].legend()

        # Plot boxplots of the distribution of library size
        boxplot(data=df_library_size, ax=axes[3, 0], palette=colors)
        axes[3, 0].set_title("Distribution of Library Size")
        axes[3, 0].set_ylabel("Total counts per cell\n log2")

        # Plot boxplots of the differences in library size
        boxplot(data=df_diff_library_size, ax=axes[3, 1], palette=colors)
        axes[3, 1].set_title("Differences in Library Size")
        axes[3, 1].set_ylabel("Rank difference library size\n log2")

        tight_layout()
        subplots_adjust(hspace=0.5)
        savefig(
            f"{self.GeneExpressionAnalysisParameters['output']}/statistical_base_benchmark.png"
        )

    from typing import Union, List

    def statistical_gene_n_cell_analysis(self, real_data: BEAST_Data,
                                         simulated_data: Union[List[BEAST_Data], BEAST_Data]) -> None:
        """
        Creates five violin-plot panels that compare gene-expression statistics
        between a real reference dataset and one or more simulations.

        1. Cell–cell Euclidean distance in expression space
        2. Cell–cell Pearson correlation
        3. Gene–gene Pearson correlation
        4. Cell detection frequency – fraction of genes detected per cell
        5. Gene detection frequency – fraction of cells in which a gene is detected

        Each distribution is shown side-by-side for every simulation, using a
        consistent colour palette. Saves the created figure as
        `statistical_gene_N_cell_analysis.png` at the
        `parameters['Analysis']['Spatial']['output']` directory according to the .json parameters file.

        Args:
        ----------
        real_data : BEAST_Data
            The real dataset to compare against the simulated datasets.
        simulated_data : Union[List[BEAST_Data], BEAST_Data]
            A single simulated dataset or a list of simulated datasets for comparison.

        Returns:
        ----------
            None: This function does not return any value. The created plots are saved at the given directory.

        Raises
        ------
        ValueError:
            If, for any metric, the length of the real vector does not
            match the corresponding simulated vector(s), signalling the input error.
        """

        from matplotlib.pyplot import subplots, tight_layout, savefig
        from seaborn import violinplot
        from BEASTsim.utils.utils import _init_colors, _build_statistical_dataframe,_unwrap_array_if_wrapped

        simulated_data = simulated_data if isinstance(simulated_data, list) else [simulated_data]
        names = [data.name for data in simulated_data]
        colors = _init_colors(names)

        # Titles of the 5 plots
        titles = [
            "Cell Distance",
            "Cell Correlation",
            "Gene Correlation",
            "Cell Detection Frequency",
            "Gene Detection Frequency",
        ]

        # Get list of statistics (one per simulated dataset)
        stats_list = self._compute_general_statistics(real_data, simulated_data)

        # Extract values
        real_cell_distances = stats_list[0]["cell_distances"]["real_cell_distances"]
        sim_cell_distances = [
            _unwrap_array_if_wrapped(s["cell_distances"]["sim_cell_distances"]) for s in stats_list
        ]

        real_correlations_cell = stats_list[0]["correlations"]["real_correlations_cell"]
        sim_correlations_cell = [
            _unwrap_array_if_wrapped(s["correlations"]["sim_correlations_cell"]) for s in stats_list
        ]

        real_correlations_gene = stats_list[0]["correlations"]["real_correlations_gene"]
        sim_correlations_gene = [
            _unwrap_array_if_wrapped(s["correlations"]["sim_correlations_gene"]) for s in stats_list
        ]

        real_cell_detection_frequency = stats_list[0]["frequencies"]["real_cell_detection_frequency"]
        sim_detection_cell_frequencies = [
            _unwrap_array_if_wrapped(s["frequencies"]["sim_detection_cell_frequencies"]) for s in stats_list
        ]

        real_gene_detection_frequency = stats_list[0]["frequencies"]["real_gene_detection_frequency"]
        sim_detection_gene_frequencies = [
            _unwrap_array_if_wrapped(s["frequencies"]["sim_detection_gene_frequencies"]) for s in stats_list
        ]

        # Bundle all metrics together for easy plotting
        plot_configs = [
            ("Cell Distance", real_cell_distances, sim_cell_distances),
            ("Cell Correlation", real_correlations_cell, sim_correlations_cell),
            ("Gene Correlation", real_correlations_gene, sim_correlations_gene),
            ("Cell Detection Frequency", real_cell_detection_frequency, sim_detection_cell_frequencies),
            ("Gene Detection Frequency", real_gene_detection_frequency, sim_detection_gene_frequencies),
        ]

        # Prepare plots
        fig, axes = subplots(ncols=len(plot_configs), figsize=(4 * len(plot_configs), 4))
        dfs = []

        for title, real_vals, sim_vals in plot_configs:
            real_len = len(real_vals)
            sim_lens = [len(arr) for arr in sim_vals]

            if not all(l == real_len for l in sim_lens):
                raise ValueError(
                    f"❌ Length mismatch in '{title}':\n"
                    f"  - Real length: {real_len}\n"
                    f"  - Simulated lengths: {sim_lens}"
                )

            df = _build_statistical_dataframe(
                real_data=real_vals,
                simulated_data=sim_vals,
                names=names,
            )
            dfs.append(df)

        # Plot
        for ax, df, (title, _, _) in zip(axes, dfs, plot_configs):
            violinplot(data=df, ax=ax, palette=colors)
            ax.set_title(title)

        tight_layout()
        savefig(
            f"{self.GeneExpressionAnalysisParameters['output']}/statistical_gene_N_cell_analysis.png"
        )

    def comparison_analysis(self, real_data: BEAST_Data,
                            simulated_data: Union[BEAST_Data, List[BEAST_Data]]) -> None:
        """
        Benchmark real and simulated datasets by creating comparison plots.

        Args:
            real_data (BEAST_Data): The real dataset.
            simulated_data (Union[MOPITAS_Dataset, List[MOPITAS_Dataset]]): Simulated dataset(s).

        Returns:
            None
        """
        from matplotlib.pyplot import subplots, tight_layout, savefig, subplots_adjust
        from BEASTsim.utils.utils import _init_colors
        names = [data.name for data in simulated_data] if isinstance(simulated_data, list) else [simulated_data.name]
        colors = _init_colors(names)
        fig, axes = subplots(
            nrows=len(names), ncols=3, figsize=(16, 5 * len(names))
        )

        # Ensure simulated_data is always iterable
        if not isinstance(simulated_data, list):
            simulated_data = [simulated_data]

        for i, sim_data in enumerate(simulated_data):
            ax = axes[i] if len(names) > 1 else axes  # handles axes assignment
            self.comparison_plots(
                real_dataset=real_data,
                simulated_dataset=sim_data,
                ax=ax,
                name=sim_data.name,
                color=colors[sim_data.name]
            )

        tight_layout()
        subplots_adjust(left=0.1)
        savefig(f"{self.GeneExpressionAnalysisParameters['output']}/comparison_analysis.png")

    def comparison_plots(self, real_dataset: BEAST_Data, simulated_dataset: BEAST_Data,
                         ax: ndarray, name: str, color: str) -> None:
        """
        Generate comparison plots between real and simulated datasets.

        Args:
            real_dataset (BEAST_Data): The real dataset.
            simulated_dataset (BEAST_Data): The simulated dataset.
            ax (ndarray): The axes for the plots.
            name (str): The name to display on the plot.
            color (str): The color for the scatter plot.

        Returns:
            None
        """
        from numpy import max, log2, clip, inf
        from scipy.sparse import issparse

        # Convert sparse matrices to dense if needed, but don't modify the originals
        real_X = real_dataset.data.X.toarray() if issparse(real_dataset.data.X) else real_dataset.data.X
        sim_X = simulated_dataset.data.X.toarray() if issparse(simulated_dataset.data.X) else simulated_dataset.data.X

        # Compute mean and differences
        mean_counts = (real_X + sim_X) / 2
        diff_counts = sim_X - real_X

        # Bland-Altman plot
        ax[0].scatter(mean_counts, diff_counts, alpha=0.5, color=color)
        ax[0].axhline(0, color="black", linestyle="--")
        ax[0].set_xlabel("Mean of Real and Simulated Dataset Counts")
        ax[0].set_ylabel("Difference of Simulated and Real Dataset Counts")
        ax[0].set_title("Bland-Altman Plot")
        ax[0].grid(True)

        # Scatter plot of real vs simulated dataset counts
        ax[1].scatter(real_X, sim_X, alpha=0.5, color=color)
        max_val = max([max(real_X), max(sim_X)])
        ax[1].set_xlim(0, max_val)
        ax[1].set_ylim(0, max_val)
        ax[1].set_xlabel("Real Dataset Counts")
        ax[1].set_ylabel("Simulated Dataset Counts")
        ax[1].set_title("Scatterplot of Gene Counts")
        ax[1].grid(True)

        # Fold change scatterplot
        enumerator = clip(sim_X, 1e-10, inf)
        denominator = clip(real_X, 1e-10, inf)
        fold_change = log2(enumerator / denominator)
        ax[2].scatter(real_X, fold_change, alpha=0.5, color=color)
        ax[2].set_xlabel("Real Dataset Counts")
        ax[2].set_ylabel("Log Fold Change")
        ax[2].set_title("Fold Change Scatterplot")
        ax[2].grid(True)

        # Adding text label to Bland-Altman plot
        ax[0].text(
            -0.3,
            0.5,
            name,
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax[0].transAxes,
            fontsize=12,
            rotation=90,
        )

    def pearson_correlation_analysis(self,
                                     datas: List[BEAST_Data]
                                     ) -> None:
        """
        Performs a Pearson correlation benchmark on a list of datasets by calculating and
        visualizing the correlation matrices for each dataset.

        This function generates heatmaps of Pearson correlation coefficients for each dataset,
        with hierarchical clustering applied to reorder the variables in the first dataset.

        Args:
            datas (List[BEAST_Data]): A list of datasets to analyze.

        Returns:
            None
        """
        from matplotlib.pyplot import subplots, suptitle, tight_layout, savefig
        from scipy.spatial.distance import squareform
        from scipy.cluster.hierarchy import linkage, fcluster
        from scipy.stats import pearsonr
        from scipy.sparse import issparse
        from seaborn import heatmap
        from numpy import argsort
        from pandas import concat

        nplots = len(datas)
        if nplots == 1:
            fig, ax = subplots(figsize=(4, 4))
            axes = [ax]
        else:
            fig, axes = subplots(ncols=nplots, figsize=(4 * nplots, 4))

        for i, data in enumerate(datas):
            X = data.data.X
            if issparse(X):
                X = X.toarray()
            X = DataFrame(X)
            correlations = X.corr()

            if i != 0:
                for idx, j in enumerate(X.columns[labels_order]):
                    if idx == 0:
                        clustered = DataFrame(X[j])
                    else:
                        df_to_append = DataFrame(X[j])
                        clustered = concat([clustered, df_to_append], axis=1)

                correlations = clustered.corr()
                r_val, _ = pearsonr(
                    first_correlations.values.flatten(), correlations.values.flatten()
                )
            else:
                dissimilarity = 1 - abs(correlations)
                Z = linkage(squareform(dissimilarity), "complete")
                threshold = 0.8
                labels = fcluster(Z, threshold, criterion="distance")
                labels_order = argsort(labels)

                for idx, j in enumerate(X.columns[labels_order]):
                    if idx == 0:
                        clustered = DataFrame(X[j])
                    else:
                        df_to_append = DataFrame(X[j])
                        clustered = concat([clustered, df_to_append], axis=1)

                correlations = clustered.corr()
                first_correlations = correlations

            heatmap(
                round(correlations, 2),
                cmap="RdBu",
                vmin=-1,
                vmax=1,
                annot=False,
                fmt=".2f",
                xticklabels=False,
                yticklabels=False,
                ax=axes[i],
            )
            axes[i].set_title(data.name)
            if i != 0:
                axes[i].text(
                    0.5,
                    -0.1,
                    f"R = {r_val:.2f}",
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=axes[i].transAxes,
                )

        suptitle("Pearson Correlation Coefficients")
        tight_layout()
        savefig(f"{self.GeneExpressionAnalysisParameters['output']}/PearsonCorrelationBenchmark.png")
