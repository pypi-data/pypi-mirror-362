import numpy as np
import pandas as pd
import scipy
import math
from scipy.linalg import cholesky, cho_solve, solve_triangular
import scipy.optimize

class MultivariateKDETest():
    def __init__(self, parameters):
        self.parameters = parameters
        self.c = 0

    def run(self, real, sim):
        """
        Multivariate (dimension ≥ 2) two-sample KDE test.

        Accepts matrices of shape ``(d, n)`` where *d* is the number of benchmark
        variables and *n* the number of observations. Bandwidth covariance
        matrices are selected via the bias-annihilating procedure of
        Duong & Hazelton (2005).

        **This Python implementation simplifies derivative estimates for the
        variance term relative to the original `ks` R routine; use the R version
        when maximal accuracy is required.**

        Parameters
        ----------
        real : ndarray
            Real benchmark matrix of shape ``d × n_real``.
        sim : ndarray
            Simulated benchmark matrix **with the same dimensionality**
            ``d × n_sim``.

        Returns
        -------
        dict
            Same keys as the univariate version except that ``h_real`` and
            ``h_sim`` are full bandwidth covariance matrices (d × d).

        Raises
        ------
        ValueError
            If *real* and *sim* have different numbers of rows (*d*).

        References
        ----------
        Tarn Duong, Bruno Goud & Kristine Schauer (2012).
        Duong, T. & Hazelton, M. L. (2005). *Cross-validation bandwidth matrices
        for multivariate kernel density estimation.* Scand. J. Stat. 32, 485–506.
        """
        real_T, sim_T = self._get_transpose(real, sim)
        n_real = real.shape[1]
        n_sim = sim.shape[1]
        if not real.shape[0] == sim.shape[0]:
            raise ValueError("Real and sim must be the same shape")
        d = real.shape[0]
        K0 = self._NormalDensityDerivative(np.zeros(d))
        cov_real = np.cov(real)
        cov_sim = np.cov(sim)
        mean_real = np.mean(real, axis=1)
        mean_sim = np.mean(sim, axis=1)
        h_real, h_sim, hder_real, hder_sim = self._get_bandwidths_advanced(real_T, sim_T, d, n_real, n_sim, cov_real, cov_sim, K0)
        phi_11, phi_22, phi_12, phi_21 = self._get_phi(h_real, real_T, h_sim, sim_T)
        T_stat = phi_11 + phi_22 - phi_12 - phi_21
        mu_hat = ((1 / (n_real * np.sqrt(np.linalg.det(h_real)))) + (1 / (n_sim * np.sqrt(np.linalg.det(h_sim))))) * K0
        var_hat_real, var_hat_sim = self._get_var_hats(mean_real, real_T, hder_real, cov_real, mean_sim, sim_T, hder_sim, cov_sim)  # this is the part that is simpler than the R version, it's the reason why I recommend using that if possible
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


    def _cholesky_inverse(self, M):
        return cho_solve((cholesky(M, lower=True), True), np.eye(M.shape[0]))

    def _NormalDensityDerivative(self, x, mu=None, Sigma=None, order=0):
        d = len(x)
        if mu is None and Sigma is not None:
            mu = np.zeros(d)
        if Sigma is None and mu is not None:
            Sigma = np.eye(d)
        if mu is None and Sigma is None:
            c = 1 / np.sqrt((2 * math.pi) ** d)
            g = np.exp(-0.5 * x @ x)
            res = c * g
            if order == 1:
                res = -res * x
        else:
            c = 1 / np.sqrt(np.linalg.det(Sigma) * (2 * math.pi) ** d)
            inv = self._cholesky_inverse(Sigma)
            y = x - mu
            g = np.exp(-0.5 * (y @ inv @ y))
            res = c * g
            if order == 1:
                res = -res * inv @ y
        return res

    def _matrix_ij(self, i, j, n):
        M = np.zeros((n, n))
        if i != j:
            M[i][j] = 1
            M[j][i] = 1
        else:
            M[i][i] = 2
        return M


    def _matrix_xi(self, x, i):
        n = len(x)
        M = np.zeros((n, n))
        for k in range(n):
            M[k][i] += x[k]
        for k in range(n):
            M[i][k] += x[k]
        return M


    def _matrix_xixj(self, x, i, j):
        n = len(x)
        M = np.zeros((n, n))
        if i != j:
            for k in range(n):
                M[k][j] += x[k] * x[j]
            for k in range(n):
                M[i][k] += x[k] * x[i]
        else:
            M += np.dot(x.reshape(-1, 1), x.reshape(1, -1))
            for k in range(n):
                M[k][j] += x[k] * x[j]
            for k in range(n):
                M[i][k] += x[k] * x[i]
        return M


    def _get_derivatives(self, x):
        d = len(x)
        x2 = np.tensordot(x, x, axes=0)
        x3 = np.tensordot(x, x2, axes=0)
        x4 = np.tensordot(x, x3, axes=0)
        x2_der1 = np.array([self._matrix_xi(x, i) for i in range(d)])
        x3_der1 = np.array([[self._matrix_xixj(x, i, j) for i in range(d)] for j in range(d)])
        x2_der2 = np.array([[self._matrix_ij(i, j, d) for i in range(d)] for j in range(d)])
        return x2, x3, x4, x2_der1, x3_der1, x2_der2

    def _dmvnorm_deriv(self, x, order=0):
        d = len(x)
        x2, x3, x4, x2_der1, x3_der1, x2_der2 = self._get_derivatives(x)
        phix = self._NormalDensityDerivative(x, mu=None, Sigma=None, order=0)
        res = 0
        if order == 0:
            res = phix
        elif order == 1:
            res = -phix * x
        elif order == 2:
            res = phix * (x2 - np.eye(d))
        elif order == 3:
            res = phix * (np.tensordot(x, np.eye(d), axes=0) - x3 + x2_der1)
        elif order == 4:
            res = phix * (x4 - np.tensordot(x, x2_der1, axes=0) - np.tensordot(x2, np.eye(d),
                                                                               axes=0) - x3_der1 + x2_der2 + np.tensordot(
                x2, np.eye(d), axes=0) + np.tensordot(np.eye(d), np.eye(d), axes=0))
        return res

    def _full_derivative(self, x, mu, Sigma, order=0):
        x = x - mu
        L = cholesky(Sigma, lower=True)
        H_inv_sqrt = solve_triangular(L, np.eye(L.shape[0]), lower=True)
        K_Hx = self._dmvnorm_deriv(H_inv_sqrt @ x, order=order)
        H_inv_sqrt_det = np.absolute(np.linalg.det(Sigma)) ** (0.5)
        res = H_inv_sqrt_det * K_Hx @ np.linalg.matrix_power(H_inv_sqrt, order)
        return res

    def _matrix_sqrt(self, A):
        if len(A) == 1: return (np.sqrt(A))
        U, singular_values, Vt = np.linalg.svd(A)
        if min(singular_values) >= 0:
            Asqrt = (U @ np.diag(np.sqrt(singular_values))) @ Vt.T
        return Asqrt

    def _pre_sphere(self, x):
        S = np.cov(x.T)
        Sinv12 = self._matrix_sqrt(self._cholesky_inverse(S))
        x_sphered = x
        x_sphered = x_sphered @ Sinv12
        return (x_sphered)

    def _get_transpose(self, real, sim):
        x = np.copy(real)
        y = np.copy(sim)
        return x.T, y.T

    def _kronecker_power(self, M, r):
        K = M.copy()
        if r == 1:
            return M
        else:
            for i in range(r - 1):
                M = np.kron(M, K)
            return M

    def _psins(self, r, Sigma):
        d = Sigma.shape[1]
        dens = self._full_derivative(x=np.zeros(d), mu=np.zeros(d), order=r, Sigma=2 * Sigma).flatten()
        return dens

    def _kfe_fast(self, x, bandwidth):
        d = x.shape[1]
        nx = x.shape[0]
        G = bandwidth
        Ginv = cho_solve((cholesky(G, lower=True), True), np.eye(G.shape[0]))
        detG = np.linalg.det(G)
        L = cholesky(bandwidth, lower=True)
        H_inv_sqrt = solve_triangular(L, np.eye(L.shape[0]), lower=True)
        H2 = np.linalg.matrix_power(H_inv_sqrt, 2)
        X = (H_inv_sqrt @ (x.T)).T
        xG = np.dot(x, Ginv)
        a = np.sum(xG * x, axis=1)
        aytemp = np.sum(np.dot(x, Ginv) * x, axis=1)
        M = np.dot(a.reshape(-1, 1), np.ones(nx).reshape(1, -1)) + np.dot(np.ones(nx).reshape(-1, 1),
                                                                          aytemp.reshape(1, -1)) - 2 * np.dot(xG, x.T)
        em2 = np.exp(-M / 2)
        em2 = em2[:, :, np.newaxis, np.newaxis]
        eye = np.eye(d)
        ten0 = np.array([[X[i] - X[j] for i in range(nx)] for j in range(nx)])
        reshaped_vectors = ten0.reshape(-1, 2)
        outer_products = np.einsum('ij,ik->ijk', reshaped_vectors, reshaped_vectors)-eye
        ten = outer_products.reshape(nx, nx, d, d)
        phi = (2 * math.pi) ** (-d / 2) * detG ** (-1 / 2) * np.sum(em2 * ten, axis=(0, 1)) @ H2 / nx ** 2
        return phi

    def _bias_annihliating_bandwidth_STAGE1(self, x, K0):
        n = x.shape[0]
        d = x.shape[1]
        r = int(0)
        x_star = self._pre_sphere(x)
        S12 = self._matrix_sqrt(np.cov(x.T))
        Sinv12 = self._cholesky_inverse(S12)
        D2K0 = self._dmvnorm_deriv(np.zeros(d), order=2).flatten().T
        K02 = K0
        psi4_ns = self._psins(r=r + 4, Sigma=np.cov(x_star.T))
        A1 = D2K0.T @ D2K0
        A2 = D2K0.T @ np.kron(np.eye(d).flatten(), np.eye(d ** 2)) @ psi4_ns
        A3 = psi4_ns.T @ (np.kron(np.diag(np.diag(np.ones(d)).flatten()), np.diag(np.ones(d ** 2))) @ psi4_ns)
        h2 = (-A1 / (2 * A2 * n)) ** (1 / (d + 4))
        H2 = h2 ** 2 * np.eye(d)
        psi2_hat = self._kfe_fast(x=x_star, bandwidth=H2).flatten()
        return A1, A2, A3, psi2_hat, K02, D2K0, S12, Sinv12, x_star, psi4_ns

    def _vech(self, H):
        d = H.shape[1]
        vechx = np.array([])
        for j in range(d):
            vechx = np.append(vechx, H[j:d, j])
        return vechx
        # return H[np.triu_indices(len(H))]

    def _invvech(self, x):
        if len(x) == 1:
            return np.array([[x[0]]])
        d = (-1 + (1 + 8 * len(x)) ** 0.5) / 2
        if round(d) != d:
            raise ValueError("Number of elements in x will not form a square matrix")
        d = int(d)
        invvechx = np.zeros((d, d))
        idx = 0
        for j in range(d):
            length = d - j
            invvechx[j:d, j] = x[idx:idx + length]
            idx += length
        invvechx = invvechx + invvechx.T - np.diag(np.diag(invvechx))
        return invvechx

    def _amse_temp(self, vechH, K0, n, psi2_hat):
        H = self._invvech(vechH) @ self._invvech(vechH)
        amse_val = 1 / (np.linalg.det(H) ** (1 / 2) * n) * K0 + 1 / 2 * H.flatten().T @ psi2_hat
        return (np.sum((amse_val ** 2)))

    def _Gns(self, r, n, Sigma, scv=False):
        d = Sigma.shape[1]
        const = 2 - int(scv)
        G = (2 / ((n * (d + r)))) ** (2 / (d + r + 2)) * const * Sigma
        return G

    def _vec(self, x, byrow=False):
        x = np.asarray(x)
        if byrow:
            return x.T.flatten(order='C')
        else:
            return x.flatten(order='F')

    def _bias_annihliating_bandwidth_STAGE2(self, x, K0):
        self.c = self.c + 1
        n = x.shape[0]
        r = int(0)
        A1, A2, A3, psi2_hat, K02, D2K0, S12, Sinv12, x_star, psi4_ns = self._bias_annihliating_bandwidth_STAGE1(x, K0)
        Hstart = self._Gns(r=r, n=n, Sigma=np.cov(x_star.T))
        Hstart = -self._matrix_sqrt(Hstart)
        Hstart_flat = self._vech(Hstart)
        verbose = False

        def _func_amse_temp(vechH):
            H = self._invvech(vechH) @ self._invvech(vechH)
            amse_val = 1 / (np.linalg.det(H) ** (1 / 2) * n) * K02 + 1 / 2 * self._vec(H).T @ psi2_hat
            return (np.sum((amse_val ** 2)))

        if self.parameters["optim"] == 'LS': # TODO: WHAT IS THIS????
            result = scipy.optimize.least_squares(_func_amse_temp, Hstart_flat)
        else:
            result = scipy.optimize.minimize(_func_amse_temp, Hstart_flat, method='BFGS', options={'disp': verbose})
        H = self._invvech(result.x) @ self._invvech(result.x)
        H = S12 @ H @ S12
        return H

    def _get_bandwidths_advanced(self, real_T, sim_T, d, n_real, n_sim, cov_real, cov_sim, K0):
        h_real = self._bias_annihliating_bandwidth_STAGE2(real_T, K0)
        h_sim = self._bias_annihliating_bandwidth_STAGE2(sim_T, K0)
        hder_real = (((4 / ((d + 4) * n_real))) ** (2 / (d+ 6))) * cov_real
        hder_sim = (((4 / ((d + 4) * n_sim))) ** (2 / (d + 6))) * cov_sim
        return h_real, h_sim, hder_real, hder_sim

    def _get_var_hats(self, mean_real, real_T, hder_real, cov_real, mean_sim, sim_T, hder_sim, cov_sim):
        f_1 = self._KDE_derivative(x=mean_real, means=real_T, bandwidth=hder_real)
        f_2 = self._KDE_derivative(x=mean_sim, means=sim_T, bandwidth=hder_sim)
        var_hat_real = f_1 @ cov_real @ f_1
        var_hat_sim = f_2 @ cov_sim @ f_2
        return var_hat_real, var_hat_sim
    def _block_indices(self, nx, ny, block_limit=1e6): # TODO: IS THIS CORRECT???
        c = int(max(block_limit // nx, 1))
        l = np.arange(1, ny + c, c) - 1
        l[-1] = ny
        return l
    def _calc_phi_fast(self, bandwidth, x, y):
        d = x.shape[1]
        nx = x.shape[0]
        ny = y.shape[0]
        G = bandwidth
        Ginv = cho_solve((cholesky(G, lower=True), True), np.eye(G.shape[0]))
        detG = np.linalg.det(G)
        n_seq = self._block_indices(nx, ny)

        xG = np.dot(x, Ginv)
        a = np.sum(xG * x, axis=1)
        phi = 0
        for i in range(len(n_seq) - 1):
            nytemp = n_seq[i + 1] - n_seq[i]
            ytemp = y[n_seq[i]:n_seq[i + 1], ]
            aytemp = np.sum(np.dot(ytemp, Ginv) * ytemp, axis=1)
            M = np.dot(a.reshape(-1, 1), np.ones(nytemp).reshape(1, -1)) + np.dot(np.ones(nx).reshape(-1, 1),
                                                                                  aytemp.reshape(1, -1)) - 2 * np.dot(
                xG, ytemp.T)
            em2 = np.exp(-M / 2)
            phi += (2 * math.pi) ** (-d / 2) * detG ** (-1 / 2) * np.sum(em2)
        return phi / (nx * ny)


    def _get_phi(self, h_real, real, h_sim, sim):
        phi_11 = self._calc_phi_fast(h_real, real, real)
        phi_22 = self._calc_phi_fast(h_sim, sim, sim)
        phi_12 = self._calc_phi_fast(h_real, real, sim)
        phi_21 = self._calc_phi_fast(h_sim, real, sim)
        return phi_11, phi_22, phi_12, phi_21

    def _KDE_derivative(self, x, means, bandwidth):
        return (1 / len(means)) * np.sum(
                np.array([self._full_derivative(x, mu=means[i], Sigma=bandwidth, order=1) for i in range(len(means))]),
                axis=0)

    def _derivative_test(self, x, means, bandwidth):
        #This function was an attempt at a simpler improvement on get_var_hats. However, it is not used.
        def fun(xk):
            return (1 / len(means)) * np.sum(
                np.array([self._NormalDensityDerivative(xk, mu=means[i], Sigma=bandwidth, order=0) for i in range(len(means))]),
                axis=0)
        result = scipy.optimize.approx_fprime(x, fun)
        return result

    def _perform_test(self, Z_stat):
        p_val = 1 - scipy.stats.norm.cdf(Z_stat)
        return p_val

    def _print_test(self):
        self.p_val = 1 - scipy.stats.norm.cdf(self.Z_stat)
        names = ['T_stat', 'Z_stat', 'p_val', 'mu_hat', 'var',
                 'var_hat_real', 'var_hat_sim', 'n_real', 'n_sim',
                 'h_real', 'h_sim', 'phi_11',
                 'phi_12', 'phi_21', 'phi_22']
        d = [self.T_stat, self.Z_stat, self.p_val, self.mu_hat, self.denom_2, self.var_hat_real, self.var_hat_sim, self.n_real, self.n_sim, self.h_real, self.h_sim, self.phi_11, self.phi_12, self.phi_21, self.phi_22]
        data = {
            "KDE_Test_Data": d
        }
        df = pd.DataFrame(data, index=names)
        return df
