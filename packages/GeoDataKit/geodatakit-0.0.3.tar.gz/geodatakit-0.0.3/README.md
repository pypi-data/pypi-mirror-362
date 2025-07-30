

[![DOI](https://zenodo.org/badge/578120061.svg)](https://zenodo.org/doi/10.5281/zenodo.11450482)


# GeoDataKit
Python tools for geoscience data analysis and visualisation

NB: this is really preliminary developments

## Demo
Demonstration Notebooks are available in the [./notebook](./notebook) directory.

Available notebooks:
1. Rose Diagram demo
2. Hough Transform demo


## Installation
```
pip install  GeoDataKit
```


## Dev
Building distribution:
```
python setup.py sdist bdist_wheel
```

Pushing to PYPI:
```
twine upload --verbose dist/*
```

