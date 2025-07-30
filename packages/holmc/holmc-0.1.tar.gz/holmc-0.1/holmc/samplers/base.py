import numpy as np
from holmc.utils.params import O3Params, O4Params


class HoLMCSamplerOrderThree:
    def __init__(
        self,
        eta: float = None,
        gamma: float = None,
        xi: float = None,
        N: int = None,
        seed: int = None,
        show_progress: bool = True,
    ):
        self.eta = eta
        self.gamma = gamma
        self.xi = xi
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        self.params = O3Params(gamma=gamma, eta=eta, xi=xi)
        if seed is not None:
            np.random.seed(seed)
    
    def sample(
        self, X: np.ndarray, y: np.ndarray, lamb: float = None
    ) -> np.ndarray:
        # Placeholder for the actual sampling logic
        # This should implement the sampling algorithm for order 3
        raise NotImplementedError(
            "Child classes must implement the sample() method."
        )


class HoLMCSamplerOrderFour:
    def __init__(
        self,
        eta: float = None,
        gamma: float = None,
        N: int = None,
        seed: int = None,
        show_progress: bool = True
    ):
        self.eta = eta
        self.gamma = gamma
        self.N = N
        self.seed = seed
        self.show_progress = show_progress
        self.params = O4Params(gamma=gamma, eta=eta)
        if seed is not None:
            np.random.seed(seed)
    
    def sample(
        self, X: np.ndarray, y: np.ndarray, lamb: float = None
    ) -> np.ndarray:
        # Placeholder for the actual sampling logic
        # This should implement the sampling algorithm for order 4
        raise NotImplementedError(
            "Child classes must implement the sample() method."
        )