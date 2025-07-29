from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        # Fallback requirements if requirements.txt is not available
        return [
            "numpy>=1.19.0",
            "scikit-learn>=1.0.0", 
            "pandas>=1.3.0",
            "scipy>=1.7.0",
            "econml>=0.13.0"
        ]

setup(
    name="pyhtelasso",
    version="0.1.0",
    author="Vasco Yasenov",
    author_email="yasenov@gmail.com",
    description="A Python package for detecting treatment effect heterogeneity using debiased lasso",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyhtelasso",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "full": [
            "econml>=0.13.0",
            "scipy>=1.7.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="causal inference, treatment effects, heterogeneity, lasso, debiased lasso, econometrics",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pyhtelasso/issues",
        "Source": "https://github.com/yourusername/pyhtelasso",
        "Documentation": "https://github.com/yourusername/pyhtelasso#readme",
    },
)
