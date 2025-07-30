import os, warnings
os.environ["RPY2_CFFI_MODE"] = "ABI"
warnings.filterwarnings("ignore",
                        message="Environment variable \"PATH\" redefined",
                        module="rpy2.rinterface")
from numpy import array, ndarray
from pandas import DataFrame
from tqdm import tqdm
from typing import Optional

class KDE:
    def __init__(self, parameters):
        self.parameters = parameters

        # Imports
        from BEASTsim.modules.benchmarking.simulation.data_properties.KDE.KDE_univariate import UnivariateKDETest
        from BEASTsim.modules.benchmarking.simulation.data_properties.KDE.KDE_multivariate import MultivariateKDETest

        # Modules
        self.univariate_kde_test = UnivariateKDETest(self.parameters)
        self.multivariate_kde_test = MultivariateKDETest(self.parameters)

    def run(self, univariate_real, bivariate_real, univariate_sim, bivariate_sim, stats_type): # TODO: Simplify this functions input and move the data transformation out of this function, and update function description
        """
        Assemble the full KDE / KS test score table comparing data properties of
        a simulation and the reference data. Univariate metrics are handled
        separately from bivariate ones; the chosen statistic (T-stat = 0,
        Z-stat = 1, p-value = 2) is taken from either the R implementation
        (``use_R=True``) or the internal Python implementation.  Three ``None``
        placeholders pad the KS column because for bivariate metrics the KS test
        is not applicable.

        Parameters
        ----------
        univariate_real : dict[str, Any]
            Raw univariate benchmark arrays for the real dataset
            (``{"mean_expression": ndarray, …}``).
        bivariate_real : dict[str, Any]
            Raw bivariate benchmark arrays for the real dataset.
        univariate_sim : dict[str, Any]
            Same structure as *univariate_real* but for the simulation.
        bivariate_sim : dict[str, Any]
            Same structure as *bivariate_real* for the simulation.
        stats_type : int | str
            Index of the KDE statistic to extract
            (0 = T-statistic, 1 = –Z-statistic, 2 = p-value).

        Returns
        -------
        DataFrame
            Two columns—``"KDE_Score"`` and ``"KS_Score"``—indexed by the 15
            benchmark names.  The KS column contains real values for univariate
            metrics and ``None`` for the three bivariate ones.

        References
        ----------
        Tarn Duong, Bruno Goud, and Kristine Schauer (2012).
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        """
        from numpy import concatenate
        if self.parameters["use_R"]:
            kde_score_univariate = self.kde_score_with_R(benchmarks_real=list(univariate_real.values()), benchmarks_sim=list(univariate_sim.values()), stats_type=stats_type)
            kde_score_multivariate = self.kde_score_with_R(benchmarks_real=list(bivariate_real.values()), benchmarks_sim=list(bivariate_sim.values()), stats_type=stats_type)
        else:
            kde_score_univariate = self.kde_score(benchmarks_real=list(univariate_real.values()), benchmarks_sim=list(univariate_sim.values()), stats_type=stats_type)
            kde_score_multivariate = self.kde_score(benchmarks_real=list(bivariate_real.values()), benchmarks_sim=list(bivariate_sim.values()), stats_type=stats_type)

        kde_score = concatenate((kde_score_univariate, kde_score_multivariate))

        ks_score = self.ks_score(list(univariate_real.values()), list(univariate_sim.values()), stats_type=stats_type)
        ks_score = concatenate((ks_score, array([None, None, None])))  # Add placeholders for bivariate KS scores

        data = {
            "KDE_Score": kde_score,
            "KS_Score": ks_score
        }
        names = list(univariate_real.keys()) + list(bivariate_real.keys())
        df = DataFrame(data, index=names)
        return df

    def kde_test(self, real: ndarray, sim: ndarray) -> list:
        """
        Run the Python KDE test implementation on two one-dimensional arrays
        (univariate) or on two multi-dimensional arrays (multivariate), automatically
        delegating to ``UnivariateKdeTest.run()`` or ``MultivariateKdeTest.run()``.

        Parameters
        ----------
        real : ndarray
            Benchmark values from the real dataset; shape N or N × D.
        sim : ndarray
            Corresponding benchmark values from the simulation.

        Returns
        -------
        list
            ``[T_stat, Z_stat, p_val]`` for the chosen test.

        References
        ----------
        Tarn Duong, Bruno Goud, and Kristine Schauer (2012).
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        """
        if len(real.shape) > 1:
            # Use multivariate KDE test if the input data is multivariate (2D or higher)
            results = self.multivariate_kde_test.run(real, sim)
        else:
            # Use univariate KDE test if the input data is univariate (1D)
            results = self.univariate_kde_test.run(real, sim)

        # Return the relevant results: T statistic, -Z normalized test statistic, P-value from the KDE test
        result = [
            results["T_stat"],
            results["Z_stat"],
            results["p_val"],
        ]
        return result

    def kde_test_with_R(self, x: ndarray, y: ndarray, print: bool = False) -> list:
        """
        Perform the KDE test via the ks package in R (``ks::kde.test()``).  Returns
        either the essential three or the full DataFrame of the values used in
        the test.

        Parameters
        ----------
        x : ndarray
            Real benchmark array (univariate or multivariate).
        y : ndarray
            Simulated benchmark array (univariate or multivariate).
        print : bool, default False
            If True, return a DataFrame with 15 diagnostic fields; otherwise
            return ``[T_stat, –Z_stat, p_val]``.

        Returns
        -------
        list | DataFrame
            Concise list or verbose DataFrame, depending on *print*.
            - If `print` is False, returns a list with the following elements:
              - T statistic
              - Negative Z-statistic (normalised version of T_stat, negative so that later on the scores follows the larger the better principle)
              - P-value (p-value of the double-sided test)
            - If `print` is True, returns a pandas DataFrame with the following columns:
              - T_stat (T statistic)
              - Z_stat (Z statistic - normalised version of T_stat)
              - p_val (p-value of the double-sided test)
              - mu_hat (mean of null distribution)
              - var (variance of null distribution)
              - var_hat_real (variance estimate for real data)
              - var_hat_sim (variance estimate for simulated data)
              - n_real (sample size for real data)
              - n_sim (sample size for simulated data)
              - h_real (selected bandwidth for real data)
              - h_sim (selected bandwidth for simulated data)
              - phi_11, phi_12, phi_21, phi_22 (kernel functional estimates)

        References
        ----------
        Tarn Duong, Bruno Goud, and Kristine Schauer (2012).
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        """
        from rpy2.robjects.packages import importr
        ksr = importr('ks')
        import rpy2.robjects as ro
        from rpy2.robjects import numpy2ri, pandas2ri
        from rpy2.robjects.conversion import localconverter
        np_pd_converter = ro.default_converter + numpy2ri.converter + pandas2ri.converter

        with localconverter(np_pd_converter):
            if x.ndim == 1:
                real = ro.FloatVector(x)
                sim = ro.FloatVector(y)
            else:
                real = ro.conversion.py2rpy(x.T)
                sim = ro.conversion.py2rpy(y.T)

        # Perform the KDE test using R's ks package
        results = ksr.kde_test(real, sim)

        if print:
            names = ['T_stat', 'Z_stat', 'p_val', 'mu_hat', 'var',
                     'var_hat_real', 'var_hat_sim', 'n_real', 'n_sim',
                     'h_real', 'h_sim', 'phi_11', 'phi_12', 'phi_21', 'phi_22']
            d = [results.rx2('Tstat')[0], results.rx2('zstat')[0], results.rx2('pvalue')[0], results.rx2('mean')[0],
                 results.rx2('var')[0], results.rx2('var.fhat1')[0], results.rx2('var.fhat2')[0], results.rx2('n1')[0],
                 results.rx2('n2')[0], results.rx2('H1'),
                 results.rx2('H2'), results.rx2('psi1')[0], results.rx2('psi12')[0], results.rx2('psi21')[0],
                 results.rx2('psi2')[0]]
            data = {
                "KDE_Test_Data": d
            }
            result = DataFrame(data, index=names)
        else:
            result = [results.rx2('Tstat')[0], -results.rx2('zstat')[0], results.rx2('pvalue')[0]]
        return result

    def ks_test(self, real: ndarray, sim: ndarray) -> tuple:
        """
        Wrapper around SciPy’s two-sided Kolmogorov–Smirnov test for two
        one-dimensional samples.

        Parameters
        ----------
        real : ndarray
            1-D array of data-property values of the real data.
        sim : ndarray
            1-D array of data-property values of the simulated data.

        Returns
        -------
        tuple[float, float]
            (statistic, p_value)
        """
        from scipy.stats import kstest
        # Convert the inputs to numpy arrays
        x = array(real)
        y = array(sim)

        # Perform the Kolmogorov-Smirnov test
        return kstest(x, y, alternative='two-sided')

    def kde_score_with_R(self, benchmarks_real: list[ndarray], benchmarks_sim: list[ndarray], stats_type: int = 2) -> ndarray:
        """
        Compute the selected KDE statistic for *each* benchmark using the R
        implementation and return them as a single NumPy vector.

        Parameters
        ----------
        benchmarks_real : list[ndarray]
            Data-property arrays of real data.
        benchmarks_sim : list[ndarray]
            Data-property arrays of simulated data.
        stats_type : int, default 2
            0 = T, 1 = –Z, 2 = p.

        Returns
        -------
        ndarray
            Length = ``len(benchmarks_real)``.

        References
        ----------
        Tarn Duong, Bruno Goud, and Kristine Schauer (2012).
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        """
        v = array(
            [self.kde_test_with_R(benchmarks_real[i], benchmarks_sim[i])[stats_type] for i in range(len(benchmarks_real))])
        return v

    def kde_score(self, benchmarks_real: list[ndarray], benchmarks_sim: list[ndarray], stats_type: int = 2) -> ndarray:
        """
        Compute the selected KDE statistic for *each* benchmark using our Python
        implementation and return them as a single NumPy vector.

        Parameters
        ----------
        benchmarks_real : list[ndarray]
            Data-property arrays of real data.
        benchmarks_sim : list[ndarray]
            Data-property arrays of simulated data.
        stats_type : int, default 2
            Statistic index to extract.

        Returns
        -------
        ndarray
            Selected statistic for each benchmark.

        References
        ----------
        Tarn Duong, Bruno Goud, and Kristine Schauer (2012).
        Yue Cao, Pengyi Yang, and Jean Yee Hwa Yang (2021).
        """
        v = array([self.kde_test(benchmarks_real[i], benchmarks_sim[i])[stats_type] for i in tqdm(range(len(benchmarks_real)), desc="Computing KDE scores", leave=False)])
        return v

    def ks_score(self, benchmarks_real: list[ndarray], benchmarks_sim: list[ndarray], stats_type: int = 2) -> ndarray:
        """
        Collect KS-test statistics over all data-property benchmarks.
        ``stats_type < 2`` returns the statistic, ``stats_type >= 2`` returns the
        p-value.

        Parameters
        ----------
        benchmarks_real : list[ndarray]
            Data-property arrays of real data.
        benchmarks_sim : list[ndarray]
            Data-property arrays of simulated data.
        stats_type : int, default 2
            Selector for statistic vs p_value.

        Returns
        -------
        ndarray
            1-D array of KS statistics or p-values.
        """
        if stats_type < 2:
            j = 0
        else:
            j = 1
        v = array([self.ks_test(benchmarks_real[i], benchmarks_sim[i])[j] for i in range(len(benchmarks_real))])
        return v

    def kde_comparrison(self, real: ndarray, sim: ndarray, multi: Optional[bool] = True) -> DataFrame:
        """
        This function is only for testing purposes.
        Compares the Kernel Density Estimation (KDE) results of two datasets (`real` and `sim`) using both Python and R implementations of KDE tests.

        This function performs two KDE tests: one using a Python-based KDE test (`KDE_test`) and another using an R-based KDE test (`KDE_test_withR`), and then returns a DataFrame that combines the results from both tests for comparison.

        Args:
            real (ndarray or list): The real dataset to be tested. Can be a 1D numpy array or list.
            sim (ndarray or list): The simulated dataset to be tested. Can be a 1D numpy array or list.
            multi (bool, optional): If `True`, returns the detailed KDE test results from R. If `False`, returns only specific results. Default is `True`.

        Returns:
            DataFrame: A DataFrame containing the KDE test results from both Python and R KDE results for comparison.
        """
        # Perform KDE test using the Python implementation
        x = self.kde_test(real, sim)

        # Perform KDE test using the R implementation
        y = self.kde_test_with_R(real, sim)

        # Define the names for the results
        names = ['T_stat', 'Z_stat', 'p_val', 'mu_hat', 'var_hat', 'var_hat_real', 'var_hat_sim', 'n_real', 'n_sim',
                 'H_real', 'H_sim', 'phi_11', 'phi_12', 'phi_21', 'phi_22']

        # Get the R results
        result = y.rx2

        # Combine the results based on the `multi` parameter
        if multi:
            combined = (
                result('Tstat')[0], result('zstat')[0], result('pvalue')[0], result('mean')[0], result('var')[0],
                result('var.fhat1')[0], result('var.fhat2')[0], result('n1')[0], result('n2')[0], result('H1'),
                result('H2'), result('psi1')[0], result('psi12')[0], result('psi21')[0], result('psi2')[0]
            )
        else:
            combined = (
                result('Tstat')[0], result('zstat')[0], result('pvalue')[0], result('mean')[0], result('var')[0],
                result('var.fhat1')[0], result('var.fhat2')[0], result('n1')[0], result('n2')[0], result('h1'),
                result('h2'), result('psi1')[0], result('psi12')[0], result('psi21')[0], result('psi2')[0]
            )

        # Create a DataFrame with the combined results
        data = {
            "KDE_py": x,
            "KDE_R": combined
        }

        # Return the results as a DataFrame
        df = DataFrame(data, index=names)
        return df
