from setuptools import setup, find_packages

setup(
    name="FiltpostQC-EU",
    version="0.1.1",
    author="Etienne Kabongo",
    author_email="etienne@example.com",
    description="A CLI tool to apply post-GWAS QC filtering to Regenie merged summary statistics using EU-based variant filters.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EtienneNtumba/FiltpostQC-EU",  # modifie si tu publies sur GitHub
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0"
    ],
    entry_points={
        "console_scripts": [
            "filtpostqc-eu=filtpostqc_eu.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)

