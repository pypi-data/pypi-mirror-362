from anndata import AnnData
from typing import Union, Optional
from numpy import ndarray, array
from tqdm import tqdm

class GenericDataProperties:
    def __init__(self, parameters):
        self.parameters = parameters
        self.generic_data_properties_parameters = self.parameters["Benchmarking"]["Simulation"]["DataProperties"]["GenericDataProperties"]

    def run(self, adata: Union[AnnData, ndarray]) -> tuple[dict, dict]:
        """
        Compute every univariate and bivariate **generic data-property benchmark**
        metric for a dataset in a single pass. Internally the method
        (i) converts the expression matrix to a *genes × cells* format,
        (ii) builds a set of random gene- and cell-index pairs for correlation
        benchmarks,
        (iii) executes the twelve univariate and three bivariate metric
        functions, and
        (iv) collects the raw arrays in two dictionaries.

        Parameters
        ----------
        adata : Union[AnnData, ndarray]
            Either an AnnData object (``adata.X`` is used as the count matrix)
            **or** a raw NumPy array whose rows are cells and columns are genes.

        Returns
        -------
        tuple[dict, dict]
            ``(univariate_results, bivariate_results)`` where each element is a
            dictionary ``{benchmark_name: ndarray}`` containing the raw metric
            vector (univariate) or 2-row matrix (bivariate) returned by the
            corresponding helper function.

        Raises
        ------
        TypeError
            If *adata* is neither an ``AnnData`` instance nor a NumPy ``ndarray``.

        References
        ----------
        Yue Cao, Pengyi Yang & Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).

        Charlotte Soneson & Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """
        if isinstance(adata, AnnData):
            counts = adata.X.T
        elif isinstance(adata, ndarray):
            counts = adata.T
        else:
            raise TypeError(f"adata must be a AnnData object or numpy array.")
        pairs_cells, pairs_genes = self.get_pairs(counts)
        univariate_benchmarks = [
            # gene related
            ("mean_expression", self.mean_expression, (counts,)),
            ("var_expression", self.var_expression, (counts,)),
            ("scaled_var_expression", self.scaled_var_expression, (counts,)),
            ("fraction_zero_genes", self.fraction_zero_genes, (counts,)),
            ("pearson_correlation_genes", self.pearson_correlation_genes, (counts, pairs_genes)),
            ("spearman_correlation_genes", self.spearman_correlation_genes, (counts, pairs_genes)),

            # cell related
            ("lib_size", self.lib_size, (counts,)),
            ("effective_lib_size", self.effective_lib_size, (counts,)),
            ("TMM", self.tmm, (counts,)),
            ("fraction_zero_cells", self.fraction_zero_cells, (counts,)),
            ("pearson_correlation_cells", self.pearson_correlation_cells, (counts, pairs_cells)),
            ("spearman_correlation_cells", self.spearman_correlation_cells, (counts, pairs_cells)),
        ]
        bivariate_benchmarks = [
            ("mean_vs_variance", self.mean_vs_variance, (counts,)),
            ("mean_vs_fraction_zero", self.mean_vs_fraction_zero, (counts,)),
            ("lib_size_vs_fraction_zero", self.lib_size_vs_fraction_zero, (counts,)),
        ]

        univariate_results = {}
        bivariate_results = {}

        total_iterations = len(univariate_benchmarks) + len(bivariate_benchmarks)
        with tqdm(total=total_iterations, desc="Running Generic Data Property Benchmarks", unit="step",
                  leave=False) as progress_bar:
            for key, benchmark_function, args in univariate_benchmarks:
                univariate_results[key] = benchmark_function(*args)  # Store results in a dictionary
                progress_bar.update(1)
            for key, benchmark_function, args in bivariate_benchmarks:
                bivariate_results[key] = benchmark_function(*args)  # Store results in a dictionary
                progress_bar.update(1)

        return univariate_results, bivariate_results

