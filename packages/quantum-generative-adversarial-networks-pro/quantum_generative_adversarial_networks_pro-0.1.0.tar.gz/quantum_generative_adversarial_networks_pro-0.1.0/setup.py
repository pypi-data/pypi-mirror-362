#!/usr/bin/env python3
"""
Setup script for quantum-generative-adversarial-networks-pro

This setup.py is provided for compatibility with tools that don't yet support
pyproject.toml. The canonical build configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    """Read README.md for long description."""
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Define dependencies
install_requires = [
    "qiskit>=1.0.0",
    "pennylane>=0.30.0",
    "torch>=1.12.0",
    "torchvision>=0.13.0",
    "numpy>=1.21.0",
    "matplotlib>=3.5.0",
    "scikit-learn>=1.1.0",
    "scipy>=1.8.0",
    "tqdm>=4.64.0",
    "typer[all]>=0.9.0",
    "pillow>=9.0.0",
    "pandas>=1.4.0",
    "seaborn>=0.11.0",
]

# Define optional dependencies
extras_require = {
    'docs': [
        "mkdocs>=1.5.0",
        "mkdocs-material>=9.0.0",
        "mkdocstrings[python]>=0.20.0",
        "mkdocs-jupyter>=0.24.0",
    ],
    'dev': [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=22.0.0",
        "isort>=5.10.0",
        "flake8>=5.0.0",
        "pre-commit>=2.20.0",
    ],
    'jupyter': [
        "jupyter>=1.0.0",
        "ipykernel>=6.15.0",
        "ipywidgets>=8.0.0",
    ],
}

# Add 'all' extra that includes everything
extras_require['all'] = list(set(sum(extras_require.values(), [])))

setup(
    name="quantum-generative-adversarial-networks-pro",
    version="0.1.0",
    description="Quantum-enhanced GAN framework for high-fidelity synthetic data generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Krishna Bajpai",
    author_email="bajpaikrishna715@gmail.com",
    url="https://github.com/krish567366/quantum-generative-adversarial-networks-pro",
    project_urls={
        "Homepage": "https://github.com/krish567366/quantum-generative-adversarial-networks-pro",
        "Documentation": "https://krish567366.github.io/quantum-generative-adversarial-networks-pro/",
        "Repository": "https://github.com/krish567366/quantum-generative-adversarial-networks-pro",
        "Issues": "https://github.com/krish567366/quantum-generative-adversarial-networks-pro/issues",
        "Bug Reports": "https://github.com/krish567366/quantum-generative-adversarial-networks-pro/issues",
        "Source": "https://github.com/krish567366/quantum-generative-adversarial-networks-pro",
    },
    packages=find_packages(include=['qgans_pro', 'qgans_pro.*']),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'qgans-pro=qgans_pro.cli:app',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
        "Typing :: Typed",
    ],
    keywords=[
        "quantum computing",
        "generative adversarial networks",
        "machine learning",
        "qiskit",
        "pennylane",
        "quantum machine learning",
        "synthetic data",
        "deep learning",
        "artificial intelligence",
        "quantum circuits",
        "variational quantum circuits",
        "quantum algorithms",
        "bias mitigation",
        "fairness",
    ],
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    package_data={
        'qgans_pro': [
            'data/*',
            'configs/*',
            'examples/*',
        ],
    },
    # Additional metadata for better discoverability
    platforms=["any"],
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
)
