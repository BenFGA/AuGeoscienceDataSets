Collection of useful links and python code to extract and manipulate Australia Geoscience Datasets.

Of most general interest is the file reader for WADG files.

## Installation

To install into a new poetry environment for the base functionality:

```commandline
poetry install
```

Or to run the example with matplotlib visualisation

```commandline
poetry install --extras viz
# poetry install --all-extras  # alternatively
```

If installing from pip the equivalent commands are:

```commandline
pip install git+https://github.com/FractalGeoAnalytics/AuGeoscienceDataSets.git
```
or 
```commandline
pip install git+https://github.com/FractalGeoAnalytics/AuGeoscienceDataSets.git#AuGeoscienceDataSets[viz]
```

