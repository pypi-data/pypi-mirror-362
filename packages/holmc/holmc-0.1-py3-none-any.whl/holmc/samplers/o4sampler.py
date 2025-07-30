import numpy as np
from tqdm import tqdm
from holmc.utils.mean import Classification, Regression
from holmc.utils.params import O4Params

# from holmc.utils.maths import gradient


class HoLMCSamplerO4Regression:
    """
    Implements a fourth-order Higher-Order Langevin Monte Carlo (HoLMC)
    sampler for Bayesian linear regression. This sampler uses a 4-stage
    underdamped Langevin dynamics scheme to generate high-quality posterior
    samples from the Bayesian model.

    Parameters
    ----------
    params : O4Params
        Parameter object containing algorithmic coefficients, step size (eta),
        and damping (gamma).
    N : int
        Number of MCMC samples to draw. Must be specified.
    seed : int
        Random seed for reproducibility.
    show_progress : bool, default=True
        Whether to display a progress bar during sampling.
    """
    def __init__(
        self,
        params: O4Params,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.params = params
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        self.rg = Regression()
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
        Run the fourth-order HoLMC sampler to draw posterior samples for 
        Bayesian linear regression.

        Parameters
        ----------
        X : np.ndarray
            Design matrix of shape (n_samples, n_features).
        y : np.ndarray
            Response vector of shape (n_samples,) or (n_samples, 1).
        lamb : float
            Ridge regularization parameter (controls the prior precision). Must 
            be specified.
        theta_random : bool, default=True
            Whether to initialize theta randomly or from the ridge solution.

        Returns
        -------
        samples : np.ndarray
            Array of shape (N+1, n_features) containing the sequence of sampled 
            parameter vectors.
        """
        if lamb is None:
            raise ValueError(
                "Regularization parameter 'lamb' must be provided."
            )
        gamma = self.params.gamma
        eta = self.params.eta
        n, d = X.shape
        A = ((X.T @ X) / n) + lamb * np.eye(d)
        b = ((X.T @ y) / n).squeeze()

        # mu parameters
        mu01, mu02 = self.params.mu01(), self.params.mu02()
        mu03, mu11 = self.params.mu03(), self.params.mu11()
        mu12, mu13 = self.params.mu12(), self.params.mu13()
        mu21, mu22 = self.params.mu21(), self.params.mu22()
        mu23, mu31 = self.params.mu23(), self.params.mu31()
        mu32, mu33 = self.params.mu32(), self.params.mu33()

        # Covariance matrix
        Sigma = self.params.sigma(d)
        CL = np.linalg.cholesky(Sigma)

        # Initiate the states
        if theta_random:
            theta = np.random.randn(d)
        else:
            theta = np.linalg.solve(A, b)
        v1 = np.zeros_like(theta)
        v2 = np.zeros_like(theta)
        v3 = np.zeros_like(theta)

        samples = []
        samples.append(theta.copy())

        for _ in tqdm(range(self.N), disable=not self.show_progress):
            mu = np.concatenate([theta, v1, v2, v3])
            z = np.random.randn(4 * d)
            x = mu + CL @ z
            theta, v1, v2, v3 = np.split(x, 4)

            # Update in the mean vectors
            theta = self.rg.update_theta(
                theta, v1, v2, v3, A, b, gamma, eta, mu01, mu02, mu03
            )
            v1 = self.rg.update_v1(
                theta, v1, v2, v3, A, b, gamma, eta, mu11, mu12, mu13
            )
            v2 = self.rg.update_v2(
                theta, v1, v2, v3, A, b, gamma, eta, mu21, mu22, mu23
            )
            v3 = self.rg.update_v3(
                theta, v1, v2, v3, A, b, gamma, eta, mu31, mu32, mu33
            )

            samples.append(theta.copy())
        return np.array(samples)


class HoLMCSamplerO4Classification:
    """
    Implements a fourth-order Higher-Order Langevin Monte Carlo (HoLMC) sampler
    for Bayesian logistic regression. This sampler uses a high-order 
    underdamped Langevin dynamic with correction terms up to the third 
    derivative of the sigmoid to approximate the gradient of the posterior.

    Parameters
    ----------
    params : O4Params
        Parameter object containing algorithmic coefficients, step size (eta), 
        and damping (gamma).
    N : int
        Number of MCMC samples to draw. Must be specified.
    seed : int
        Random seed for reproducibility.
    show_progress : bool, default=True
        Whether to display a progress bar during sampling.
    """
    def __init__(
        self,
        params: O4Params,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.params = params
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        self.cl = Classification()
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
        gamma = self.params.gamma

        # mu parameters
        mu01, mu02 = self.params.mu01(), self.params.mu02()
        mu03, mu11 = self.params.mu03(), self.params.mu11()
        mu12, mu13 = self.params.mu12(), self.params.mu13()
        mu21, mu22 = self.params.mu21(), self.params.mu22()
        mu23, mu31 = self.params.mu23(), self.params.mu31()
        mu32, mu33 = self.params.mu32(), self.params.mu33()

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
        v3 = np.zeros_like(theta)

        samples = []
        samples.append(theta.copy())

        for _ in tqdm(range(self.N), disable=not self.show_progress):
            mu = np.concatenate([theta, v1, v2, v3])
            z = np.random.randn(4 * d)
            x = mu + CL @ z
            theta, v1, v2, v3 = np.split(x, 4)
            # Updates in the mean vectors
            theta = self.cl.update_theta(
                theta, v1, v2, v3, X, y, gamma, eta, lamb, mu01, mu02, mu03
            )
            v1 = self.cl.update_v1(
                theta, v1, v2, v3, X, y, gamma, eta, lamb, mu11, mu12, mu13
            )
            v2 = self.cl.update_v2(
                theta, v1, v2, v3, X, y, gamma, eta, lamb, mu21, mu22, mu23
            )
            v3 = self.cl.update_v3(
                theta, v1, v2, v3, X, y, gamma, eta, lamb, mu31, mu32, mu33
            )

            samples.append(theta.copy())
        return np.array(samples)
