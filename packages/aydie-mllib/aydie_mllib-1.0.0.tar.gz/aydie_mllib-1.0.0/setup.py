# setup.py

from setuptools import setup, find_packages
from pathlib import Path

# --- Read the README for the long description ---
# This is a good practice to avoid duplicating content.
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# --- Project Metadata ---
PROJECT_NAME = "aydie_mllib"
VERSION = "1.0.0"
AUTHOR = "Aditya (Aydie) Dinesh K"  
AUTHOR_EMAIL = "business@aydie.in" 
DESCRIPTION = "A Python library to automate machine learning model training and tuning using a simple configuration file."
REPO_URL = "https://github.com/aydiegithub/aydie-mllib" 

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=REPO_URL,
    
    packages=find_packages(),
    
    install_requires=[
        "PyYAML",
        "scikit-learn",
        "xgboost"
    ],
    

    classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
],
    python_requires='>=3.7',
)
