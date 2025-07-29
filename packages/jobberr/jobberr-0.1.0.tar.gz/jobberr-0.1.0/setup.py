# setup.py
from setuptools import setup, find_packages

setup(
    name="jobberr",
    version="0.1.0",
    description="run python job",
    author="Dyotak",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "jobberr= jobber.cli:main",
        ],
    },

    install_requires=[]
)