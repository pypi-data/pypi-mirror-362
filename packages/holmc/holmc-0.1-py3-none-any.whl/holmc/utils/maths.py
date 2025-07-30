import numpy as np


def sigmoid(x):
    """
    Compute the sigmoid function element-wise.

    Parameters
    ----------
    x : np.ndarray or float
        Input scalar or array.

    Returns
    -------
    np.ndarray or float
        Sigmoid of the input.
    """
    return 1 / (1 + np.exp(-x))


def gradient(theta, X, y, lamb):
    """
    Compute the gradient of the regularized logistic loss function.

    Parameters
    ----------
    theta : np.ndarray
        Parameter vector of shape (n_features,).
    X : np.ndarray
        Design matrix of shape (n_samples, n_features).
    y : np.ndarray
        Binary target vector of shape (n_samples,) with values in {0, 1}.
    lamb : float
        Regularization parameter (prior precision).

    Returns
    -------
    np.ndarray
        Gradient vector of shape (n_features,).
    """
    s = sigmoid(X @ theta)
    return X.T @ (s - y) + lamb * theta


def loss(theta, X, y, lamb):
    """
    Compute the regularized logistic loss (negative log-likelihood).

    Parameters
    ----------
    theta : np.ndarray
        Parameter vector of shape (n_features,).
    X : np.ndarray
        Design matrix of shape (n_samples, n_features).
    y : np.ndarray
        Binary target vector of shape (n_samples,) with values in {0, 1}.
    lamb : float
        Regularization parameter (prior precision).

    Returns
    -------
    float
        Regularized logistic loss value.
    """
    logits = X @ theta
    loss_val = (
        np.mean(np.log(1 + np.exp(-y * logits)))
        + (lamb / 2) * np.linalg.norm(theta) ** 2
    )
    return loss_val


def accuracy(y_true, y_pred):
    """
    Compute classification accuracy.

    Parameters
    ----------
    y_true : np.ndarray
        Ground truth binary labels of shape (n_samples,).
    y_pred : np.ndarray
        Predicted binary labels of shape (n_samples,).

    Returns
    -------
    float
        Accuracy score rounded to four decimal places.
    """
    if len(y_true) != len(y_pred):
        raise ValueError(
            "Length of true labels and predicted labels must match."
        )
    correct = 0
    for true, pred in zip(y_true, y_pred):
        if true == pred:
            correct += 1
    return round(correct / len(y_true), 4)


def thetastarreg(
    A: np.ndarray, b: np.ndarray, randomized: bool = False
) -> np.ndarray:
    """
    Compute the theta star for regression.

    Args:
        A (np.ndarray): Design matrix.
        b (np.ndarray): Response vector.

    Returns:
        np.ndarray: Computed theta star.
    """
    if randomized:
        d = A.shape[1]
        theta = np.random.randn(d)
    else:
        theta = np.linalg.solve(A, b)
    return theta
