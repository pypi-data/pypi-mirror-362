"""
Main program for compressing a given dataset inside a HDF5 file using BLOSC2-GROK
Author: Nicolas Soler (SDM section), ALBA synchrotron, 2025
"""

import argparse
from tomocompress.compressor import Blosc2GrokCompressor
from tomocompress.constants import DEFAULT_CR, DEFAULT_CHUNK_SIZE


def main():
    """
    Main function to handle command line arguments and call the compressor.
    """

    # Parsing input options
    PARSER = argparse.ArgumentParser(
        prog="Tomocompress",
        description="A wrapper for Blosc2 Grok lossy compressor",
        epilog="2024 - Nicolas Soler - Alba Synchrotron",
    )

    PARSER.add_argument(
        "hdf5_file", help="hdf5 input file (ideally NeXus)"
    )  # positional argument
    PARSER.add_argument(
        "-d",
        "--dataset_names",
        help="Names of the datasets to compress inside the input hdf5 file, comma-separated (default: 'data')",
        type=str,
        default="data",
    )
    PARSER.add_argument(
        "-c",
        "--cratio",
        type=int,
        default=DEFAULT_CR,
        help=f"compression ratio (default: {DEFAULT_CR})",
    )
    PARSER.add_argument(
        "-o",
        "--output_file_path",
        type=str,
        default="",
        help="Absolute path to output_file (either a directory path or full file name). If not provided, the output file will be created in the same directory as the input file with a suffix added to the original file name.",
    )

    ARGS = PARSER.parse_args()

    # --------------------------------------------
    # Calling the compressor
    print(
        f"Compressing using JPEG2K GROK {ARGS.cratio}X: dataset {ARGS.dataset_names} of file {ARGS.hdf5_file}. Please wait...\n"
    )
    grok_compressor = Blosc2GrokCompressor(
        input_hdf5=ARGS.hdf5_file if ARGS.hdf5_file else "",
        compression_ratio=ARGS.cratio if ARGS.cratio > 1 else DEFAULT_CR,
        dataset_names=ARGS.dataset_names if ARGS.dataset_names else "data",
        chunk_size=DEFAULT_CHUNK_SIZE,
        output_file_path=ARGS.output_file_path if ARGS.output_file_path else "",
    )
    grok_compressor.compress()


# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()
