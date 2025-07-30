"""
Classification and Regression update routines for 4th-order Langevin Monte 
Carlo samplers.

This module provides methods for updating theta and velocity variables 
v1, v2, v3 in both Bayesian logistic and linear regression settings using 
fourth-order underdamped Langevin dynamics.

Classes
-------
- Classification : Update rules for Bayesian logistic regression 
  (nonlinear likelihood).
- Regression     : Update rules for Bayesian linear regression 
  (Gaussian likelihood).
"""


import numpy as np
from holmc.utils.maths import sigmoid


class Classification:
    """
    Update equations for fourth-order Langevin dynamics in Bayesian 
    logistic regression.

    This class provides high-order update rules for the parameter vector 
    theta and auxiliary velocity variables v1, v2, and v3, using high-order 
    expansions of the sigmoid likelihood gradient.
    """
    def __init__(self):
        pass
    
    def update_theta(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        X: np.ndarray,
        y: np.ndarray,
        gamma: float, eta: float, lamb: float,
        mu01: float, mu02: float, mu03: float
    ) -> np.ndarray:
        """
          Compute the updated theta (position) vector for logistic regression.

        Returns
        -------
        theta_new : np.ndarray
            Updated theta vector.
        """
        s = sigmoid(X @ theta)

        # Scalar coefficients
        c0 = (
            (gamma**2 * eta**4 * lamb) / 24
            + (eta**4 * lamb**2) / 24
            - (eta**2 * lamb) / 2 + 1
        )
        c1 = (
            (gamma**2 * eta**5 * lamb) / 60
            + (eta**5 * lamb**2) / 120
            - (eta**3 * lamb) / 6 + mu01
        )
        c2 = mu02 - (gamma * eta**4 * lamb) / 24
        c3 = mu03 - (gamma**2 * eta**5 * lamb) / 120

        cM0 = (gamma**2 * eta**4) / 24 + (eta**4 * lamb) / 24 - (eta**2) / 2
        cM1 = (gamma**2 * eta**5) / 120 + (eta**5 * lamb) / 120 - (eta**3) / 6
        cM2 = (gamma**2 * eta**6) / 720 + (eta**6 * lamb) / 720 - (eta**4) / 24
        cM3 = (
            (gamma**2 * eta**7) / 5040 + (eta**7 * lamb) / 5040
            - (eta**5) / 120
        )

        # Compute theta update
        xv1 = X @ v1
        theta_new = (
            c0 * theta +
            c1 * v1 +
            c2 * v2 +
            c3 * v3 +
            cM0 * (X.T @ (s - y)) +
            cM1 * (X.T @ (s * (1 - s) * xv1)) +
            cM2 * (X.T @ (s * (1 - s) * (1 - 2 * s) * xv1**2)) +
            cM3 * (X.T @ (s * (1 - s) * (1 - 6 * s + 6 * s**2) * xv1**3))
        )

        return theta_new
    
    def update_v1(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        X: np.ndarray,
        y: np.ndarray,
        gamma: float, eta: float, lamb: float,
        mu11: float, mu12: float, mu13: float
    ) -> np.ndarray:
        """
         Compute the updated v1 (first velocity) vector for logistic regression

        Returns
        -------
        v1_new : np.ndarray
            Updated v1 vector.
        """
        s = sigmoid(X @ theta)
        
        # Scalar coefficients
        c0 = (
            (gamma**2 * eta**3 * lamb) / 6
            + (eta**3 * lamb**2) / 6 - eta * lamb
        )
        c1 = (
            (gamma**2 * eta**4 * lamb) / 12
            + (eta**4 * lamb**2) / 24 - (eta**2 * lamb) / 2 + mu11
        )
        c2 = mu12 - (gamma * eta**3 * lamb) / 6
        c3 = mu13 - (gamma**2 * eta**4 * lamb) / 24

        cM0 = (gamma**2 * eta**3) / 6 + (eta**3 * lamb) / 6 - eta
        cM1 = (gamma**2 * eta**4) / 24 + (eta**4 * lamb) / 24 - (eta**2) / 2
        cM2 = (gamma**2 * eta**5) / 120 + (eta**5 * lamb) / 120 - (eta**3) / 6
        cM3 = (gamma**2 * eta**6) / 720 + (eta**6 * lamb) / 720 - (eta**4) / 24

        # Compute v1 update
        xv1 = X @ v1
        v1_new = (
            c0 * theta +
            c1 * v1 +
            c2 * v2 +
            c3 * v3 +
            cM0 * (X.T @ (s - y)) +
            cM1 * (X.T @ (s * (1 - s) * xv1)) +
            cM2 * (X.T @ (s * (1 - s) * (1 - 2 * s) * xv1**2)) +
            cM3 * (X.T @ (s * (1 - s) * (1 - 6 * s + 6 * s**2) * xv1**3))
        )

        return v1_new
    
    def update_v2(
        self,
        theta: np.ndarray, 
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray, 
        X: np.ndarray,
        y: np.ndarray, 
        gamma: float, eta: float, lamb: float, 
        mu21: float, mu22: float, mu23: float
    ) -> np.ndarray:
        """
        Compute the updated v2 (second velocity) vector for logistic regression

        Returns
        -------
        v2_new : np.ndarray
            Updated v2 vector.
        """
        s = sigmoid(X @ theta)

        exp_term = np.exp(-gamma * eta)

        # θ coefficient
        c_theta = (
            - (gamma * eta**2 * lamb / 24)
            * (gamma**2 * eta**2 + eta**2 * lamb - 12)
            + (lamb / (6 * gamma))
            * (
                -gamma**3 * eta**3 + 3 * gamma**2 * eta**2
                - 6 * gamma * eta - 6 * exp_term + 6
            )
        )

        # v1 coefficient
        c_v1 = (
            mu21
            - (
                gamma * eta**3 * lamb
                * (2 * gamma**2 * eta**2 + eta**2 * lamb - 20)
            ) / 120
            + (lamb / (24 * gamma**2)) * (
                -gamma**4 * eta**4 + 4 * gamma**3 * eta**3
                - 12 * gamma**2 * eta**2 + 24 * gamma * eta
                + 24 * exp_term - 24
            )
        )

        # v2 and v3 coefficients
        c_v2 = mu22 + (gamma**2 * eta**4 * lamb) / 24
        c_v3 = mu23 + (gamma**3 * eta**5 * lamb) / 120

        # M0 coefficient
        c_M0 = (
            - (gamma * eta**2 / 24)
            * (gamma**2 * eta**2 + eta**2 * lamb - 12)
            - (1 / (6 * gamma))
            * (
                gamma**3 * eta**3 - 3 * gamma**2 * eta**2
                + 6 * gamma * eta + 6 * exp_term - 6
            )
        )

        # M1 coefficient
        c_M1 = (
            (1 / (24 * gamma**2))
            * (
                gamma**4 * eta**4 - 4 * gamma**3 * eta**3
                + 12 * gamma**2 * eta**2 - 24 * gamma * eta
                - 24 * exp_term + 24
            )
            - (gamma * eta**3 / 120) * (gamma**2 * eta**2 + eta**2 * lamb - 20)
        )

        # M2 coefficient
        c_M2 = (
            - (gamma * eta**4 * (gamma**2 * eta**2 + eta**2 * lamb - 30)) / 720
            + (1 - exp_term) / gamma**3
            - (1 / 120) * gamma**2 * eta**5
            - eta / gamma**2
            + (gamma * eta**4) / 24
            + (eta**2) / (2 * gamma)
            - (eta**3) / 6
        )

        # M3 coefficient
        c_M3 = (
            - (
                gamma * eta**5 * (gamma**2 * eta**2 + eta**2 * lamb - 42)
            ) / 5040
            - (1 / (720 * gamma**4)) * (
                gamma**6 * eta**6 - 6 * gamma**5 * eta**5
                + 30 * gamma**4 * eta**4
                - 120 * gamma**3 * eta**3 + 360 * gamma**2 * eta**2
                - 720 * gamma * eta - 720 * exp_term + 720
            )
        )

        # Final v2 update
        xv1 = X @ v1
        v2_new = (
            c_theta * theta +
            c_v1 * v1 +
            c_v2 * v2 +
            c_v3 * v3 +
            c_M0 * (X.T @ (s - y)) +
            c_M1 * (X.T @ (s * (1 - s) * xv1)) +
            c_M2 * (X.T @ (s * (1 - s) * (1 - 2 * s) * xv1**2)) +
            c_M3 * (X.T @ (s * (1 - s) * (1 - 6 * s + 6 * s**2) * xv1**3))
        )

        return v2_new
    
    def update_v3(
        self,
        theta: np.ndarray, 
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray, 
        X: np.ndarray,
        y: np.ndarray, 
        gamma: float, eta: float, lamb: float, 
        mu31: float, mu32: float, mu33: float
    ) -> np.ndarray:
        """
        Compute the updated v3 (third velocity) vector for logistic regression

        Returns
        -------
        v3_new : np.ndarray
            Updated v3 vector.
        """
        exp_ge = np.exp(gamma * eta)
        exp_neg_ge = np.exp(-gamma * eta)
        s = sigmoid(X @ theta)
        
        # Coefficient for theta
        c_theta = (lamb * exp_neg_ge / (24 * gamma**3)) * (
            gamma**6 * eta**4 * exp_ge
            + gamma**4 * eta**2 * exp_ge * (eta**2 * lamb - 24)
            - 4 * gamma**3 * eta * (exp_ge * (eta**2 * lamb - 18) - 6)
            + 12 * gamma**2 * (exp_ge * (eta**2 * lamb - 8) + 8)
            - 24 * gamma * eta * lamb * exp_ge
            + 24 * lamb * (exp_ge - 1)
        )

        # Coefficient for v1
        c_v1 = mu31 + (lamb * exp_neg_ge / (120 * gamma**4)) * (
            2 * gamma**7 * eta**5 * exp_ge
            - 5 * gamma**6 * eta**4 * exp_ge
            + gamma**5 * eta**3 * exp_ge * (eta**2 * lamb - 20)
            - 5 * gamma**4 * eta**2 * exp_ge * (eta**2 * lamb - 24)
            + 20 * gamma**3 * eta * (exp_ge * (eta**2 * lamb - 18) - 6)
            - 60 * gamma**2 * (exp_ge * (eta**2 * lamb - 8) + 8)
            + 120 * gamma * eta * lamb * exp_ge
            - 120 * lamb * (exp_ge - 1)
        )

        # Coefficient for v2
        c_v2 = mu32 + (lamb / (24 * gamma**2)) * (
            -gamma**4 * eta**4 + 4 * gamma**3 * eta**3 - 12 * gamma**2 * eta**2
            + 24 * gamma * eta + 24 * exp_neg_ge - 24
        )

        # Coefficient for v3
        c_v3 = mu33 + (lamb / (120 * gamma**2)) * (
            -gamma**5 * eta**5 + 5 * gamma**4 * eta**4 - 20 * gamma**3 * eta**3
            + 60 * gamma**2 * eta**2 - 120 * gamma * eta
            - 120 * exp_neg_ge + 120
        )

        # M0 coefficient
        c_M0 = (
            (gamma**3 * eta**4) / 24
            + (lamb - lamb * exp_neg_ge) / gamma**3
            - (eta * lamb) / gamma**2
            + (4 * exp_neg_ge + (eta**2 * lamb) / 2 - 4) / gamma
            + gamma * (eta**4 * lamb / 24 - eta**2)
            + eta * (exp_neg_ge + 3)
            - (eta**3 * lamb) / 6
        )

        # M1 coefficient
        c_M1 = (
            (lamb * (exp_neg_ge - 1)) / gamma**4
            + (gamma**3 * eta**5) / 120
            + (eta * lamb) / gamma**3
            + (-5 * exp_neg_ge - (eta**2 * lamb) / 2 + 5) / gamma**2
            + (eta * (-exp_neg_ge - 4) + (eta**3 * lamb) / 6) / gamma
            + (1 / 120) * gamma * eta**3 * (eta**2 * lamb - 40)
            - (1 / 24) * eta**2 * (eta**2 * lamb - 36)
        )

        # M2 coefficient
        c_M2 = (
            (lamb - lamb * exp_neg_ge) / gamma**5
            - (eta * lamb) / gamma**4
            + (gamma**3 * eta**6) / 720
            + (6 * exp_neg_ge + (eta**2 * lamb) / 2 - 6) / gamma**3
            + (eta * (exp_neg_ge + 5) - (eta**3 * lamb) / 6) / gamma**2
            + (1 / 720) * gamma * eta**4 * (eta**2 * lamb - 60)
            + ((eta**4 * lamb) / 24 - 2 * eta**2) / gamma
            - (1 / 120) * eta**3 * (eta**2 * lamb - 60)
        )

        # M3 coefficient
        c_M3 = (
            (lamb * (exp_neg_ge - 1)) / gamma**6
            + (eta * lamb) / gamma**5
            + (-7 * exp_neg_ge - (eta**2 * lamb) / 2 + 7) / gamma**4
            + (gamma**3 * eta**7) / 5040
            + (eta * (-exp_neg_ge - 6) + (eta**3 * lamb) / 6) / gamma**3
            + (60 * eta**2 - eta**4 * lamb) / (24 * gamma**2)
            + (gamma * eta**5 * (eta**2 * lamb - 84)) / 5040
            + (eta**3 * (eta**2 * lamb - 80)) / (120 * gamma)
            - (1 / 720) * eta**4 * (eta**2 * lamb - 90)
        )

        # Final v3 update
        xv1 = X @ v1
        v3_new = (
            c_theta * theta +
            c_v1 * v1 +
            c_v2 * v2 +
            c_v3 * v3 +
            c_M0 * (X.T @ (s - y)) +
            c_M1 * (X.T @ (s * (1 - s) * xv1)) +
            c_M2 * (X.T @ (s * (1 - s) * (1 - 2 * s) * xv1**2)) +
            c_M3 * (X.T @ (s * (1 - s) * (1 - 6 * s + 6 * s**2) * xv1**3))
        )

        return v3_new


