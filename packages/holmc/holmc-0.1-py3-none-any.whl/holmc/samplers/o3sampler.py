import numpy as np
from tqdm import tqdm
from holmc.utils.maths import sigmoid
from holmc.utils.params import O3Params


class HoLMCSamplerO3Regression:
    """
    Implements a third-order Higher-Order Langevin Monte Carlo (HoLMC) sampler 
    for Bayesian linear regression. The sampler uses an underdamped Langevin 
    dynamics approach to generate posterior samples over model parameters.

    Parameters
    ----------
    params : O3Params
        Parameter object containing integration coefficients and covariance 
        settings.
    N : int
        Number of samples to draw. Required.
    seed : int, optional
        Random seed for reproducibility.
    show_progress : bool, default=True
        Whether to display a progress bar during sampling.
    """
    def __init__(
        self,
        params: O3Params,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.p = params
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        if seed is not None:
            np.random.seed(seed)
        if N is None:
            raise ValueError("Number of samples 'N' must be provided.")

    def sample(
        self,
        X: np.ndarray,
        y: np.ndarray,
        lamb: float = None,
        theta_random: bool = True,
    ) -> np.ndarray:
        """
        Run the HoLMC sampler to draw posterior samples for Bayesian linear 
        regression.

        Parameters
        ----------
        X : np.ndarray
            Design matrix of shape (n_samples, n_features).
        y : np.ndarray
            Response vector of shape (n_samples,) or (n_samples, 1).
        lamb : float
            Regularization (prior precision) parameter. Required.
        theta_random : bool, default=True
            If True, initializes theta randomly; otherwise uses the ridge 
            solution.

        Returns
        -------
        samples : np.ndarray
            Array of shape (N+1, n_features) containing sampled parameter 
            vectors.
        """
        if lamb is None:
            raise ValueError(
                "Regularization parameter 'lamb' must be provided."
            )
        eta = self.p.eta
        n, d = X.shape
        A = ((X.T @ X) / n) + lamb * np.eye(d)
        b = ((X.T @ y) / n).squeeze()
        L = self.p.L

        # mu parameters
        mu12, mu13 = self.p.mu12(), self.p.mu13()
        mu22, mu23 = self.p.mu22(), self.p.mu23()
        mu31, mu32 = self.p.mu31(), self.p.mu32()
        mu33 = self.p.mu33()

        # Covariance matrix
        Sigma = self.p.sigma(d)

        CL = np.linalg.cholesky(Sigma)

        # Initiate the states
        if theta_random:
            theta = np.random.randn(d)
        else:
            theta = np.linalg.solve(A, b)
        v1 = np.zeros_like(theta)
        v2 = np.zeros_like(theta)

        samples = []
        samples.append(theta.copy())

        for _ in tqdm(range(self.N), disable=not self.show_progress):
            mu = np.concatenate([theta, v1, v2])
            z = np.random.randn(3 * d)
            x = mu + CL @ z
            theta, v1, v2 = np.split(x, 3)

            # Updates in the mean vectors
            delta_f = (
                A @ (eta * theta + (np.power(eta, 2) / 2.0) * v1) - eta * b
            )

            theta = theta - (eta / (2.0 * L)) * delta_f + mu12 * v1 + mu13 * v2
            v1 = -(1 / L) * delta_f + mu22 * v1 + mu23 * v2
            v2 = (mu31 / L) * delta_f + mu32 * v1 + mu33 * v2

            samples.append(theta.copy())
        return np.array(samples)


class HoLMCSamplerO3Classification:
    """
    Implements a third-order Higher-Order Langevin Monte Carlo (HoLMC) 
    sampler for Bayesian logistic regression. This sampler uses higher-order
    approximations of the potential energy gradient to improve sampling
    efficiency in classification tasks.

    Parameters
    ----------
    params : O3Params
        Parameter object containing integration coefficients and covariance
        settings.
    N : int
        Number of samples to draw. Required.
    seed : int
        Random seed for reproducibility.
    show_progress : bool, default=True
        Whether to display a progress bar during sampling.
    """
    def __init__(
        self,
        params: O3Params,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.params = params
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        if seed is not None:
            np.random.seed(seed)
        if N is None:
            raise ValueError("Number of samples 'N' must be provided.")

    def sample(
        self, X: np.ndarray, y: np.ndarray, lamb: float = None
    ) -> np.ndarray:
        if lamb is None:
            raise ValueError(
                "Regularization parameter 'lamb' must be provided."
            )
        d = X.shape[1]
        eta = self.params.eta
        L = self.params.L

        # mu parameters
        mu12, mu13 = self.params.mu12(), self.params.mu13()
        mu22, mu23 = self.params.mu22(), self.params.mu23()
        mu31, mu32 = self.params.mu31(), self.params.mu32()
        mu33 = self.params.mu33()

        # Covariance matrix
        Sigma = self.params.sigma(d)

        CL = np.linalg.cholesky(Sigma)

        # Initiate the states
        theta = np.random.randn(d)
        # theta_star = np.random.randn(d)
        # for _ in range(self.N):
        #     g = gradient(theta_star, X, y, lamb)
        #     theta_star -= eta * g
        # theta = theta_star.copy()
        v1 = np.zeros_like(theta)
        v2 = np.zeros_like(theta)

        samples = []
        samples.append(theta.copy())

        for _ in tqdm(range(self.N), disable=not self.show_progress):
            # Sample from the multivariate normal distribution
            mu = np.concatenate([theta, v1, v2])
            z = np.random.randn(3 * d)
            x = mu + CL @ z
            theta, v1, v2 = np.split(x, 3)
            # Updates in the mean vectors
            s = sigmoid(X @ theta)
            xv1 = X @ v1
            deltaU = (
                eta * (lamb * theta + X.T @ (s - y))
                + (eta**2 / 2) * (X.T @ (s * (1 - s) * xv1) + lamb * v1)
                + (eta**3 / 6) * (X.T @ (s * (1 - s) * (1 - 2 * s) * xv1**2))
                + (eta**4 / 24)
                * (X.T @ (s * (1 - s) * (1 - 6 * s + 6 * s**2) * xv1**3))
            )
            theta = theta - (eta / (2.0 * L)) * deltaU + mu12 * v1 + mu13 * v2
            v1 = -(1 / L) * deltaU + mu22 * v1 + mu23 * v2
            v2 = (mu31 / L) * deltaU + mu32 * v1 + mu33 * v2

            samples.append(theta.copy())
        return np.array(samples)
