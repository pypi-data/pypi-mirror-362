from setuptools import setup, find_packages
from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='cssfix',
    version='2.0.1',
    packages=find_packages(),
    description='Simple CSS optimizer module for merging class properties',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='seekii',
    author_email='seekii.official@example.com',
    url='https://github.com/seekiii/cssfix',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