class Regression:
    """
     Update equations for fourth-order Langevin dynamics in Bayesian linear 
     regression.

    This class implements analytical updates of the position and velocity 
    vectors using high-order Taylor approximations of the quadratic potential
    induced by the Gaussian likelihood.
    """
    def __init__(self):
        pass
    
    def update_theta(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        A: np.ndarray,
        b: np.ndarray,
        gamma: float, eta: float,
        mu01: float, mu02: float, mu03: float
    ):
        """
        Compute the updated theta (position) vector for linear regression.

        Returns
        -------
        theta : np.ndarray
            Updated theta vector.
        """
        a_theta_b = A @ theta - b
        aa_theta_b = A @ (A @ theta - b)
        a_v1 = A @ v1
        aa_v1 = A @ (A @ v1)
        a_v2 = A @ v2
        a_v3 = A @ v3
        theta = (
                theta
                + mu01 * v1
                + mu02 * v2
                + mu03 * v3
                + (
                    (np.power(eta, 4) * np.power(gamma, 2)) / 24
                    - np.power(eta, 2) / 2
                )
                * a_theta_b
                + (np.power(eta, 4) / 24) * aa_theta_b
                + (
                    (np.power(eta, 5) * np.power(gamma, 2)) / 60
                    - np.power(eta, 3) / 6
                )
                * a_v1
                + (np.power(eta, 5) / 120) * aa_v1
                - ((np.power(eta, 4) * gamma) / 24) * a_v2
                - ((np.power(eta, 5) * np.power(gamma, 2)) / 120) * a_v3
            )
        return theta
    
    def update_v1(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        A: np.ndarray,
        b: np.ndarray,
        gamma: float, eta: float,
        mu11: float, mu12: float, mu13: float
    ):
        """
        Compute the updated v1 (first velocity) vector for linear regression.

        Returns
        -------
        v1 : np.ndarray
            Updated v1 vector.
        """
        a_theta_b = A @ theta - b
        aa_theta_b = A @ (A @ theta - b)
        a_v1 = A @ v1
        aa_v1 = A @ (A @ v1)
        a_v2 = A @ v2
        a_v3 = A @ v3
        v1 = (
                mu11 * v1
                + mu12 * v2
                + mu13 * v3
                + (((np.power(eta, 3) * np.power(gamma, 2)) / 6) - eta)
                * a_theta_b
                + (np.power(eta, 3) / 6) * aa_theta_b
                + (
                    (np.power(eta, 4) * np.power(gamma, 2)) / 12
                    - np.power(eta, 2) / 2
                )
                * a_v1
                + (np.power(eta, 4) / 24) * aa_v1
                - ((np.power(eta, 3) * gamma) / 6) * a_v2
                - ((np.power(eta, 4) * np.power(gamma, 2)) / 24) * a_v3
            )
        return v1
    
    def update_v2(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        A: np.ndarray,
        b: np.ndarray,
        gamma: float, eta: float,
        mu21: float, mu22: float, mu23: float
    ):
        """
        Compute the updated v2 (second velocity) vector for linear regression.

        Returns
        -------
        v2 : np.ndarray
            Updated v2 vector.
        """
        a_theta_b = A @ theta - b
        aa_theta_b = A @ (A @ theta - b)
        a_v1 = A @ v1
        aa_v1 = A @ (A @ v1)
        a_v2 = A @ v2
        a_v3 = A @ v3
        v2 = (
                mu21 * v1
                + mu22 * v2
                + mu23 * v3
                + (
                    (1 - np.exp(-eta * gamma)) / gamma
                    - np.power(eta, 4) * np.power(gamma, 3) / 24
                    - np.power(eta, 3) * np.power(gamma, 2) / 6
                    + np.power(eta, 2) * gamma
                    - eta
                )
                * a_theta_b
                - (np.power(eta, 4) * gamma / 24) * aa_theta_b
                + (
                    -np.power(eta, 5) * np.power(gamma, 3) / 60
                    - np.power(eta, 4) * np.power(gamma, 2) / 24
                    + np.power(eta, 3) * gamma / 3
                    - np.power(eta, 2) / 2
                    + eta / gamma
                    - (1 - np.exp(-eta * gamma)) / np.power(gamma, 2)
                )
                * a_v1
                - (np.power(eta, 5) * gamma / 120) * aa_v1
                + (np.power(eta, 4) * np.power(gamma, 3) / 24) * a_v2
                + (np.power(eta, 5) * np.power(gamma, 3) / 120) * a_v3
            )
        return v2
    
    def update_v3(
        self,
        theta: np.ndarray,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
        A: np.ndarray,
        b: np.ndarray,
        gamma: float, eta: float,
        mu31: float, mu32: float, mu33: float
    ):
        """
        Compute the updated v3 (third velocity) vector for linear regression.

        Returns
        -------
        v3 : np.ndarray
            Updated v3 vector.
        """
        a_theta_b = A @ theta - b
        aa_theta_b = A @ (A @ theta - b)
        a_v1 = A @ v1
        aa_v1 = A @ (A @ v1)
        a_v2 = A @ v2
        a_v3 = A @ v3
        v3 = (
                mu31 * v1
                + mu32 * v2
                + mu33 * v3
                + (
                    np.power(eta, 4) * np.power(gamma, 3) / 24
                    - np.power(eta, 2) * gamma
                    + eta * (3 + np.exp(-eta * gamma))
                    - (4 * (1 - np.exp(-eta * gamma))) / gamma
                )
                * a_theta_b
                + (
                    np.power(eta, 4) * gamma / 24
                    - np.power(eta, 3) / 6
                    + np.power(eta, 2) / (2 * gamma)
                    - eta / np.power(gamma, 2)
                    + (1 - np.exp(-eta * gamma)) / np.power(gamma, 3)
                )
                * aa_theta_b
                + (
                    np.power(eta, 5) * np.power(gamma, 3) / 60
                    - np.power(eta, 4) * np.power(gamma, 2) / 24
                    - np.power(eta, 3) * gamma / 6
                    + np.power(eta, 2)
                    - 4 * np.exp(-eta * gamma) / np.power(gamma, 2)
                    - eta * np.exp(-eta * gamma) / gamma
                    - 3 * eta / gamma
                    + 4 / np.power(gamma, 2)
                )
                * a_v1
                + (
                    np.power(eta, 5) * gamma / 120
                    - np.power(eta, 4) / 24
                    + np.power(eta, 3) / (6 * gamma)
                    - np.power(eta, 2) / (2 * np.power(gamma, 2))
                    + np.exp(-eta * gamma) / np.power(gamma, 4)
                    + eta / np.power(gamma, 3)
                    - 1 / np.power(gamma, 4)
                )
                * aa_v1
                + (
                    -np.power(eta, 4) * np.power(gamma, 2) / 24
                    + np.power(eta, 3) * gamma / 6
                    - np.power(eta, 2) / 2
                    + np.exp(-eta * gamma) / np.power(gamma, 2)
                    + eta / gamma
                    - 1 / np.power(gamma, 2)
                )
                * a_v2
                + (
                    -np.power(eta, 5) * np.power(gamma, 3) / 120
                    + np.power(eta, 4) * np.power(gamma, 2) / 24
                    - np.power(eta, 3) * gamma / 6
                    + np.power(eta, 2) / 2
                    - np.exp(-eta * gamma) / np.power(gamma, 2)
                    - eta / gamma
                    + 1 / np.power(gamma, 2)
                )
                * a_v3
            )
        return v3