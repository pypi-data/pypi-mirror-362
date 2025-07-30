"""
Class to manage HDF5 data
Author: Nicolas Soler (SDM)
"""

import os
import sys
import h5py
import hdf5plugin
import logging
from tomocompress.utils import absolute_path, check_existence
from tomocompress.constants import DEFAULT_CHUNK_SIZE


class Hdf5DataFile:
    """
    Class to manage HDF5 data files, providing methods to read datasets and their attributes.
    """

    def __init__(
        self,
        path: str,
        dataset_names: str = "data,dark,flat",
        chunk_size=DEFAULT_CHUNK_SIZE,
    ):
        self.path = absolute_path(path)
        self.folder = os.path.dirname(self.path)
        self.dataset_names = dataset_names
        self.dataset_obj_list = []
        self._data_attributes = dict()
        self.chunk_size = chunk_size

        if not check_existence(self.path):
            raise FileNotFoundError(f"Input HDF5 file {self.path} not found!")

        for dataset_name in self._dataset_name_list:
            self.dataset_obj_list.append(
                Hdf5Dataset(
                    file_path=self.path,
                    dataset_name=dataset_name,
                    chunk_size=self.chunk_size,
                )
            )

        with h5py.File(self.path, "r") as infile:
            self._data_attributes["file_size"] = os.path.getsize(self.path)
            self._data_attributes["n_datasets"] = len(infile.keys())

    @property
    def _dataset_name_list(self) -> list:
        if self.dataset_names is None:
            return ["data"]
        return [d.strip() for d in self.dataset_names.split(",")]

    def copy_without_data(self, output_path: str = None) -> str:
        """
        Copy the structure of the input HDF5 file without the data
        """
        if output_path is None:
            output_path = os.path.splitext(self.path)[0] + "_no_data.h5"

        logging.debug("Excluding", self.dataset_names)

        list_of_dataset_paths_to_exclude = [
            dataset.dataset_path for dataset in self.dataset_obj_list
        ]
        self.copy_hdf5_except_dataset(
            self.path, output_path, list_of_dataset_paths_to_exclude
        )

        return output_path

    def copy_hdf5_except_dataset(
        self, input_path: str, output_path: str, exclude_datasets: list
    ):
        """
        Copies the entire HDF5 file except for a specified dataset.

        Parameters:
            input_path (str): Path to the input HDF5 file.
            output_path (str): Path to the output HDF5 file.
            exclude_dataset (str): list of paths of the datasets to exclude (absolute path in the HDF5 file).

        Returns:
            str: Path to the copied HDF5 file.
        """

        def recursive_copy(source, dest, exclude_path_list):
            for key in source:
                obj = source[key]
                if isinstance(obj, h5py.Group):
                    # Create a group in the destination and copy recursively
                    new_group = dest.create_group(key)
                    # Copy group attributes
                    for attr_name, attr_value in obj.attrs.items():
                        new_group.attrs[attr_name] = attr_value
                    recursive_copy(obj, new_group, exclude_path_list)
                elif isinstance(obj, h5py.Dataset):
                    # Skip the excluded dataset
                    full_path = obj.name
                    logging.debug(f"Full path found: {full_path}")
                    if full_path in exclude_path_list:
                        logging.debug(f"Skipping dataset: {full_path}")
                        continue
                    # Copy the dataset
                    dest.copy(obj, key)

        with h5py.File(input_path, "r") as src, h5py.File(output_path, "w") as dest:
            # Copy file-level attributes
            for attr_name, attr_value in src.attrs.items():
                dest.attrs[attr_name] = attr_value
            # Recursively copy groups and datasets
            recursive_copy(src, dest, exclude_datasets)

        return output_path


