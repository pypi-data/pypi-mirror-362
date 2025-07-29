from setuptools import setup

setup(
    name="sqpax",
    version="0.0.0",
    description="solving sqp trajectory optimization problems with jax",
    author="Karen Leung",
    author_email="kymleung@uw.edu",
    packages=["sqpax"],
    install_requires=[
        "jax",
        "numpy",
        "equinox",
        "qpax",
        "dynamaxsys",
        "matplotlib"
    ],
)
