# Higher-Order Langevin Monte Carlo Algorithms

This repository contains the implementation and experimental evaluation of generalized Higher-Order Langevin Monte Carlo (HoLMC) algorithms for Bayesian inference. We focus on third- and fourth-order underdamped Langevin samplers and demonstrate their performance in both regression and classification tasks using real-world datasets.

The implementation is done by creating a Python package called `holmc`.
The package is modular and reproducible, with symbolic derivations, numerical validation, and Wasserstein-2 distance–based performance evaluation. All code, figures, and notebooks are included for easy experimentation and extension.

## Installation

To set up the environment and install dependencies:

1. Create a virtual environment:

```bash
python3 -m venv holmc_env
```

2. Activate the environment:

**On macOS/Linux:**

```bash
source holmc_env/bin/activate
```

**On Windows:**

```bash
holmc_env\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
pip install -e .
```

4. *(Optional)* Create a new Jupyter kernel:

```bash
python -m ipykernel install --user --name=holmc_env --display-name "holmc_env"
```

## Project Structure

```
.
├── docs/                   # Symbolic derivations (MATLAB, Mathematica, Jupyter)
├── experiments/            # Regression and classification notebooks
├── holmc/                  # Core package (samplers, utils, metrics)
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup script
├── pyproject.toml          # Build configuration
├── README.md               # This file
└── LICENSE                 # License information
```

## Citation

This repository contains the official implementation for the methods and experiments described in our forthcoming journal publication:

**Higher-Order Langevin Monte Carlo Algorithms**, by *T.L. Dang*, *M. Gürbüzbalaban*, *M. R. Islam*, *N. Yao* and *L. Zhu*

A full citation will be added upon publication.

If you use this code in your work, please cite this repository as:

```bibtex
@misc{islam2025holmc,
  author       = {Rafiq Islam},
  title        = {Codebase for Higher-Order Langevin Monte Carlo Algorithms},
  year         = {2025},
  howpublished = {\url{https://github.com/mrislambd/higher-order-Langevin-dynamics}}
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
