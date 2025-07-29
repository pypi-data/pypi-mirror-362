
from setuptools import setup, find_packages

setup(
    name="phosadsorption",
    version="0.2.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy",
        "xgboost>=1.7.0",
        "matplotlib",
        "openpyxl"
    ],
    author="Miltiadis Iatrou",
    description="Library for predicting phosphorus adsorption in soil",
    long_description="Phosadsorption is a Python package for predicting percentage phosphorus adsorption in soils using XGBoost models.",
    long_description_content_type="text/markdown",
    url="https://github.com/Mil-afk/soil_phosphorus_adsorption_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
