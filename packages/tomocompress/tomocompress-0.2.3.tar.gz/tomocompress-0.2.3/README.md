# Tomocompress

Simple-to-use compression tool for tomographic HDF5 file compression (developed with __Python 3.12__).

A command-line executable named  **tomocompress** is installed. It is a wrapper for the [Blosc2](https://www.blosc.org/) [Grok](https://grokcompression.com/) [JPEG2K](https://jpeg.org/jpeg2000/) to compress tomography raw NeXus/HDF5 in a lossy fashion. This work was financed by the [LEAPS-INNOV project](https://www.leaps-innov.eu/).


## Install Tomocompress
```bash

# Optionally, create a dedicated conda env with Python 3.12
$ conda create -n tomocompress python=3.12
$ conda activate tomocompress

# Install the latest wheel from PyPI
$ pip install tomocompress

# It installs a command-line tool called tomocompress
```

## Run Tomocompress 

```bash
# Activate your conda env if needed
$ conda activate tomocompress

# Run it!
$ tomocompress myfile.h5

# More options
$ tomocompress --help

# Result
A file called compressed_grok_myfile.h5 next to the input hdf5 file.

# Examples

## If your dataset is not called 'data' but 'something' in your hdf5 arborescence
$ tomocompress myfile.h5 -d something

## Specify more than one dataset to compress (comma-separated)
## note: the program will look for these dataset names in the HDF5 arborescence
## so that you don't have to enter their full path
$ tomocompress myfile.h5 -d "data,dark,flat"

## Specify a target compression ratio of 10 (default 4)
$ tomocompress myfile.h5 -c 10
```
## Output file
By default, a compressed file bearing a suffix is created in the same directory as the original file.
You can change this behaviour by specifying either a path to a directory or a full file path 
```bash
$ tomocompress myfile.h5 -o /some/other/path/compressed.h5

# only specifying a directory, a suffix will be appended to the name of the original file
$ tomocompress myfile.h5 -o /some/other/path

```

## Reading compressed files (Python)
Provided that the **hdf5plugin** and **blosc2-grok** Python packages are installed,
it is possible to read back the written data with h5py.

```python

import blosc2_grok
import h5py
import hdf5plugin

with h5py.File("my_compressed_file.h5", "r") as h5f:
    read_data = h5f["data"][()]
```

See the __doc__ and __scripts__ folders for more resources.

## Programmatic usage (Python):

```python
from tomocompress.compressor import Blosc2GrokCompressor

# Input HDF5 tomo file to compress
input_tomo_file = sys.argv[1]

# The dataset name you want to compress inside the input HDF5 file (default:data)
# If not specified, it will try to find automatically a dataset called "data" in the file arborescence
dataset_names = "data,dark,flat"

# Desired compression ratio
CR = 20               # desired compression ratio

# This will write the compressed file in the same directory as the original one
grok_compressor =  Blosc2GrokCompressor(input_hdf5=input_tomo_file, compression_ratio=CR, dataset_names=dataset_names, output_file_path="/some/path")
grok_compressor.compress()

```
## Recommended Python version
3.12

## Authors and acknowledgment
Nicolas Soler (SDM) Alba Synchrotron

## License
See LICENSE.rst

## Gitlab page
https://gitlab.com/alba-synchrotron/sdm/tomocompress

## PyPI page
https://pypi.org/project/tomocompress/

## Project status
stable
