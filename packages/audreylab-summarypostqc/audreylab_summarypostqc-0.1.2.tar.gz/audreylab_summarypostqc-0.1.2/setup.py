from setuptools import setup, find_packages

setup(
    name="audreylab-summarypostqc",
    version="0.1.2",
    author="Etienne Kabongo",
    author_email="etienne.kabongo@mail.mcgill.ca",
    description="GWAS Summary Statistics QC Plotting and Annotation Tool from the Audrey Grant Lab",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EtienneNtumba/audreylab-summarypostqc",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "pybiomart",
        "myvariant",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    entry_points={
        "console_scripts": [
            "audreylab-summarypostqc=audreylab_summarypostqc.cli:main",
        ],
    },
    python_requires='>=3.7',
)

