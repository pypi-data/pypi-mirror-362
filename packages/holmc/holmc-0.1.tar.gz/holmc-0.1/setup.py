from setuptools import setup, find_packages

requirements_dev = ["black", "isort", "pre-commit"]


setup(
    name="holmc",
    version="0.1",
    description="Higher Order Langevin Monte Carlo- A MCMC sampler \
        for Bayesian inference",
    author="Rafiq Islam",
    author_email="rislam@fsu.edu",
    license="MIT",
    packages=find_packages(where=".", include=["holmc", "holmc.*"]),
    install_requires=[
        "numpy",
        "matplotlib",
        "seaborn",
        "tqdm",
        "scipy",
        "pandas",
        "sympy",
        "scikit-learn",
        "ucimlrepo",
    ],
    extras_require={"dev": requirements_dev},
)