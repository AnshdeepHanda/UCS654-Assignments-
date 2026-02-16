from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Anshdeep-102303124",
    version="1.0.0",
    author="Anshdeep Handa",
    author_email="anshdeep@example.com",
    description="A Python package for implementing TOPSIS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'topsis=Topsis_Anshdeep_102303124.topsis:main',
        ],
    },
)