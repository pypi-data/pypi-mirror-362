from setuptools import setup, find_packages

setup(
    name="phosadsorption",
    version="0.2.3",
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
    long_description="Phosphorus adsorption predictor using XGBoost with soil input data",
    long_description_content_type="text/markdown",
    url="https://github.com/Mil-afk/soil_phosphorus_adsorption_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
