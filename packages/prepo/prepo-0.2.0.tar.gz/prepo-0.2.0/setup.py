from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prepo",
    version="0.2.0",
    author="Erik Hoxhaj",
    author_email="erik.hoxhaj@outlook.com",
    description="A Python package with automated data type detection, KNN imputation, outlier removal, and multiple scaling methods using type-safe enum architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erikhox/prepo",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Scientists",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "performance": [
            "polars>=0.20.0",
            "pyarrow>=10.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xvfb>=3.0.0",  # For headless testing
            "coverage>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "cli": [
            "click>=8.0.0",
        ],
        "all": [
            "polars>=0.20.0",
            "pyarrow>=10.0.0",
            "click>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prepo=prepo.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/erikhox/prepo/issues",
        "Source": "https://github.com/erikhox/prepo",
        "Documentation": "https://github.com/erikhox/prepo#readme",
        "Changelog": "https://github.com/erikhox/prepo/blob/main/CHANGELOG.md",
    },
    keywords="pandas preprocessing data-science feature-engineering machine-learning automation type-detection knn-imputation scaling outlier-detection cli polars pyarrow",
    include_package_data=True,
    zip_safe=False,
)
