"""
Utility functions for compression/decompression
Author: Nicolas Soler (SDM)
"""

import os
import logging


def absolute_path(file_path: str = None) -> str:
    return os.path.realpath(os.path.abspath(file_path))


def check_existence(
    file_path: str = None, dataset_path: str = "entry/data/data"
) -> bool:
    """
    Check that the file exists
    """
    if not os.path.exists(absolute_path(file_path)):
        return False

    return True


def check_extension(file_path, required_extension: str = ".h5") -> bool:
    """
    Check the required extension
    """
    _, ext = os.path.splitext(file_path)
    if ext.lower() != required_extension.lower():
        return False

    return True


def new_hdf5_path(
    input_hdf5_path: str, suffix: str = "compressed_", remove=False
) -> str:
    """
    Create a new file name from an input file, given a suffix
    remove: if True, remove a preexisting file with the same name if it exists
    """
    input_path, input_base = os.path.split(input_hdf5_path)
    output_hdf5_path = os.path.join(input_path, suffix + input_base)

    if remove and os.path.exists(output_hdf5_path):
        logging.warning(f"Removing previous compressed dataset {output_hdf5_path}")
        os.remove(output_hdf5_path)

    return output_hdf5_path
