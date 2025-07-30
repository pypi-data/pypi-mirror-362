from setuptools import setup, find_packages
from typing import List
    
with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()
    
__version__ = "0.1.8"
REPO_NAME = "DynamicTS"
PACKAGE_NAME = "dynamicts"
ORGANISATION_USERNAME = "Chinar-Quantum-AI-Ltd"
ORGANISATION_EMAIL = "engineering@chinarqai.com"


setup(
    name=PACKAGE_NAME,
    version=__version__,
    description='A library for time series analysis and preprocessing',
    author=ORGANISATION_USERNAME,
    author_email=ORGANISATION_EMAIL,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{ORGANISATION_USERNAME}/{REPO_NAME}",
    project_urls={
        "Issue Tracker": f"https://github.com/{ORGANISATION_USERNAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "."},
    packages=find_packages(include=["dynamicts"]),
)
