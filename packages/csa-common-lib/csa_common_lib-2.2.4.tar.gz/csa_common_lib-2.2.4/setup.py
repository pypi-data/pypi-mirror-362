from setuptools import setup, find_packages
import pathlib


# Locate the current directory where setup.py is located
HERE = pathlib.Path(__file__).parent

# Read the README.md file for the long description
# engine_long_description = (HERE / "pip_setup/prediction_engine_readme.md").read_text()

common_lib_long_description = (HERE / "pip_setup/common_lib_readme.md").read_text()

# setup(
#     name='csa_prediction_engine',
#     version="2.2.3",
#     author="Cambridge Sports Analytics",
#     author_email="prediction@csanalytics.io",
#     description="The csa_prediction_engine library provides a suite of tools and functions for performing relevance-based predictions using the Cambridge Sports Analytics Prediction Engine API. The package is designed to facilitate single and multi-task predictions, allowing for flexible model evaluation and experimentation.",
#     long_description=engine_long_description,
#     long_description_content_type="text/markdown",
#     packages=find_packages(include=['csa_prediction_engine', 'csa_prediction_engine.*']),
#     install_requires=[
#         'numpy>=2.1',
#         'requests',
#         'csa_common_lib>=2.2.3'
#     ]
# )

setup(
    name='csa_common_lib',
    version="2.2.4",
    author="Cambridge Sports Analytics",
    author_email="prediction@csanalytics.io",
    description="csa_common_lib is a shared library designed to provide utility modules, class definitions, enumerations, and helper functions for the CSA Prediction Engine Python client. It standardizes and simplifies complex operations across different parts of the CSA Prediction Engine.",
    long_description=common_lib_long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['csa_common_lib', 'csa_common_lib.*']),
    install_requires=[
        'boto3==1.35.20',
        'numpy==2.1.1',
        'openpyxl==3.1.5',
        'pandas==2.2.2',
        'plotnine==0.13.6',
        'requests==2.32.3',
    ]
)