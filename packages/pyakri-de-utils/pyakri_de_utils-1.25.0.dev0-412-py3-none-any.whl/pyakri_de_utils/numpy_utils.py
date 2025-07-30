import os
from pathlib import Path
from typing import List

import numpy as np
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import get_dest_file_path
from pyakri_de_utils.file_utils import get_input_files_dir


def save_as_npy_file(np_data, files: List[Path], src_dir, dest_dir):
    for i in range(0, len(files)):
        outfile = str(
            get_dest_file_path(
                file_path=files[i], src_dir=src_dir, dst_dir=dest_dir, extn=".npy"
            )
        )

        outfile_dir = os.path.dirname(outfile)
        create_directory(outfile_dir)

        np.save(outfile, np_data[i])


def get_mem_mapped_np_array(src_dir, temp_fp):
    flist = get_input_files_dir(src_dir, filter_extensions=[".csv"])
    if len(flist) == 0:
        raise ValueError("No input files")

    np0 = np.load(str(flist[0]))
    shape = tuple([len(flist)] + list(np0.shape))
    arr = np.memmap(filename=temp_fp, dtype=np0.dtype, mode="w+", shape=shape)
    arr[0] = np0
    for i in range(1, len(flist)):
        arr[i] = np.load(str(flist[i]))
    return arr


def get_bytes_from_img(file):
    # Read file in binary mode and interpret as unsigned bytes('B')
    with open(file, "rb") as img:
        return np.fromfile(img, np.dtype("B")).tobytes()


def get_flattened_np_array(file):
    return np.load(file).ravel()
