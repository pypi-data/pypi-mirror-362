from setuptools import setup
import setuptools

import vecstore

with open('vecstore/requirements.txt') as f:
    required = f.read().splitlines()
with open("README.md", "r") as f:
    long_description = f.read()

version = vecstore.__version__
setup(name='vecstore',
      version=version,
      description="Dynamically expandable Vector Store for embeddings, using the HNSW library",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ptarau/vecstore.git',
      author='Paul Tarau',
      author_email='ptarau@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      package_data={
          'vecstore': [
            '*.txt'
          ]
      },
      include_package_data=True,
      install_requires=required,
      zip_safe=False
      )
