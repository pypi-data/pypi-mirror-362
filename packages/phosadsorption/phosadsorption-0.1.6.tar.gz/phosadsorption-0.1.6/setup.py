
from setuptools import setup, find_packages

setup(
    name="phosadsorption",
    version="0.1.6",
    packages=find_packages(include=["phosadsorption", "phosadsorption.*"]),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "xgboost",
        "openpyxl",
        "matplotlib"
    ],
    author="Miltiadis Iatrou",
    description="Library for predicting phosphorus adsorption in soil",
    long_description="Predicts phosphorus adsorption and fertilizer productivity based on soil inputs.",
    long_description_content_type="text/markdown",
    url="https://github.com/Mil-afk/soil_phosphorus_adsorption_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
