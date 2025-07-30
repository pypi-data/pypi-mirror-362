import numpy as np
import pandas as pd
from tqdm import tqdm

from holmc.samplers.o3sampler import HoLMCSamplerO3Classification
from holmc.samplers.o3sampler import HoLMCSamplerO3Regression
from holmc.samplers.o4sampler import HoLMCSamplerO4Classification
from holmc.samplers.o4sampler import HoLMCSamplerO4Regression
from holmc.utils.maths import accuracy, sigmoid
from holmc.utils.metric import Wasserstein2Distance
from holmc.utils.params import O3Params, O4Params


class GridSearch:
    """
    Base class for performing grid search over Langevin Monte Carlo 
    hyperparameters.

    Parameters
    ----------
    gammas : list
        List of gamma (friction) values to try.
    etas : list
        List of eta (step size) values to try.
    xis : list
        List of xi values (used only for third-order methods). If None, 
        fourth-order is assumed.
    N : int
        Number of MCMC samples to draw for each parameter configuration. 
        Required.
    seed : int
        Random seed for reproducibility.
    show_progress : bool, default=True
        Whether to show a progress bar during the grid search.
    """
    def __init__(
        self,
        gammas: list = None,
        etas: list = None,
        xis: list = None,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.gammas = gammas
        self.etas = etas
        self.xis = xis
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        if seed is not None:
            np.random.seed(seed)
        if N is None:
            raise ValueError("N must be specified for grid search.")


class GridSearchRegression(GridSearch):
    """
    Grid search implementation for Bayesian linear regression using HoLMC 
    samplers.

    This class runs over a grid of (eta, gamma, xi) parameters and evaluates 
    performance
    using the Wasserstein-2 distance between the sampled distribution and the 
    target posterior.

    Methods
    -------
    run(X, y, lamb):
        Executes the grid search and returns a DataFrame of results sorted by 
        W2 distance.
    """
    def run(self, X: np.ndarray, y: np.ndarray, lamb: float = None):
        """
        Run the grid search for regression.

        Parameters
        ----------
        X : np.ndarray
            Design matrix of shape (n_samples, n_features).
        y : np.ndarray
            Response vector of shape (n_samples,) or (n_samples, 1).
        lamb : float
            Regularization (prior precision) parameter. Required.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the grid search results sorted by minimum
            Wasserstein-2 distance.
        """
        if lamb is None:
            raise ValueError("lamb must be specified for grid search.")

        if X is None or y is None:
            raise ValueError("X and y must be provided for grid search.")

        N = self.N

        results = []

        is_third_order = self.xis is not None

        for eta in tqdm(self.etas, disable=not self.show_progress, desc="Eta"):
            for gamma in self.gammas:
                xi_list = self.xis if is_third_order else [None]
                for xi in xi_list:
                    try:
                        if is_third_order:
                            params = O3Params(eta=eta, gamma=gamma, xi=xi)
                            sampler = HoLMCSamplerO3Regression(
                                params=params,
                                N=N,
                                seed=self.seed,
                                show_progress=False,
                            )
                        else:
                            params = O4Params(eta=eta, gamma=gamma)
                            sampler = HoLMCSamplerO4Regression(
                                params=params,
                                N=N,
                                seed=self.seed,
                                show_progress=False,
                            )
                        samples = sampler.sample(X, y, lamb)
                        metric = Wasserstein2Distance(X=X, y=y)
                        dist = metric.w2distance(samples)
                        min_dist = np.nanmin(dist)

                        result = {
                            "gamma": gamma,
                            "eta": eta,
                            "w2dist": min_dist,
                        }
                        if is_third_order:
                            result["xi"] = xi
                        results.append(result)
                    except Exception:
                        result = {"gamma": gamma, "eta": eta, "w2dist": np.nan}
                        if is_third_order:
                            result["xi"] = xi
                        results.append(result)

        self.results_df = pd.DataFrame(results).sort_values("w2dist")
        return self.results_df


class GridSearchClassification(GridSearch):
    """
    Grid search implementation for Bayesian logistic regression using HoLMC
    samplers.

    This class evaluates sampler performance over a grid of parameters using
    predictive accuracy
    based on samples averaged over time.

    Methods
    -------
    run(X, y, lamb):
        Executes the grid search and returns a DataFrame sorted by maximum
        accuracy.
    compute_accuracy(X, y, samples):
        Computes predictive accuracy from the sample sequence.
    """
    def compute_accuracy(self, X, y, samples):
        """
        Compute classification accuracy over cumulative average of sampled 
        parameters.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix of shape (n_samples, n_features).
        y : np.ndarray
            Binary target labels (0 or 1) of shape (n_samples,).
        samples : np.ndarray
            Array of sampled parameter vectors of shape (n_samples, n_features)

        Returns
        -------
        np.ndarray
            Array of accuracy scores as function of the sample index.
        """
        n = samples.shape[0]
        accuracies = []

        for i in range(1, n + 1):
            avg_theta = np.mean(samples[:i], axis=0)
            logits = X @ avg_theta
            probs = sigmoid(logits)
            y_pred = (probs >= 0.5).astype(int)
            acc = accuracy(y, y_pred)
            accuracies.append(acc)

        return np.array(accuracies)

    def run(self, X: np.ndarray, y: np.ndarray, lamb: float = None):
        """
        Run the grid search for classification.

        Parameters
        ----------
        X : np.ndarray
            Feature matrix of shape (n_samples, n_features).
        y : np.ndarray
            Binary target labels (0 or 1) of shape (n_samples,).
        lamb : float
            Regularization (prior precision) parameter. Required.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the grid search results sorted by maximum 
            accuracy.
        """
        if lamb is None:
            raise ValueError("lamb must be specified for grid search.")

        results = []
        N = self.N

        is_third_order = self.xis is not None

        for eta in tqdm(self.etas, disable=not self.show_progress, desc="Eta"):
            for gamma in self.gammas:
                xi_list = self.xis if is_third_order else [None]
                for xi in xi_list:
                    try:
                        if is_third_order:
                            params = O3Params(eta=eta, gamma=gamma, xi=xi)
                            sampler = HoLMCSamplerO3Classification(
                                params=params,
                                N=N,
                                seed=self.seed,
                                show_progress=False,
                            )
                        else:
                            params = O4Params(eta=eta, gamma=gamma)
                            sampler = HoLMCSamplerO4Classification(
                                params=params,
                                N=N,
                                seed=self.seed,
                                show_progress=False,
                            )
                        samples = sampler.sample(X, y, lamb)
                        ac = self.compute_accuracy(X, y, samples)
                        max_acc = np.nanmax(ac)

                        result = {
                            "gamma": gamma,
                            "eta": eta,
                            "MaxAcc": max_acc,
                        }
                        if is_third_order:
                            result["xi"] = xi
                        results.append(result)
                    except Exception:
                        result = {"gamma": gamma, "eta": eta, "MaxAcc": np.nan}
                        if is_third_order:
                            result["xi"] = xi
                        results.append(result)

        self.results_df = pd.DataFrame(results).sort_values(
            "MaxAcc", ascending=False
        )
        return self.results_df