class Hdf5Dataset:
    def __init__(
        self,
        file_path: str,
        dataset_name: str = "data",
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        self.file_path = absolute_path(file_path)
        self.dataset_name = dataset_name
        self._chunk_size = chunk_size  # in order to copy the dataset chunk by chunk (1 image by default)

        # These objects are created in the __init__ of Hdf5DataFile
        # So if there is a problem, the program will quit right away
        if not self.check_integrity():
            logging.error("Exiting")
            sys.exit(1)

        # data attributes for each dataset
        self._data_attributes = dict()

        with h5py.File(self.file_path, "r") as infile:
            input_dataset = infile[self.dataset_path]
            self._data_attributes = {
                "shape": input_dataset.shape,
                "dtype": input_dataset.dtype,
                "storage_size": input_dataset.id.get_storage_size(),
            }

    @property
    def dataset_path(self) -> str:
        """
        Absolute path to of the dataset containing
        the data in the hdf5 file (usually named 'data')
        """
        if "/" in self.dataset_name:
            # if the dataset name contains a path, we return it directly
            data_path = self.dataset_name
        else:
            data_path = self.find_dataset(h5_obj=None, dataset_name=self.dataset_name)

        # if the dataset path is empty, we raise an error
        if data_path:
            if not data_path.startswith("/"):
                data_path = "/" + data_path
        else:
            data_path = ""

        logging.debug(f"DATA PATH {data_path}")

        return data_path

    # TODO: add more checks to these properties
    @property
    def shape(self):
        return self._data_attributes["shape"]

    @property
    def dtype(self):
        return self._data_attributes["dtype"]

    @property
    def nrows(self):
        return self.shape[0]

    @property
    def chunk_size(self):
        """
        In case there are less rows than the chunk size, then we set
        the chunk size equal to the number of rows
        """
        if self._chunk_size > self.nrows:
            return self.nrows
        elif self._chunk_size <= 0:
            logging.warning(
                f"Chunk size must be a positive integer. Set to {DEFAULT_CHUNK_SIZE}"
            )
            return DEFAULT_CHUNK_SIZE

        return self._chunk_size

    @property
    def storage_size(self) -> int:
        """
        Returns the size of the dataset in bytes
        """
        return self._data_attributes["storage_size"]

    def check_integrity(self) -> bool:
        """
        Check that the data path inside the HDF5 exists
        """
        errormsg = (
            "Unable to find the required dataset '"
            + self.dataset_name
            + "' anywhere in the input hdf5 file."
        )

        if not check_existence(self.file_path):
            raise FileNotFoundError(f"Input HDF5 file {self.file_path} not found!")

        # In case the recursive search for the dataset path fails (returns group name)
        if self.dataset_name not in self.dataset_path:
            logging.error(errormsg)
            return False

        if self.dataset_path:
            with h5py.File(self.file_path, "r") as h5_master:
                try:
                    # checking the existence of the dataset
                    _ = h5_master[self.dataset_path]

                except KeyError:
                    logging.error(errormsg)

                else:
                    return True
        else:
            logging.error(errormsg)

        return False

    def __iter__(self):
        """Returns a generator that allows iterating data in chunks"""

        with h5py.File(self.file_path, "r") as infile:
            # Get the input dataset
            input_dataset = infile[self.dataset_path]

            # Yields data in chunks
            for i in range(0, self.nrows, self.chunk_size):
                # Calculate the slice for this chunk
                # the min function serves when we reach the end of nrows
                chunk_slice = slice(i, min(i + self.chunk_size, self.nrows))

                # Read the chunk from the input dataset
                data_chunk = input_dataset[chunk_slice]

                # Perform any processing on the data_chunk here if needed
                # Example: data_chunk = np.sqrt(data_chunk)

                yield chunk_slice, data_chunk

    def find_dataset(self, h5_obj=None, dataset_name=None) -> str:
        """
        Reads an hdf5 file object in a recursive way until it finds the dataset name
        """
        # spaces to add in front of group or dataset names

        if h5_obj is None:
            # this is the file handle we manipulate recursively
            h5_obj = h5py.File(self.file_path, "r")

        if dataset_name is None:
            dataset_name = self.dataset_name

        for field_name, field_ref in h5_obj.items():
            if isinstance(field_ref, h5py.Group):
                # go into the group (folder) to continue searching

                return (
                    "/"
                    + field_name
                    + self.find_dataset(h5_obj=field_ref, dataset_name=dataset_name)
                )

            elif isinstance(field_ref, h5py.Dataset):
                if field_name.lower() == dataset_name.lower():
                    # We found where the data is
                    return "/" + field_name

        # closing the file handle
        try:
            logging.debug(f"Closing {h5_obj}")
            h5_obj.close()
        except Exception as e:
            logging.debug(f"HDF5 file {h5_obj} already closed")
            logging.debug(e)

        return ""

    def read_h5_comp_param(self):
        """
        Determines how a hdf5 dataset has been compressed
        to develop later
        """
        with h5py.File(self.file_path) as f:
            data_obj = f[self.dataset_path]
            plist = data_obj.id.get_create_plist()
            logging.debug(f"DIRECT H5PY COMPRESSION: {data_obj.compression}")

            # Another way of retrieving filter info
            filter2 = data_obj._filters
            logging.debug(f"FILTER2 {filter2}")

            try:
                nfilters = plist.get_nfilters()
                logging.debug(f"Number of filters: {nfilters}")

            except AttributeError:
                logging.warning(f"No compression filters found in {self.file_path}")
                return ""

            # Retrieve and interpret filter information
            for i in range(nfilters):
                filter_info = plist.get_filter(i)
                filter_id = filter_info[0]
                parameters = filter_info[2]
                description = filter_info[3].decode()
                filter_description = Hdf5Dataset.interpret_filter_parameters(
                    filter_id, parameters
                )
                logging.debug(
                    f"Filter {i}: ID={filter_id}, Flags={filter_info[1]}, Parameters={parameters}, Description={description}"
                )
                return filter_description

    @staticmethod
    def interpret_filter_parameters(filter_id, parameters) -> str:
        """
        Uses the H5py low level API to get info about which filter and codec was used
        For HDF5 filter doc see https://docs.hdfgroup.org/hdf5/v1_14/_f_i_l_t_e_r.html
        Note: hdf5plugin provides a mapping "name -> filter id in the dict hdf5plugin.FILTERS"
        """
        filter_names = {
            1: "GZIP (DEFLATE)",
            2: "SHUFFLE",
            3: "FLETCHER32",
            4: "SZIP",
            5: "NBIT",
            6: "SCALEOFFSET",
        }

        # HDF5plugin codes
        # {'bshuf': 32008, 'blosc': 32001, 'blosc2': 32026, 'bzip2': 307,
        # 'fcidecomp': 32018, 'lz4': 32004, 'sz': 32017, 'sz3': 32024, 'zfp': 32013, 'zstd': 32015}

        hdf5_plugin_dict = {v: k for k, v in hdf5plugin.FILTERS.items()}
        filter_names.update(hdf5_plugin_dict)
        # logging.debug(filter_names)

        if filter_id == 32008:  # ID for bitshuffle
            # According to bitshuffle's documentation
            if len(parameters) > 4 and parameters[4] == 2:
                return "bslz4"
            else:
                return "Bitshuffle with unknown or no compression"
        else:
            return filter_names.get(filter_id, f"Unknown filter: code {filter_id}")

        # Here we have to search documentation in order to know how to
        # interpret these output id
