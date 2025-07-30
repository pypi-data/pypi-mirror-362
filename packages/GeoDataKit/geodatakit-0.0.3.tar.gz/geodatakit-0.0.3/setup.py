# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
setup(name='GeoDataKit',
      version='0.0.3',
      url='https://github.com/GeoISTO/GeoDataKit',
      license='MIT',
      author='Gautier Laurent',
      author_email='gautier.laurent@univ-orleans.fr',
      description='Analyses and graphs for geoscience',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['seaborn>=0.11.2',
                      'pandas>=1.3',
                      'numpy>=1.20',
                      'matplotlib>=3.5',
                      ],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Science/Research",
          "Natural Language :: English",
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering :: Visualization"
          ]
      )