### Univariate ###
    def lib_size(self, x: ndarray) -> ndarray:
        """
        Calculates the total amount of genes in each cell of the count matrix.

        Parameters
        ----------
        x : ndarray
            Count matrix (*genes × cells*).

        Returns
        -------
        ndarray
            One scalar per cell (column) containing ``x.sum(axis=0)``.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).

        Charlotte Soneson & Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """

        r = x.sum(axis=0)
        return array(r)

    def tmm(self, x: ndarray) -> ndarray:
        """
        Calculates the **Trimmed Mean of M-values (TMM)** normalisation factors for each cell in the data matrix used for
        scaling library sizes. The result is a vector of values that can be multiplied by the columns (cells) of the count matrix
        to normalize the data. This normalization method accounts for differing library sizes across cells,
        focusing on gene expression proportions rather than absolute counts.

        Parameters
        ----------
        x : ndarray
            Count matrix (*genes × cells*).

        Returns
        -------
        ndarray
            1-D array of length *n_cells* containing the TMM factors.

        References
        ----------
        Mark D. Robinson & Alicia Oshlack.
            *A scaling normalization method for differential expression analysis
            of RNA-seq data.* Genome Biology 11, R25 (2010).

        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).

        Charlotte Soneson & Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """
        from numpy import sum, log2, argsort, intersect1d, mean, argmax, argmin, abs, quantile, exp, log

        # Function to calculate the empirical 75th quantile for each column of the count matrix
        def _calc_quantile(x: ndarray, p: float = 0.75) -> ndarray:
            n = x.shape[1]
            f = array([quantile(x[:, j], p) for j in range(n)])
            return f / self.lib_size(x)

        # Function to get the reference column for TMM normalization based on the 75th quantile
        def _get_ref_for_TMM(x: ndarray) -> int:
            from statistics import median
            f75 = _calc_quantile(x, p=0.75)
            if median(f75) < 10 ** (-20):
                ref_column = argmax(
                    sum(x ** (1 / 2), axis=0))  # Selects the column with the highest sum of square roots
            else:
                ref_column = argmin(
                    abs(f75 - mean(f75)))  # Selects the column closest to the mean of the quantiles
            return ref_column

        # Function to compute TMM between two vectors (gene expression values) using trimming and weighting
        def _TMM_between(Y_gk: ndarray, Y_gr: ndarray, trim_M: float = 0.3, trim_A: float = 0.05,
                        weighting: bool = True) -> float:

            N_k = sum(Y_gk)
            N_r = sum(Y_gr)
            fin = (Y_gk != 0) & (Y_gr != 0)
            Y_gk = Y_gk[fin]
            Y_gr = Y_gr[fin]

            M_gkr = log2((Y_gk / N_k) / (Y_gr / N_r))  # M-values (log fold changes)
            A_g = (log2(Y_gk / N_k) + log2(Y_gr / N_r)) / 2  # A-values (average log expression)
            w_gkr = (N_k - Y_gk) / N_k / Y_gk + (N_r - Y_gr) / N_r / Y_gr  # Weighting factors

            n = len(M_gkr)
            I_M = argsort(M_gkr)[int(n * trim_M):n - int(n * trim_M)]  # Indices after trimming M-values
            I_A = argsort(A_g)[int(n * trim_A):n - int(n * trim_A)]  # Indices after trimming A-values

            I = intersect1d(I_M, I_A)  # Intersection of trimmed M and A indices

            M_gkr = M_gkr[I]
            w_gkr = w_gkr[I]

            # If weighting is enabled, apply weights to M-values and compute the weighted mean, otherwise calculate the simple mean
            if weighting:
                f = sum(M_gkr / w_gkr) / sum(1 / w_gkr)
            else:
                f = mean(M_gkr)

            return 2 ** f

        # Get the reference column for normalization
        j = _get_ref_for_TMM(x)
        reference_column = x[:, j]

        # Calculate TMM normalization factor for each column (cell)
        f = array([_TMM_between(x[:, i], reference_column, trim_M=self.generic_data_properties_parameters["trim_M"], trim_A=self.generic_data_properties_parameters["trim_A"], weighting=self.generic_data_properties_parameters["weight_GE"]) for i in
                      range(x.shape[1])])

        # Normalize the TMM factors by the geometric mean of the TMM factors
        f = f / exp(mean(log(f)))

        return f

    def effective_lib_size(self, x: ndarray) -> ndarray:
        """
        Return the effective library size of every cell,
        i.e. ``lib_size(x) × tmm(x)``.

        Parameters
        ----------
        x : ndarray
            Count matrix (*genes × cells*).

        Returns
        -------
        ndarray
            Effective library size per cell.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).

        Charlotte Soneson & Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """
        from numpy import sum
        A = self.tmm(x)
        B = sum(x, axis=0)
        return B * A

    def mean_expression(self, x: ndarray) -> ndarray:
        """
        Compute the mean expression of each gene with optional CPM conversion
        and / or log-transformation, according to the class parameters.

        Parameters
        -----------
        x : ndarray
            Count matrix (*genes × cells*).

        Returns
        -------
        ndarray
            One mean value per gene (row).

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).

        Charlotte Soneson & Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import log2, mean
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])
        if self.generic_data_properties_parameters["use_log_sums"]:
            r = log2(mean(x, axis=1) + 1)
        else:
            r = mean(x, axis=1)
        return array(r)

    def var_expression(self, x: ndarray) -> ndarray:
        """
        Gene-wise sample variance calculated in raw counts, CPM, log counts,
        or log-CPM, according to the class parameters.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).

        Returns
        -------
        ndarray
            Variance per gene.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang.
            *A benchmark study of simulation methods for single-cell RNA-seq data.*
            Nature Communications 12, 6911 (2021).
        Charlotte Soneson and Mark D. Robinson.
            *Towards unified quality verification of synthetic count data with
            countsimQC.* Bioinformatics 34, 691–692 (2018).
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import var, log2
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])
        if self.generic_data_properties_parameters["use_log_sums"]:
            r = log2(var(x, axis=1) + 1)
        else:
            r = var(x, axis=1)
        return array(r)

    def scaled_var_expression(self, x: ndarray) -> ndarray:
        """
        Z-score–scaled version of ``var_expression``:
        ``(variance − mean(variance)) / std(variance)``.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).

        Returns
        -------
        ndarray
            Variance z-score per gene.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """
        from numpy import mean, std
        r = self.var_expression(x)
        z = (r - mean(r)) / std(r)
        return z

    def fraction_zero_cells(self, x: ndarray) -> ndarray:
        """
        For every cell, compute the fraction of genes with zero counts.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).

        Returns
        -------
        ndarray
            Length *n_cells*; values in [0, 1].

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """
        from numpy import sum
        n = len(x[:, 0])  # Number of genes (rows)
        m = len(x[0])  # Number of cells (columns)
        r = array([sum(x[:, i] == 0) / n for i in range(m)])  # Fraction of zero-expressed genes in each cell
        return r

    def fraction_zero_genes(self, x: ndarray) -> ndarray:
        """
        For every gene, compute the fraction of cells in which it is
        not expressed (zero counts).

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).

        Returns
        -------
        ndarray
            Length *n_genes*; values in [0, 1].

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """
        from numpy import sum
        n = len(x[0])  # Number of cells (columns)
        m = len(x[:, 0])  # Number of genes (rows)
        r = array([sum(x[i] == 0) / n for i in range(m)])  # Fraction of zero-expressed cells for each gene
        return r

    def pearson_correlation_cells(self, x: ndarray, pairs: ndarray) -> ndarray:
        """
        Compute the Pearson correlation between specified **cell pairs**.
        Counts can be converted to CPM and/or log-transformed, and the
        calculation can be restricted to the *top N* most variable genes,
        according to the class parameters.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        pairs : ndarray
            Array of shape (n_pairs, 2); each row ``[i, j]`` lists the indices
            of the two cells to correlate.

        Returns
        -------
        ndarray
            1-D array of length *n_pairs*; each element is the Pearson
            correlation coefficient for the corresponding cell pair.
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import std, cov, argsort
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])  # Apply CPM transformation if specified
        var_genes = x.var(axis=1)  # Compute variance for each row
        maxgene = min(self.generic_data_properties_parameters["top_genes"], x.shape[0])  # Take the minimum of 500 or the number of rows
        select_var = argsort(var_genes)[-maxgene:][::-1]
        x_selected = x[select_var,:].copy()
        r = []
        for i in range(len(pairs)):
            j = pairs[i][0]  # First cell index in the pair
            k = pairs[i][1]  # Second cell index in the pair
            if std(x_selected[:, k]) * std(x_selected[:, j]) > 0:  # Ensure no division by zero
                # Calculate the Pearson correlation coefficient
                r.append(cov(x_selected[:, j], x_selected[:, k])[0, 1] / (std(x_selected[:, k]) * std(x_selected[:, j])))
        return array(r)

    def pearson_correlation_genes(self, x: ndarray, pairs: ndarray) -> ndarray:
        """
        Calculate the Pearson correlation between **gene pairs** drawn from the
        count matrix. According to the class parameters, optionally converts
        counts to CPM or log-CPM.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        pairs : ndarray
            Array of gene-index pairs with shape (n_pairs, 2).

        Returns
        -------
        ndarray
            A 1-D array of length *n_pairs*; each element is the Pearson
            correlation for the corresponding gene pair.
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import std, cov
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])  # Apply CPM transformation if specified

        r = []
        for i in range(len(pairs)):
            j, k = pairs[i]  # Gene indices in the pair
            if (std(x[k]) * std(x[j])) > 0:  # Ensure no division by zero
                # Calculate the Pearson correlation coefficient
                r.append(cov(x[j], x[k])[0, 1] / (std(x[k]) * std(x[j])))
        return array(r)

    def spearman_correlation_cells(self, x: ndarray, pairs: ndarray) -> ndarray:
        """
        Spearman rank correlation between a set of cell pairs. The method ranks
        expression values for the selected genes and then applies the Pearson
        correlation formula to the rank vectors.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        pairs : ndarray
            Cell-index pairs (n_pairs, 2).

        Returns
        -------
        ndarray
            A 1-D array of length *n_pairs*; each element is the Spearman rank
            correlation for the corresponding cell pair.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021)
        Charlotte Soneson and Mark D. Robinson (2018)
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import argsort, std, cov
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])  # Apply CPM transformation if specified
        var_genes = x.var(axis=1)  # Compute variance for each row
        maxgene = min(self.generic_data_properties_parameters["top_genes"], x.shape[0])  # Top 500 most variable genes
        select_var = argsort(var_genes)[-maxgene:][::-1]
        x_selected = x[select_var,:].copy()
        x_selected = argsort(x_selected, axis=0)  # Rank the values in each cell (column)
        r = []
        for i in range(len(pairs)):
            j, k = pairs[i]  # Cell indices in the pair
            if std(x_selected[:, k]) * std(x_selected[:, j]) > 0:  # Ensure no division by zero
                # Calculate the Pearson correlation of the rank vectors (Spearman correlation)
                r.append(cov(x_selected[:, j], x_selected[:, k])[0, 1] / (std(x_selected[:, k]) * std(x_selected[:, j])))
        return array(r)

    def spearman_correlation_genes(self, x: ndarray, pairs: ndarray) -> ndarray:
        """
        Spearman rank correlation for each **gene pair**, obtained by ranking each
        gene’s expression across cells and computing the Pearson correlation of
        those ranks.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        pairs : ndarray
            Gene-index pairs (n_pairs, 2).

        Returns
        -------
        ndarray
            Spearman correlation coefficients, one per gene pair.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021)
        Charlotte Soneson and Mark D. Robinson (2018)
        """
        from BEASTsim.utils.utils import _cpm
        from numpy import argsort, cov, std
        if self.generic_data_properties_parameters["use_CPM"]:
            x = _cpm(x, log=self.generic_data_properties_parameters["use_log"])  # Apply CPM transformation if specified
        x = argsort(x, axis=1)  # Rank the values in each gene (row)
        r = []
        for i in range(len(pairs)):
            j, k = pairs[i]  # Gene indices in the pair
            if std(x[k]) * std(x[j]) > 0:  # Ensure no division by zero
                # Calculate the Pearson correlation of the rank vectors (Spearman correlation)
                r.append(cov(x[j], x[k])[0, 1] / (std(x[k]) * std(x[j])))
        return array(r)

    def get_pairs_cells(self, x: ndarray, k = 100) -> list[list[int]]:
        """
        Randomly sample up to *k* distinct cells and return all pairwise
        combinations among them, used for selecting pairs for cell-correlation
        metrics.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        k : int, default 100
            Maximum number of cells to sample.

        Returns
        -------
        list[list[int]]
            List of [i, j] index pairs (length ≤ k choose 2).
        """
        from random import sample
        from itertools import combinations
        n = len(x[0])  # Number of cells (columns)
        indices = list(range(n))
        if n > k:
            sampled_indices = sample(indices, k)
        else:
            sampled_indices = indices
        pairs_cells = list(combinations(sampled_indices, 2))
        return pairs_cells

    def get_pairs_genes(self, x: ndarray) -> list[list[int]]:
        """
        Select the top most-variable genes (the number depends on the
        ``parameters["select_genes"]`` class parameter) and return all pairwise
        combinations of their indices. Used for selecting pairs for
        gene-correlation metrics.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).

        Returns
        -------
        list[list[int]]
            List of gene-index pairs for correlation analysis.
        """
        from numpy import argsort, var
        from itertools import combinations
        row_vars = var(x, axis=1)
        cpms = x[row_vars > 0, :].copy()
        var_genes = var(cpms, axis=1)
        maxgene = min(self.generic_data_properties_parameters["select_genes"], cpms.shape[0])
        select_var = argsort(var_genes)[-maxgene:][::-1]  # Sort in descending order
        pairs_genes = list(combinations(select_var, 2))
        return pairs_genes

    def get_pairs(self, x: ndarray, pairs_cells: Optional[ndarray] = None,
                  pairs_genes: Optional[ndarray] = None) -> tuple:
        """
        Convenience wrapper that returns both cell pairs *and* gene pairs—either
        the user-supplied lists or freshly generated via ``get_pairs_cells`` or
        ``get_pairs_genes`` if either ``pairs_cells`` or ``pairs_genes`` is None.

        Parameters
        ----------
        x : ndarray
            Count matrix (genes × cells).
        pairs_cells : Optional[ndarray], default None
            Pre-computed cell pairs to reuse; if None they are generated by this function.
        pairs_genes : Optional[ndarray], default None
            Pre-computed gene pairs to reuse; if None they are generated by this function.

        Returns
        -------
        tuple[list[list[int]], list[list[int]]]
            (pairs_cells, pairs_genes)
        """

        if pairs_cells is None:
            pairs_cells = self.get_pairs_cells(x, k=self.generic_data_properties_parameters["select_cells"])  # Generate random pairs of cells if not provided
        if pairs_genes is None:
            pairs_genes = self.get_pairs_genes(x)  # Generate random pairs of genes if not provided
        return pairs_cells, pairs_genes

    ### Bivariate ###

    def mean_vs_variance(self, x: ndarray) -> ndarray:
        """
        Bivariate data property, returning for every gene its mean expression
        and its variance combined as a 2 × N array.

        Parameters
        ----------
        x : ndarray
            Count matrix.

        Returns
        -------
        ndarray
            A 2 × N array where row 0 = mean gene expression,
            row 1 = variance per gene.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """
        r0 = self.mean_expression(x)
        r1 = self.var_expression(x)
        return array([r0, r1])

    def mean_vs_fraction_zero(self, x: ndarray) -> ndarray:
        """
        Bivariate data property, returning for every gene its mean expression
        and its fraction of zero counts combined as a 2 × N array.

        Parameters
        ----------
        x : ndarray
            Count matrix.

        Returns
        -------
        ndarray
            2 × N array: row 0 = mean gene expression,
            row 1 = fraction of zero counts.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """
        r0 = self.mean_expression(x)
        r1 = self.fraction_zero_genes(x)
        return array([r0, r1])

    def lib_size_vs_fraction_zero(self, x: ndarray) -> ndarray:
        """
        Bivariate data property, returning for every cell its library size and
        its fraction of zero-expressed genes combined as a 2 × M array.

        Parameters
        ----------
        x : ndarray
            Count matrix.

        Returns
        -------
        ndarray
            2 × M array: row 0 = library size per cell,
            row 1 = fraction of zero counts per cell.

        References
        ----------
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        Charlotte Soneson and Mark D. Robinson (2018).
        """

        r0 = self.lib_size(x)
        r1 = self.fraction_zero_cells(x)
        return array([r0, r1])
