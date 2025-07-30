import numpy as np
from scipy.linalg import sqrtm
from holmc.utils.maths import accuracy, sigmoid


class Wasserstein2Distance:
    def __init__(
        self,
        lamb2: float = 10.0,
        X: np.ndarray = None,
        y: np.ndarray = None,
        sample_std: float = 1.0,
    ):
        """
        Initialize the Wasserstein-2 distance sampler.
        Parameters:
        - lamb2: Lambda value to compute the prior. The default
          value is 10.0.
        - X: Input data matrix (numpy array).
          It should be of shape (n_samples, n_features).
        - y: Output data vector (numpy array).
          It should be of shape (n_samples,).
        - sample_std: Sample Standard Deviation (float).
          The default value is 1.0.

        Raises:
        - ValueError: If X or y is None.

        Returns:
        - Priors: A tuple containing the prior mean and covariance.
        - Posteriors: A tuple containing the posterior mean and covariance.
        - w2distance: A method to compute the Wasserstein-2 distance
          between two distributions.
        """
        self.lamb2 = lamb2
        self.sample_std = sample_std
        self.X = X
        self.y = y
        if X is None or y is None:
            raise ValueError(
                "X and y must be provided for \
                    Wasserstein-2 distance computation."
            )

    def priors(self):
        """
        Compute the prior mean and covariance.
        """
        dim = self.X.shape[1]
        prior_mean = np.zeros(dim)
        prior_cov = self.lamb2 * np.eye(dim)
        return prior_mean, prior_cov

    def posteriors(self):
        """
        Compute the posterior mean and covariance.
        """
        lam = self.lamb2
        X = self.X
        y = self.y
        dim = X.shape[1]
        sample_std = self.sample_std
        prior_cov = lam * np.eye(dim)
        XtX = X.T @ X
        Xty = X.T @ y
        posterior_cov = np.linalg.inv(
            np.linalg.inv(prior_cov) + (1.0 / sample_std**2) * XtX
        )
        posterior_mean = np.dot(
            posterior_cov, (1.0 / sample_std**2) * Xty
        ).flatten()

        return posterior_mean, posterior_cov

    def w2distance(self, distn, log_scale: bool = True):
        """
        Compute the Wasserstein-2 distance between two
        distributions.
        """
        N, d = distn.shape
        post_mean, post_cov = self.posteriors()

        w2dist = []
        for i in range(2, N):
            sample = distn[: i + 1]
            sample_mean = np.mean(sample, axis=0)
            sample_cov = np.cov(sample.T)
            diff = post_mean - sample_mean
            diff_norm_sq = np.dot(diff, diff)

            try:
                M = sample_cov @ post_cov @ sample_cov
                det = np.linalg.det(M)
                if det == 0 or np.isnan(det) or np.isinf(det):
                    M += 1e-6 * np.eye(d)
                cov_sqrt = sqrtm(M)

                w2 = diff_norm_sq + np.trace(
                    post_cov + sample_cov - 2 * cov_sqrt
                )
                w2dist.append(np.sqrt(abs(w2)))
            except Exception:
                w2dist.append(np.nan)

        if log_scale:
            return np.array(np.log(w2dist))

        return np.array(w2dist)


class AccuracyMeasure:
    def __init__(
        self,
        X: np.ndarray = None,
        y: np.ndarray = None,
    ):
        """
        Initialize the accuracy measure.
        Parameters:
        - X: Input data matrix (numpy array).
          It should be of shape (n_samples, n_features).
        - y: Output data vector (numpy array).
          It should be of shape (n_samples,).
        - sample: Sample data matrix (numpy array).
          It should be of shape (n_samples, n_features).

        Raises:
        - ValueError: If X or y is None.
        """
        self.X = X
        self.y = y
        if X is None or y is None:
            raise ValueError(
                "X and y must be provided for accuracy computation."
            )

    def compute_accuracy(self, sample: np.ndarray):
        """
        Compute the accuracy of the model.
        Returns:
        - accuracies: A numpy array containing the accuracy values.
        """
        n = sample.shape[0]

        accuracies = []

        for i in range(1, n + 1):
            avg_theta = np.mean(sample[:i], axis=0)
            logits = self.X @ avg_theta
            probs = sigmoid(logits)
            y_pred = (probs >= 0.5).astype(int)
            acc = accuracy(self.y, y_pred)
            accuracies.append(acc)

        return np.array(accuracies)
