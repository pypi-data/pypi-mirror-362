"""Setup configuration for CRCreditum package."""

from setuptools import setup, find_packages
import os

# Read the long description from README
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

# Read requirements from requirements.txt
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crcreditum",
    version="1.0.6",
    author="CRCreditum Team",
    author_email="support@crcreditum.com",
    description="Advanced Credit Risk Assessment with CRA Compliance and Basel III Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crcreditum/crcreditum",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ],
        "ml": [
            "lightgbm>=3.3.0",
            "catboost>=1.1.0",
            "optuna>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "crcreditum=crcreditum.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "crcreditum": ["py.typed"],
    },
    keywords=[
        "credit risk", "basel iii", "cra compliance", "financial modeling",
        "stress testing", "explainable ai", "regulatory compliance"
    ],
    project_urls={
        "Documentation": "https://docs.crcreditum.com",
        "Source": "https://github.com/crcreditum/crcreditum",
        "Tracker": "https://github.com/crcreditum/crcreditum/issues",
    },
)