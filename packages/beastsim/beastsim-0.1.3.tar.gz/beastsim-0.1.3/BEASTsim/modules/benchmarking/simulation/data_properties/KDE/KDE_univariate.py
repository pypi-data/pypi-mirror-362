import numpy as np
import scipy
import math
import scipy.optimize

class UnivariateKDETest():
    def __init__(self, parameters):
        self.parameters = parameters

    def run(self, real, sim) -> dict:
        """
        Perform the **univariate two-sample KDE test** proposed by Duong et al.
        (real vs simulated). The method automatically chooses bias-annihilating
        bandwidths for each sample, evaluates the test statistic

            T = φ₁₁ + φ₂₂ – φ₁₂ – φ₂₁,

        estimates the integral-squared error, and converts *T* into a Z-score
        using plug-in mean and standard-deviation estimators to obtain a
        one-sided *p*-value.

        **This Python implementation makes simplifications in the derivative
        estimates for the variance term compared with the original `ks` R
        routine; whenever possible use the R version for maximal accuracy.**

        Parameters
        ----------
        real : Sequence[float] | ndarray
            One-dimensional array of benchmark values from the real dataset.
        sim : Sequence[float] | ndarray
            One-dimensional array of benchmark values from the simulated dataset
            (length may differ from *real*).

        Returns
        -------
        dict
            Keys and meanings::

                T_stat        – raw KDE test statistic T
                Z_stat        – **negated** Z-normalised statistic
                p_val         – one-sided p-value
                mu_hat        – estimated null mean of T
                denom_squared – denominator used in Z computation
                var_hat_real  – variance estimate of real density derivative
                var_hat_sim   – variance estimate of simulated density derivative
                n_real / n_sim – sample sizes
                h_real / h_sim – bias-annihilating bandwidths
                phi_11, phi_22, phi_12, phi_21 – kernel integrals used in T

        References
        ----------
        Tarn Duong, Bruno Goud & Kristine Schauer (2012).
            *Closed-form density-based framework for automatic detection of
            cellular morphology changes.* PNAS 109, 8382–8387.
        """
        n_real = len(real)
        n_sim = len(sim)
        mean_real = np.mean(real)
        mean_sim = np.mean(sim)
        std_real = np.std(real)
        std_sim = np.std(sim)
        K0 = (2 * math.pi) ** (-0.5)
        h_real, h_sim, hder_real, hder_sim = self._get_bandwidths(real, sim, std_real, std_sim, n_real, n_sim, K0)
        phi_11, phi_22, phi_12, phi_21 = self._get_phi(h_real, real, h_sim, sim)
        T_stat = phi_11 + phi_22 - phi_12 - phi_21
        mu_hat = ((n_real * h_real) ** (-1) + (n_sim * h_sim) ** (-1)) * K0
        var_hat_real, var_hat_sim = self._get_var_hats(std_real, mean_real, real, hder_real, std_sim, mean_sim, sim, hder_sim)
        var_hat = (n_real * var_hat_real + n_sim * var_hat_sim) / (n_sim + n_real)
        num = T_stat - mu_hat
        denom = (3 * var_hat * (1 / n_real + 1 / n_sim)) ** (0.5)
        Z_stat = num / denom
        p_val = self._perform_test(Z_stat)
        results = {
            "T_stat": T_stat,
            "Z_stat": -Z_stat,
            "p_val": p_val,
            "mu_hat": mu_hat,
            "denom_squared": denom ** 2,
            "var_hat_real": var_hat_real,
            "var_hat_sim": var_hat_sim,
            "n_real": n_real,
            "n_sim": n_sim,
            "h_real": h_real,
            "h_sim": h_sim,
            "phi_11": phi_11,
            "phi_22": phi_22,
            "phi_12": phi_12,
            "phi_21": phi_21,
        }
        return results

    # PDF of Normal(mu,sigma)
    def _NormalPDF(self, x, mu, sigma):
        return (2 * math.pi) ** (-0.5) * np.exp(-(((x - mu) / sigma) ** 2) / 2.0) / sigma

    # Derivative of PDF of Normal(mu,sigma)
    def _NormalPDF_derivative(self, x, mu, sigma):
        return -self._NormalPDF(x, mu, sigma) * (x - mu) / (sigma ** 2)

    def _block_indices(self, nx, ny, block_limit=1e6):
        c = int(max(block_limit // nx, 1))
        l = np.arange(1, ny + c, c) - 1
        l[-1] = ny
        return l

    def _psins_1d(self, r, sigma):
        if r % 2 == 0:
            psins = (-1)**(r/2)*math.factorial(r)/((2*sigma)**(r+1)*math.factorial(r//2)*math.pi**(1/2))
        else:
            psins = 0
        return psins

    def _dnorm_deriv(self, x, mu=0, sigma=1, deriv_order=0):
        r = deriv_order
        phi = self._NormalPDF(x, mu, sigma)
        x = x - mu
        arg = x / sigma
        hmold0 = 1
        hmold1 = arg
        hmnew = 1
        if r == 1:
            hmnew = hmold1
        if r >= 2:
            for i in range(2, r+1):
                hmnew = arg * hmold1 - (i - 1) * hmold0
                hmold0 = hmold1
                hmold1 = hmnew
        derivt = (-1) ** r * phi * hmnew / sigma ** r
        return derivt

    def _dnorm_deriv_sum(self, sigma, x, deriv_order=0):
        r = deriv_order
        n = len(x)
        sumval = 0
        for i in range(n):
            sumval += np.sum(self._dnorm_deriv(x=x[i] - x, mu=0, sigma=sigma, deriv_order = r))
        sumval = sumval / n ** 2
        return sumval

    def _kfe_1d(self, x, g, deriv_order):
        r = deriv_order
        n = len(x)
        psir = self._dnorm_deriv_sum(x=x, sigma=g, deriv_order=r)
        return(psir)

    def _bias_annihliating_bandwidth(self, x, K0):
        n = len(x)
        r = int(0)
        k = 2
        Kr0 = K0
        mu2K = 1
        psi4_hat = self._psins_1d(r=int(r + k + 2), sigma=np.std(x))
        gamse2 = (math.factorial(r + 2) * Kr0 / (mu2K * psi4_hat * n)) ** (1 / (r + k + 3))
        psi2_hat = self._kfe_1d(x=x, g=gamse2, deriv_order=r + k)
        gamse = (math.factorial(r) * Kr0 / (-mu2K * psi2_hat * n)) ** (1 / (r + k + 1))
        return(gamse)

    def _get_bandwidths(self, real, sim, std_real, std_sim, n_real, n_sim, K0):
        h_real = self._bias_annihliating_bandwidth(real, K0)
        h_sim = self._bias_annihliating_bandwidth(sim, K0)
        hder_real = (((4 / 5) ** (2 / 7)) * (std_real ** 2) * (n_real ** (-2 / 7))) ** (0.5)
        hder_sim = (((4 / 5) ** (2 / 7)) * (std_sim ** 2) * (n_sim ** (-2 / 7))) ** (0.5)
        return h_real, h_sim, hder_real, hder_sim

    def _calc_phi_fast_1d(self, bandwidth, x, y):
        d = 1
        nx = len(x)
        ny = len(y)
        g = bandwidth
        n_seq = self._block_indices(nx, ny)
        phi = 0
        a = x ** 2
        for i in range(len(n_seq)-1):
            nytemp = n_seq[i + 1] - n_seq[i]
            ytemp = y[n_seq[i]:n_seq[i + 1]]
            aytemp = ytemp ** 2
            M = np.dot(a.reshape(-1, 1), np.ones(nytemp).reshape(1, -1)) + np.dot(np.ones(nx).reshape(-1, 1), aytemp.reshape(1, -1)) - 2 * np.dot(x.reshape(-1, 1),ytemp.reshape(1, -1))
            em2 = np.exp(-M / (2 * g ** 2))
            phi += (2 * math.pi) ** (-d / 2) * g ** (-1) * np.sum(em2)
        return phi / (nx * ny)

    def _get_phi(self, h_real, real, h_sim, sim):
        phi_11 = self._calc_phi_fast_1d(h_real, real, real)
        phi_22 = self._calc_phi_fast_1d(h_sim, sim, sim)
        phi_12 = self._calc_phi_fast_1d(h_real, real, sim)
        phi_21 = self._calc_phi_fast_1d(h_sim, real, sim)
        return phi_11, phi_22, phi_12, phi_21

    def _KDE(self, x, means, bandwidth):
        return (1 / len(means)) * np.sum(np.array([self._NormalPDF(x, means[i], bandwidth) for i in range(len(means))]))

    def _KDE_derivative(self, x, means, bandwidth):
        return (1 / len(means)) * np.sum(
            np.array([self._NormalPDF_derivative(x, means[i], bandwidth) for i in range(len(means))]))

    def _get_var_hats(self, std_real, mean_real, real, hder_real, std_sim, mean_sim, sim, hder_sim):
        var_hat_real = (std_real * self._KDE_derivative(mean_real, real, hder_real)) ** 2
        var_hat_sim = (std_sim * self._KDE_derivative(mean_sim, sim, hder_sim)) ** 2
        return var_hat_real, var_hat_sim

    def _perform_test(self, Z_stat):
        p_val = 1 - scipy.stats.norm.cdf(Z_stat)
        return p_val
