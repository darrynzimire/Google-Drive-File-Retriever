from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='UTF-8') as handle:
    long_description = handle.read()

setup(
    name=f'raw file retriever',
    version='0.0.1',
    description='This is a simple script that takes in a list of files to search and retrieve '
                'from a Google drive and writes the files to a desired output directory',

    long_description=long_description,
    author='Darryn Zimire',
    author_email='darryn.zimire@uct.ac.za',
    licence='MIT License'



)