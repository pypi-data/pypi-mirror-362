import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'aecroscopy/__version__.py')) as f:
    __version__ = f.read().split("'")[1]

with open("README.md", "r") as fr:
    long_description = fr.read()

setup(name='aecroscopy',
      version=__version__,
      description='Acquisition software for microscopy developed at CNMS ORNL',
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://code.ornl.gov/rvv/aecroscopy',
      author='Rama Vasudevan, Yongtao Liu, Mani Valleti',
      license='MIT',
      packages=find_packages(exclude='tests'),
      zip_safe=False)
