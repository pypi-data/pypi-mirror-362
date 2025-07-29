from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

setup(
    name="pypsoa",
    version="0.1.0",
    author="Ahmet Atasoglu",
    author_email="ahmetatasoglu98@gmail.com",
    description="A simple, zero-dependency Particle Swarm Optimization (PSO) library for Python.",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/atasoglu/pypsoa",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
