from setuptools import setup, find_packages

setup(
    name="FiltpostQC-EU",
    version="0.1.0",
    author="Etienne Kabongo",
    author_email="etienne@example.com",
    description="A CLI tool to apply post-GWAS QC filtering to Regenie merged summary statistics using EU-based variant filters.",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "filtpostqc-eu=filtpostqc_eu.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    license="MIT",
    include_package_data=True,
)

