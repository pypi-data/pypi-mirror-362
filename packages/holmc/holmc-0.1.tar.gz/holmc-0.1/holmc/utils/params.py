import numpy as np


class O3Params:
    def __init__(
        self,
        gamma: float = None,
        eta: float = None,
        xi: float = None,
        L: float = 1.0
    ):
        self.gamma = gamma
        self.eta = eta
        self.xi = xi
        self.L = L

    def mu12(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (
            (1 + gamma**2 / xi**2) * eta
            - (gamma**2 / (2 * xi)) * eta**2
            - (gamma**2 / xi**3) * (1 - np.exp(-xi * eta))
        )
        return val

    def mu13(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (gamma / xi) * eta + (gamma / xi**2) * (np.exp(-xi * eta) - 1)
        return val

    def mu22(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = 1 + (gamma**2 / xi**2) * (1 - xi * eta - np.exp(-xi * eta))
        return val

    def mu23(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (gamma / xi) * (1 - np.exp(-xi * eta))
        return val

    def mu31(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (gamma / xi) - (gamma / xi**2) * ((1 - np.exp(-xi * eta)) / eta)
        return val

    def mu32(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (
            (gamma**3 / xi**2) * eta
            + (gamma**3 / xi**2) * eta * np.exp(-xi * eta)
            - (2 * gamma**3 / xi**3 + gamma / xi) * (1 - np.exp(-xi * eta))
        )
        return val

    def mu33(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        val = (
            np.exp(-xi * eta)
            + (gamma**2 / xi) * eta * np.exp(-xi * eta)
            - (gamma**2 / xi**2) * (1 - np.exp(-xi * eta))
        )
        return val

    # Sigma entries
    def sigma11(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        exp1 = np.exp(-eta * xi)
        exp2 = np.exp(-2 * eta * xi)
        val = (
            (2 * np.power(gamma, 2) * eta) / np.power(xi, 3)
            - (2 * np.power(gamma, 2) * np.power(eta, 2)) / np.power(xi, 2)
            + (2 * np.power(gamma, 2) * np.power(eta, 3)) / (3 * xi)
            - (4 * np.power(gamma, 2) * eta * exp1) / np.power(xi, 3)
            + (np.power(gamma, 2) * (1 - exp2)) / np.power(xi, 4)
        )
        return val

    def sigma12(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        L = self.L
        exp1 = np.exp(-eta * xi)
        val = (np.power(gamma, 2) * np.power((xi * eta - (1 - exp1)), 2)) / (
            np.power(xi, 3) * L
        )
        return val

    def sigma22(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        exp1 = np.exp(-eta * xi)
        exp2 = np.exp(-2 * eta * xi)
        val = (
            (2 * np.power(gamma, 2) * eta) / xi
            - (4 * np.power(gamma, 2) * (1 - exp1)) / np.power(xi, 2)
            + (np.power(gamma, 2) * (1 - exp2)) / np.power(xi, 2)
        )
        return val

    def sigma13(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        exp1 = np.exp(-eta * xi)
        exp2 = np.exp(-2 * eta * xi)
        val = (
            -(np.power(gamma, 3) * np.power(eta, 2) * (2 * exp1 + 1))
            / np.power(xi, 2)
            + eta
            * (
                (2 * np.power(gamma, 3)) / np.power(xi, 3)
                - (np.power(gamma, 3) * exp2) / np.power(xi, 3)
                - (4 * np.power(gamma, 3) * exp1) / np.power(xi, 3)
                - (2 * gamma * exp1) / xi
            )
            + (
                ((3 * np.power(gamma, 3)) / (2 * np.power(xi, 4)))
                + gamma / np.power(xi, 2)
            )
            * (1 - exp2)
        )
        return val

    def sigma23(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        exp1 = np.exp(-eta * xi)
        exp2 = np.exp(-2 * eta * xi)
        val = (
            (np.power(gamma, 3) * (exp2 - 2 * exp1 - 2) * eta)
            / np.power(xi, 2)
            + (3 * np.power(gamma, 3) * (exp2 - 4 * exp1 + 3))
            / (2 * np.power(xi, 3))
            + (gamma * np.power((1 - exp1), 2)) / xi
        )
        return val

    def sigma33(self):
        gamma = self.gamma
        eta = self.eta
        xi = self.xi
        exp1 = np.exp(-eta * xi)
        exp2 = np.exp(-2 * eta * xi)
        val = (
            -(np.power(gamma, 4) * np.power(eta, 2) * exp2) / np.power(xi, 2)
            + eta
            * (
                -(2 * np.power(gamma, 2) * exp2) / xi
                + (np.power(gamma, 4) * (-3 * exp2 + 4 * exp1 + 2))
                / np.power(xi, 3)
            )
            + (np.power(gamma, 4) * (-5 * exp2 + 16 * exp1 - 11))
            / (2 * np.power(xi, 4))
            + (
                (np.power(gamma, 2) * (-3 * exp2 + 4 * exp1 - 1))
                / np.power(xi, 2)
            )
            + (1 - exp2)
        )
        return val

    def sigma(self, d):
        s11 = self.sigma11()
        s12 = self.sigma12()
        s13 = self.sigma13()
        s22 = self.sigma22()
        s23 = self.sigma23()
        s33 = self.sigma33()
        I_d = np.eye(d)

        # Now construct the full (3*dim x 3*dim) matrix
        top = np.hstack([s11 * I_d, s12 * I_d, s13 * I_d])
        mid = np.hstack([s12 * I_d, s22 * I_d, s23 * I_d])
        bot = np.hstack([s13 * I_d, s23 * I_d, s33 * I_d])

        mat = np.vstack([top, mid, bot])
        epsilon = 0.00001
        matrix = mat + epsilon * np.eye(3 * d)

        return matrix


class O4Params:
    def __init__(
        self,
        gamma: float = None,
        eta: float = None
    ):
        self.gamma = gamma
        self.eta = eta

    def mu01(self):
        gamma = self.gamma
        eta = self.eta
        term1 = eta
        term2 = -(gamma**2) * (eta**3) / 6
        term3 = (gamma**4) * (eta**5) / 120

        exp_term = -np.exp(-gamma * eta) / (gamma**5)
        constant_terms = (
            +1 / gamma**5
            - eta / gamma**4
            + eta**2 / (2 * gamma**3)
            - eta**3 / (6 * gamma**2)
            + eta**4 / (24 * gamma)
        )

        term4 = gamma**4 * (exp_term + constant_terms)
        val = term1 + term2 + term3 + term4
        return val

    def mu02(self):
        gamma = self.gamma
        eta = self.eta
        term1 = gamma * (eta**2) / 2
        term2 = -(gamma**3) * (eta**4) / 24

        bracket = (
            np.exp(-gamma * eta) / (gamma**4)
            - 1 / (gamma**4)
            + eta / (gamma**3)
            - eta**2 / (2 * gamma**2)
            + eta**3 / (6 * gamma)
        )

        term3 = -(gamma**3) * bracket
        val = term1 + term2 + term3

        return val

    def mu03(self):
        gamma = self.gamma
        eta = self.eta
        term1 = -(gamma**4) * (eta**5) / 120

        bracket1 = (
            -np.exp(-gamma * eta) / (gamma**3)
            + 1 / (gamma**3)
            - eta / (gamma**2)
            + eta**2 / (2 * gamma)
        )

        bracket2 = (
            -np.exp(-gamma * eta) / (gamma**5)
            + 1 / (gamma**5)
            - eta / (gamma**4)
            + eta**2 / (2 * gamma**3)
            - eta**3 / (6 * gamma**2)
            + eta**4 / (24 * gamma)
        )

        term2 = gamma**2 * bracket1
        term3 = -(gamma**4) * bracket2

        val = term1 + term2 + term3

        return val

    def mu11(self):
        gamma = self.gamma
        eta = self.eta
        term1 = 1
        term2 = -(gamma**2) * (eta**2) / 2
        term3 = (gamma**4) * (eta**4) / 24

        bracket = (
            np.exp(-gamma * eta) / (gamma**4)
            - 1 / (gamma**4)
            + eta / (gamma**3)
            - eta**2 / (2 * gamma**2)
            + eta**3 / (6 * gamma)
        )

        term4 = gamma**4 * bracket

        val = term1 + term2 + term3 + term4

        return val

    def mu12(self):
        gamma = self.gamma
        eta = self.eta
        term1 = gamma * eta
        term2 = -(gamma**3) * (eta**3) / 6

        bracket = (
            -np.exp(-gamma * eta) / (gamma**3)
            + 1 / (gamma**3)
            - eta / (gamma**2)
            + eta**2 / (2 * gamma)
        )

        term3 = -(gamma**3) * bracket

        val = term1 + term2 + term3

        return val

    def mu13(self):
        gamma = self.gamma
        eta = self.eta
        term1 = -(gamma**4) * (eta**4) / 24

        bracket1 = (
            np.exp(-gamma * eta) / (gamma**2) - 1 / (gamma**2) + eta / gamma
        )

        bracket2 = (
            np.exp(-gamma * eta) / (gamma**4)
            - 1 / (gamma**4)
            + eta / (gamma**3)
            - eta**2 / (2 * gamma**2)
            + eta**3 / (6 * gamma)
        )

        term2 = gamma**2 * bracket1
        term3 = -(gamma**4) * bracket2

        val = term1 + term2 + term3

        return val

    def mu21(self):
        gamma = self.gamma
        eta = self.eta
        # Leading terms
        term1 = -gamma * eta
        term2 = gamma**3 * eta**3 / 6
        term3 = -(gamma**5) * eta**5 / 120

        # First bracket (with gamma^5)
        bracket1 = (
            -np.exp(-gamma * eta) / gamma**5
            + 1 / gamma**5
            - eta / gamma**4
            + eta**2 / (2 * gamma**3)
            - eta**3 / (6 * gamma**2)
            + eta**4 / (24 * gamma)
        )
        term4 = -(gamma**5) * bracket1

        # Second bracket (with gamma^3)
        bracket2 = (
            -np.exp(-gamma * eta) / gamma**3
            + 1 / gamma**3
            - eta / gamma**2
            + eta**2 / (2 * gamma)
        )
        term5 = gamma**3 * bracket2

        # Third bracket (gamma^5 / 3!)
        bracket3 = (
            -6 * np.exp(-gamma * eta) / gamma**5
            + 6 / gamma**5
            - 6 * eta / gamma**4
            + 3 * eta**2 / gamma**3
            - eta**3 / gamma**2
            + eta**4 / (4 * gamma)
        )
        term6 = -(gamma**5 / 6) * bracket3

        # Fourth bracket (gamma^5)
        bracket4 = (
            4 * np.exp(-gamma * eta) / gamma**5
            - 4 / gamma**5
            + eta * np.exp(-gamma * eta) / gamma**4
            + 3 * eta / gamma**4
            - eta**2 / gamma**3
            + eta**3 / (6 * gamma**2)
        )
        term7 = -(gamma**5) * bracket4

        val = term1 + term2 + term3 + term4 + term5 + term6 + term7

        return val

    def mu22(self):
        gamma = self.gamma
        eta = self.eta
        term1 = 1
        term2 = -(gamma**2) * eta**2 / 2
        term3 = gamma**4 * eta**4 / 24

        # Bracket 1
        bracket1 = (
            np.exp(-gamma * eta) / gamma**4
            - 1 / gamma**4
            + eta / gamma**3
            - eta**2 / (2 * gamma**2)
            + eta**3 / (6 * gamma)
        )
        term4 = gamma**4 * bracket1

        # Bracket 2
        bracket2 = np.exp(-gamma * eta) / gamma**2 - 1 / gamma**2 + eta / gamma
        term5 = -(gamma**2) * bracket2

        # Bracket 3 (coefficient γ⁴ / 2!)
        bracket3 = (
            2 * np.exp(-gamma * eta) / gamma**4
            - 2 / gamma**4
            + 2 * eta / gamma**3
            - eta**2 / gamma**2
            + eta**3 / (3 * gamma)
        )
        term6 = (gamma**4 / 2) * bracket3

        # Bracket 4
        bracket4 = (
            -3 * np.exp(-gamma * eta) / gamma**4
            + 3 / gamma**4
            - eta * np.exp(-gamma * eta) / gamma**3
            - 2 * eta / gamma**3
            + eta**2 / (2 * gamma**2)
        )
        term7 = gamma**4 * bracket4

        val = term1 + term2 + term3 + term4 + term5 + term6 + term7

        return val

    def mu23(self):
        gamma = self.gamma
        eta = self.eta
        # Term 1
        term1 = gamma**5 * eta**5 / 120

        # Bracket 1 (gamma^3)
        bracket1 = (
            -np.exp(-gamma * eta) / gamma**3
            + 1 / gamma**3
            - eta / gamma**2
            + eta**2 / (2 * gamma)
        )
        term2 = -(gamma**3) * bracket1

        # Bracket 2 (gamma^5)
        bracket2 = (
            -np.exp(-gamma * eta) / gamma**5
            + 1 / gamma**5
            - eta / gamma**4
            + eta**2 / (2 * gamma**3)
            - eta**3 / (6 * gamma**2)
            + eta**4 / (24 * gamma)
        )
        term3 = gamma**5 * bracket2

        # Term 4
        term4 = 1 - np.exp(-gamma * eta)

        # Bracket 3 (gamma^5 / 3!)
        bracket3 = (
            -6 * np.exp(-gamma * eta) / gamma**5
            + 6 / gamma**5
            - 6 * eta / gamma**4
            + 3 * eta**2 / gamma**3
            - eta**3 / gamma**2
            + eta**4 / (4 * gamma)
        )
        term5 = (gamma**5 / 6) * bracket3

        # Bracket 4 (gamma^5)
        bracket4 = (
            4 * np.exp(-gamma * eta) / gamma**5
            - 4 / gamma**5
            + eta * np.exp(-gamma * eta) / gamma**4
            + 3 * eta / gamma**4
            - eta**2 / gamma**3
            + eta**3 / (6 * gamma**2)
        )
        term6 = gamma**5 * bracket4

        val = term1 + term2 + term3 + term4 + term5 + term6

        return val

    def mu31(self):
        gamma = self.gamma
        eta = self.eta
        exp = np.exp(-gamma * eta)

        # Term 1
        bracket1 = exp / gamma**2 - 1 / gamma**2 + eta / gamma
        term1 = gamma**2 * bracket1

        # Term 2
        bracket2 = (
            6 * exp / gamma**4
            - 6 / gamma**4
            + 6 * eta / gamma**3
            - 3 * eta**2 / gamma**2
            + eta**3 / gamma
        )
        term2 = -(gamma**4 / 6) * bracket2

        # Term 3
        bracket3 = (
            120 * exp / gamma**6
            - 120 / gamma**6
            + 120 * eta / gamma**5
            - 60 * eta**2 / gamma**4
            + 20 * eta**3 / gamma**3
            - 5 * eta**4 / gamma**2
            + eta**5 / gamma
        )
        term3 = (gamma**6 / 120) * bracket3

        # Term 4
        bracket4 = (
            -5 * exp / gamma**6
            + 5 / gamma**6
            - eta * exp / gamma**5
            - 4 * eta / gamma**5
            + 3 * eta**2 / (2 * gamma**4)
            - eta**3 / (3 * gamma**3)
            + eta**4 / (24 * gamma**2)
        )
        term4 = gamma**6 * bracket4

        # Term 5
        bracket5 = (
            -3 * exp / gamma**4
            + 3 / gamma**4
            - eta * exp / gamma**3
            - 2 * eta / gamma**3
            + eta**2 / (2 * gamma**2)
        )
        term5 = -(gamma**4) * bracket5

        # Term 6
        bracket6 = (
            -30 * exp / gamma**6
            + 30 / gamma**6
            - 6 * eta * exp / gamma**5
            - 24 * eta / gamma**5
            + 9 * eta**2 / gamma**4
            - 2 * eta**3 / gamma**3
            + eta**4 / (4 * gamma**2)
        )
        term6 = (gamma**6 / 6) * bracket6

        # Term 7
        bracket7 = (
            10 * exp / gamma**6
            - 10 / gamma**6
            + 4 * eta * exp / gamma**5
            + 6 * eta / gamma**5
            + eta**2 * exp / (2 * gamma**4)
            - 3 * eta**2 / (2 * gamma**4)
            + eta**3 / (6 * gamma**3)
        )
        term7 = gamma**6 * bracket7

        val = term1 + term2 + term3 + term4 + term5 + term6 + term7

        return val

    def mu32(self):
        gamma = self.gamma
        eta = self.eta
        exp = np.exp(-gamma * eta)

        # Term 1
        bracket1 = 1 / gamma - exp / gamma
        term1 = -gamma * bracket1

        # Term 2
        bracket2 = (
            -2 * exp / gamma**3
            + 2 / gamma**3
            - 2 * eta / gamma**2
            + eta**2 / gamma
        )
        term2 = (gamma**3 / 2) * bracket2

        # Term 3
        bracket3 = (
            -24 * exp / gamma**5
            + 24 / gamma**5
            - 24 * eta / gamma**4
            + 12 * eta**2 / gamma**3
            - 4 * eta**3 / gamma**2
            + eta**4 / gamma
        )
        term3 = -(gamma**5 / 24) * bracket3

        # Term 4
        bracket4 = (
            4 * exp / gamma**5
            - 4 / gamma**5
            + eta * exp / gamma**4
            + 3 * eta / gamma**4
            - eta**2 / gamma**3
            + eta**3 / (6 * gamma**2)
        )
        term4 = -(gamma**5) * bracket4

        # Term 5
        bracket5 = (
            2 * exp / gamma**3
            - 2 / gamma**3
            + eta * exp / gamma**2
            + eta / gamma**2
        )
        term5 = gamma**3 * bracket5

        # Term 6
        bracket6 = (
            8 * exp / gamma**5
            - 8 / gamma**5
            + 2 * eta * exp / gamma**4
            + 6 * eta / gamma**4
            - 2 * eta**2 / gamma**3
            + eta**3 / (3 * gamma**2)
        )
        term6 = -(gamma**5 / 2) * bracket6

        # Term 7
        bracket7 = (
            -6 * exp / gamma**5
            + 6 / gamma**5
            - 3 * eta * exp / gamma**4
            - 3 * eta / gamma**4
            - eta**2 * exp / (2 * gamma**3)
            + eta**2 / (2 * gamma**3)
        )
        term7 = -(gamma**5) * bracket7

        val = term1 + term2 + term3 + term4 + term5 + term6 + term7

        return val

    def mu33(self):
        gamma = self.gamma
        eta = self.eta
        exp = np.exp(-gamma * eta)

        # Term 1
        term1 = exp

        # Term 2
        bracket2 = (
            120 * exp / gamma**6
            - 120 / gamma**6
            + 120 * eta / gamma**5
            - 60 * eta**2 / gamma**4
            + 20 * eta**3 / gamma**3
            - 5 * eta**4 / gamma**2
            + eta**5 / gamma
        )
        term2 = -(gamma**6 / 120) * bracket2

        # Term 3
        bracket3 = (
            -3 * exp / gamma**4
            + 3 / gamma**4
            - eta * exp / gamma**3
            - 2 * eta / gamma**3
            + eta**2 / (2 * gamma**2)
        )
        term3 = gamma**4 * bracket3

        # Term 4
        bracket4 = (
            -5 * exp / gamma**6
            + 5 / gamma**6
            - eta * exp / gamma**5
            - 4 * eta / gamma**5
            + 3 * eta**2 / (2 * gamma**4)
            - eta**3 / (3 * gamma**3)
            + eta**4 / (24 * gamma**2)
        )
        term4 = -(gamma**6) * bracket4

        # Term 5
        bracket5 = -exp / gamma**2 + 1 / gamma**2 - eta * exp / gamma
        term5 = -(gamma**2) * bracket5

        # Term 6
        bracket6 = (
            -30 * exp / gamma**6
            + 30 / gamma**6
            - 6 * eta * exp / gamma**5
            - 24 * eta / gamma**5
            + 9 * eta**2 / gamma**4
            - 2 * eta**3 / gamma**3
            + eta**4 / (4 * gamma**2)
        )
        term6 = -(gamma**6 / 6) * bracket6

        # Term 7
        bracket7 = (
            3 * exp / gamma**4
            - 3 / gamma**4
            + 2 * eta * exp / gamma**3
            + eta / gamma**3
            + eta**2 * exp / (2 * gamma**2)
        )
        term7 = gamma**4 * bracket7

        # Term 8
        bracket8 = (
            10 * exp / gamma**6
            - 10 / gamma**6
            + 4 * eta * exp / gamma**5
            + 6 * eta / gamma**5
            + eta**2 * exp / (2 * gamma**4)
            - 3 * eta**2 / (2 * gamma**4)
            + eta**3 / (6 * gamma**3)
        )
        term8 = -(gamma**6) * bracket8

        val = term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8

        return val

    def sigma00(self):
        gamma = self.gamma
        eta = self.eta
        val = (
            ((2 * eta) / gamma)
            - (
                (np.exp(-2 * gamma * eta) - 4 * np.exp(-gamma * eta) + 3)
                / np.power(gamma, 2)
            )
            + ((4 * np.power(eta, 3) * gamma) / 3.0)
            + 2 * np.power(eta, 2) * np.exp(-eta * gamma)
            - 2 * np.power(eta, 2)
            - ((np.power(eta, 4) * np.power(gamma, 2)) / 2)
            + ((np.power(eta, 5) * np.power(gamma, 3)) / 10)
        )
        return val

    def sigma11(self):
        gamma = self.gamma
        eta = self.eta
        val = (
            (2 * eta * gamma)
            - np.exp(-2 * eta * gamma)
            - (2 * np.power(eta, 2) * np.power(gamma, 2))
            + ((2 * np.power(eta, 3) * np.power(gamma, 3)) / 3)
            - (4 * eta * gamma * np.exp(-eta * gamma))
            + 1
        )
        return val

    def sigma22(self):
        gamma = self.gamma
        eta = self.eta
        val = (
            (4 * np.exp(-eta * gamma))
            - ((13 * np.exp(-2 * eta * gamma)) / 2)
            + (8 * eta * gamma)
            - ((4 * np.power(eta, 3) * np.power(gamma, 3)) / 3)
            + ((np.power(eta, 5) * np.power(gamma, 5)) / 10)
            - (
                10
                * (np.power(eta, 2) * np.power(gamma, 2))
                * np.exp(-eta * gamma)
            )
            - (np.power(eta, 2) * np.power(gamma, 2)
                * np.exp(-2 * eta * gamma))
            - (
                2
                * (np.power(eta, 3) * np.power(gamma, 3))
                * np.exp(-eta * gamma)
            )
            - 12 * eta * gamma * np.exp(-eta * gamma)
            - 5 * eta * gamma * np.exp(-2 * eta * gamma)
            + 2.5
        )
        return val

    def sigma33(self):
        gamma = self.gamma
        eta = self.eta
        val = (
            (283 * eta) / 4
            + 88 * np.exp(-eta * gamma)
            - (397 * np.exp(-2 * eta * gamma)) / 8
            + 32 * eta * gamma
            + 84 * eta * np.exp(-eta * gamma)
            - (101 * eta * np.exp(-2 * eta * gamma)) / 4
            + (159 * eta) / (2 * gamma)
            - 24 * eta**2 * gamma
            + 6 * eta**3 * gamma
            + 32 * eta**2 * np.exp(-eta * gamma)
            - (eta**2 * np.exp(-2 * eta * gamma)) / 2
            + (204 * np.exp(-eta * gamma)) / gamma
            - (149 * np.exp(-2 * eta * gamma)) / (4 * gamma)
            + (192 * np.exp(-eta * gamma)) / gamma**2
            - (21 * np.exp(-2 * eta * gamma)) / (2 * gamma**2)
            - (39 * eta**2) / 2
            - 667 / (4 * gamma)
            - 363 / (2 * gamma**2)
            - 8 * eta**2 * gamma**2
            + (22 * eta**3 * gamma**2) / 3
            + (2 * eta**3 * gamma**3) / 3
            - 2 * eta**4 * gamma**2
            - (4 * eta**4 * gamma**3) / 3
            + (7 * eta**5 * gamma**3) / 15
            + (eta**5 * gamma**4) / 10
            - (eta**6 * gamma**4) / 15
            + (eta**7 * gamma**5) / 210
            + (96 * eta * np.exp(-eta * gamma)) / gamma
            - (9 * eta * np.exp(-2 * eta * gamma)) / (2 * gamma)
            + 36 * eta**2 * gamma * np.exp(-eta * gamma)
            - 6 * eta**2 * gamma * np.exp(-2 * eta * gamma)
            + 4 * eta**3 * gamma * np.exp(-eta * gamma)
            - 10 * eta**2 * gamma**2 * np.exp(-eta * gamma)
            - (77 * eta**2 * gamma**2 * np.exp(-2 * eta * gamma)) / 4
            + 10 * eta**3 * gamma**2 * np.exp(-eta * gamma)
            - (eta**3 * gamma**2 * np.exp(-2 * eta * gamma)) / 2
            - 2 * eta**3 * gamma**3 * np.exp(-eta * gamma)
            - (7 * eta**3 * gamma**3 * np.exp(-2 * eta * gamma)) / 2
            + eta**4 * gamma**3 * np.exp(-eta * gamma)
            - (eta**4 * gamma**4 * np.exp(-2 * eta * gamma)) / 4
            + 8 * eta * gamma * np.exp(-eta * gamma)
            - (197 * eta * gamma * np.exp(-2 * eta * gamma)) / 4
            - 307 / 8
        )
        return val

    def sigma01(self):
        gamma = self.gamma
        eta = self.eta
        exp1 = np.exp(eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)
        inner = (
            2 * exp1 + eta**2 * gamma**2 * exp1
            - 2 * eta * gamma * exp1 - 2
        )
        val = (exp2 * inner**2) / (4 * gamma)
        return val

    def sigma02(self):
        gamma = self.gamma
        eta = self.eta

        exp1 = np.exp(-eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)

        val = (
            4 * eta
            + 2 * eta * exp1
            - eta * exp2
            - 2 * eta**2 * gamma
            + (10 * exp1) / gamma
            - (5 * exp2) / (2 * gamma)
            - (15) / (2 * gamma)
            + (eta**3 * gamma**2) / 3
            + (eta**4 * gamma**3) / 4
            - (eta**5 * gamma**4) / 10
            + 2 * eta**2 * gamma * exp1
            + eta**3 * gamma**2 * exp1
        )
        return val

    def sigma03(self):
        gamma = self.gamma
        eta = self.eta
        exp1 = np.exp(-eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)

        val = (
            (7 * eta * exp2) / 2
            - 18 * eta * exp1
            - 8 * eta
            - (21 * eta) / (2 * gamma)
            + 5 * eta**2 * gamma
            - (5 * eta**3 * gamma) / 3
            - 8 * eta**2 * exp1
            - (36 * exp1) / gamma
            + (27 * exp2) / (4 * gamma)
            - (32 * exp1) / gamma**2
            + (2 * exp2) / gamma**2
            + 3 * eta**2
            + 117 / (4 * gamma)
            + 30 / gamma**2
            - 2 * eta**3 * gamma**2
            + (2 * eta**4 * gamma**2) / 3
            + (eta**4 * gamma**3) / 4
            - (3 * eta**5 * gamma**3) / 20
            + (eta**6 * gamma**4) / 60
            - (18 * eta * exp1) / gamma
            + (eta * exp2) / (2 * gamma)
            - 12 * eta**2 * gamma * exp1
            + (eta**2 * gamma * exp2) / 2
            - eta**3 * gamma * exp1
            - 4 * eta**3 * gamma**2 * exp1
            - (eta**4 * gamma**3 * exp1) / 2
        )
        return val

    def sigma12(self):
        gamma = self.gamma
        eta = self.eta
        exp1 = np.exp(-eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)

        val = (
            (5 * exp2) / 2
            - 4 * eta * gamma
            + 2 * eta**2 * gamma**2
            + (eta**3 * gamma**3) / 3
            - (eta**4 * gamma**4) / 4
            + 3 * eta**2 * gamma**2 * exp1
            + 8 * eta * gamma * exp1
            + eta * gamma * exp2
            - 5 / 2
        )
        return val

    def sigma13(self):
        gamma = self.gamma
        eta = self.eta

        exp1 = np.exp(-eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)

        val = (
            8 * eta * gamma
            - 4 * exp1
            - (27 * exp2) / 4
            - (3 * eta) / 2
            - 12 * eta * exp1
            - (eta * exp2) / 2
            - 3 * eta**2 * gamma
            - (10 * exp1) / gamma
            - (2 * exp2) / gamma
            + 12 / gamma
            - 5 * eta**2 * gamma**2
            + (5 * eta**3 * gamma**2) / 3
            + (2 * eta**3 * gamma**3) / 3
            - (5 * eta**4 * gamma**3) / 12
            + (eta**5 * gamma**4) / 20
            - eta**2 * gamma * exp1
            - 8 * eta**2 * gamma**2 * exp1
            - (eta**2 * gamma**2 * exp2) / 2
            - eta**3 * gamma**3 * exp1
            - 22 * eta * gamma * exp1
            - (7 * eta * gamma * exp2) / 2
            + 43 / 4
        )
        return val

    def sigma23(self):
        gamma = self.gamma
        eta = self.eta
        exp1 = np.exp(-eta * gamma)
        exp2 = np.exp(-2 * eta * gamma)

        val = (
            (143 * exp2) / 8
            - 12 * exp1
            - 7 * eta
            - 16 * eta * gamma
            + 18 * eta * exp1
            + (7 * eta * exp2) / 2
            + 6 * eta**2 * gamma
            + (2 * exp1) / gamma
            + (25 * exp2) / (4 * gamma)
            - 33 / (4 * gamma)
            + 2 * eta**2 * gamma**2
            - (4 * eta**3 * gamma**2) / 3
            + (4 * eta**3 * gamma**3) / 3
            - (eta**4 * gamma**3) / 12
            - (eta**4 * gamma**4) / 4
            + (eta**5 * gamma**4) / 10
            - (eta**6 * gamma**5) / 60
            + 5 * eta**2 * gamma * exp1
            + (eta**2 * gamma * exp2) / 2
            + 20 * eta**2 * gamma**2 * exp1
            + (19 * eta**2 * gamma**2 * exp2) / 4
            + 5 * eta**3 * gamma**3 * exp1
            + (eta**3 * gamma**3 * exp2) / 2
            + (eta**4 * gamma**4 * exp1) / 2
            + 24 * eta * gamma * exp1
            + (63 * eta * gamma * exp2) / 4
            - 47 / 8
        )
        return val

    def sigma(self, d):
        s00 = self.sigma00()
        s01 = self.sigma01()
        s02 = self.sigma02()
        s03 = self.sigma03()
        s11 = self.sigma11()
        s12 = self.sigma12()
        s13 = self.sigma13()
        s22 = self.sigma22()
        s23 = self.sigma23()
        s33 = self.sigma33()

        I_d = np.eye(d)

        top_mat = np.hstack([s00 * I_d, s01 * I_d, s02 * I_d, s03 * I_d])
        mid_mat1 = np.hstack([s01 * I_d, s11 * I_d, s12 * I_d, s13 * I_d])
        mid_mat2 = np.hstack([s02 * I_d, s12 * I_d, s22 * I_d, s23 * I_d])
        bot_mat = np.hstack([s03 * I_d, s13 * I_d, s23 * I_d, s33 * I_d])

        mat = np.vstack([top_mat, mid_mat1, mid_mat2, bot_mat])
        epsilon = 0.00001
        matrix = mat + epsilon * np.eye(4 * d)

        return matrix
