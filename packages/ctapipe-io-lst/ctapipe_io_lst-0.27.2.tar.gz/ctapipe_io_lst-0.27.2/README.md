# ctapipe_io_lst [![CI](https://github.com/cta-observatory/ctapipe_io_lst/actions/workflows/ci.yml/badge.svg)](https://github.com/cta-observatory/ctapipe_io_lst/actions/workflows/ci.yml)

EventSource Plugin for ctapipe, able to read LST zfits files
and calibration them to R1 as needed for ctapipe tools.

Since version 0.19, `ctapipe_io_lst` is on conda-forge,
which is the easiest way to install it, since the `protozfits`
dependency is offered pre-compiled for Linux and mac OS (including arm64).

To install into an exisiting environtment, just do:
```
# or conda
$ mamba install -c conda-forge ctapipe_io_lst
```

For development, create a new environment and run the development install:
```
conda env create -n lstenv -f environment.yml
conda activate lstenv
pip install -e .
```

`ctapipe_io_lst` is also on PyPI, but note that the `protozfits`
dependency only has wheels for Linux, so you'd need to compile 
from source on mac OS.

## Test Data

To run the tests, a set of non-public files is needed.
If you are a member of CTA, ask one of the project maintainers for the credentials
and then run

```
./download_test_data.sh
```
