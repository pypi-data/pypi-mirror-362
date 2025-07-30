"""
Handle data (store/move/delete/load...)
"""

import numpy as np
import pandas as pd
import os
from copy import deepcopy
from pathlib import Path
import time
import datetime
from typing import List, Optional, Tuple
import pickle
import bz2
import lzma
import json
import zipfile

parent_dir =  'data'


##############################################################################################################################
"""                                                       I. Save                                                          """
##############################################################################################################################

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def save_preprocess(filename, saving_type, parent_dir):
    """Creates parent dir if does not exist and ensures filename has the saving_type extension."""
    _parent_dir, _filename = os.path.split(filename)
    if _parent_dir:  # directory specified in filename
        parent_dir = _parent_dir
        filename = _filename
    Path(parent_dir).mkdir(parents=True, exist_ok=True)
    filename = filename if filename.endswith('.{}'.format(saving_type)) else '{}.{}'.format(filename, saving_type)
    return parent_dir, filename

def create_saving_func(file_opener, file_writer, saving_type, **kwargs):
    def saving_func(data, filename, parent_dir=parent_dir):
        """Can specify directory in filename or in parent_dir."""
        parent_dir, filename = save_preprocess(filename, saving_type, parent_dir)
        with file_opener(os.path.join(parent_dir, filename), 'w') as f:
            file_writer(data, f, **kwargs)
        return
    return saving_func

save_json = create_saving_func(open, json.dump, 'json', cls=NpEncoder)
save_bz2 = create_saving_func(bz2.BZ2File, pickle.dump, 'pbz2')
save_lzma = create_saving_func(lzma.LZMAFile, pickle.dump, 'lzma')

def save_npz(arr, filename, parent_dir=parent_dir, key="arr"):
    np.savez_compressed(os.path.join(parent_dir, filename), **{key:arr})
    return

def save_csv(data, filename, parent_dir=parent_dir, **kwargs):
    """
    If data is a numpy array => if 2D => data
                                   1D => [data]
    (required by np.savetxt)
    """
    parent_dir, filename = save_preprocess(filename, "csv", parent_dir)
    file_path = os.path.join(parent_dir, filename)
    if isinstance(data, (pd.core.frame.DataFrame, pd.core.series.Series)):
        data.to_csv(file_path, **kwargs)
    else:
        np.savetxt(file_path, data, delimiter=',', **kwargs)
    return


##############################################################################################################################
"""                                                       II. Load                                                         """
##############################################################################################################################

def create_loading_func(file_opener, file_loader, extra_processing=None, apply_defaults=None):
    """
    - extra_processing = List of process that could be applied to the file.
    - apply_defaults = dict:{str: bool}. The key is set as a function variable, the value indicates whether to apply the process named by the key.
    """
    if extra_processing is None:
        def loading_func(path):
            with file_opener(path, 'rb') as f:
                return file_loader(f)
    else:
        def loading_func(path):
            args = {key:val for key,val in locals().items() if key not in  ('path', *create_loading_func.__code__.co_varnames)}
            with file_opener(path, 'rb') as f:
                data = file_loader(f)

            for condition, process in zip(args.values(), extra_processing):
                if condition:
                    data = process(data)
            return data

        # I know this sould not be done this way, but I wanted to check it can
        code_data = loading_func.__code__
        num_vars = code_data.co_argcount
        num_vars_new = len(apply_defaults)
        new_code = code_data.replace(co_varnames=(*code_data.co_varnames[:num_vars], *apply_defaults.keys(), *code_data.co_varnames[num_vars:]),
                                     co_argcount=num_vars + num_vars_new,
                                     co_nlocals=code_data.co_nlocals + num_vars_new)
        loading_func.__code__ = new_code
        loading_func.__defaults__ = tuple(apply_defaults.values())
    return loading_func

def int_keys(dictionary):
     return {int(key):val for key,val in dictionary.items()}

load_json = create_loading_func(open, json.load, extra_processing=[int_keys], apply_defaults={'int_keys':True})
load_bz2 = create_loading_func(bz2.BZ2File, pickle.load)
load_lzma = create_loading_func(lzma.LZMAFile, pickle.load)

def load_npz(path, key=None):
    data = np.load(path)
    key = [*data.keys()][0] if key is None else key
    return data[key]

def load_csv(path, mode="pandas", **kwargs):
    if mode == "pandas":
        return pd.read_csv(path, **kwargs)
    elif mode == "numpy":
        return np.loadtxt(path, delimiter=",", **kwargs)
    else:
        raise ValueError(f"mode {mode} not valid. Available: 'panda', 'numpy'.")


##############################################################################################################################
"""                                                   III. Compression                                                     """
##############################################################################################################################

def compress_files(rootDir=parent_dir, extension='.json', compress_to='lzma', min_size=0, loading_key=None):
    """
    Searches in a directory and all its subdirectories files with a certain extension and compresses them.

    Attributes:
    - rootDir: The root directory.
    - extension: Extension setting which files should be compressed. Available options: '.json', '.npz'.
    - compress_to: File type after compression. Available options: 'lzma', 'bz2' (or pbz2).
    - min_size: Minimum size for applying compression (in MB).
    - loading_key: Key for retrieving the data in a npz file. If None, retrieves the data corresponding to the first key.

    Returns: Dict containing the name of the files that could not be processed ('bad compression') or those that were corrupted and had to be deleted('deleted files').
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell': # script being run in Jupyter notebook
            from tqdm.notebook import tqdm
        elif shell == 'TerminalInteractiveShell': #script being run in iPython terminal
            from tqdm import tqdm
    except NameError:
            from tqdm import tqdm # Probably runing on standard python terminal.

    # Get all the paths with the desired extension and minimum size.
    files = []

    for dirpath, subdirList, fileList in os.walk(rootDir):
        files += [os.path.join(dirpath, file) for file in fileList if os.path.splitext(file)[1] == extension]

    if min_size > 0:
        files = [file for file in files if os.path.getsize(file) > min_size*1e6]

    # Load files, compress, save and delete if compressed_file == pre_compressed_file
    if extension == '.json':
        loader = load_json
    elif extension == '.npz':
        loader = load_npz
    else:
        raise ValueError("extension = '{}' not valid. Available options: '.json', '.npz'".format(extension))

    if compress_to == 'lzma':
        compressor = save_lzma
        load_compressor = load_lzma
    elif compress_to == 'bz2':
        compressor = save_bz2
        load_compressor = load_bz2
    else:
        raise ValueError("compress_to = '{}' not valid. Available options: 'lzma', 'bz2'".format(extension))

    not_correctly_processed = {'bad_compression': []}
    pbar = tqdm(range(len(files)))

    if extension == '.json':
        for file in files:
            try:
                pre_compressed = loader(file, int_keys=True)
            except ValueError:
                pre_compressed = loader(file, int_keys=False)

            new_filename = '{}.{}'.format(os.path.splitext(file)[0], compress_to)
            compressor(pre_compressed, new_filename, parent_dir="")
            compressed_file = load_compressor(new_filename)

            if compressed_file == pre_compressed:
                os.remove(file)
            else:
                not_correctly_processed['bad_compression'].append(file)

            pbar.refresh()
            print(pbar.update())

    if extension == '.npz':
        not_correctly_processed['deleted_files'] = []
        for file in files:
            try:
                pre_compressed = loader(file, key=loading_key)
            except zipfile.BadZipFile: # corrupted file
                os.remove(file)
                not_correctly_processed['deleted_files'].append(file)
                continue

            new_filename = '{}.{}'.format(os.path.splitext(file)[0], compress_to)
            compressor(pre_compressed, new_filename, parent_dir="")
            compressed_file = load_compressor(new_filename)

            if np.all(compressed_file == pre_compressed):
                os.remove(file)
            else:
                not_correctly_processed['bad_compression'].append(file)
            pbar.refresh()
            print(pbar.update())

    return not_correctly_processed


##############################################################################################################################
"""                                                   IV. Deletion                                                         """
##############################################################################################################################
def _delete_files_newer_than(
    directory: str,
    dry_run: bool = True,
    t: float = 1.0,
    time_unit: str = 'd',
    recursive: bool = False,
    file_extensions: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    verbose: bool = True
) -> Tuple[List[str], List[str]]:
    """
    Delete files in a directory that are newer than time [time_unit].

    Args:
        directory (str): Path to the directory to process
        dry_run (bool): If True, only simulate deletion (safer default)
        t (float): Time in seconds (default: 1 day)
        time_unit (str): Time unit (default: 'd'). Example ['s', 'm', 'h', 'd', 'w']
        recursive (bool): If True, process subdirectories recursively
        file_extensions (List[str], optional): Only process files with these extensions
            Example: ['.txt', '.csv', '.log']
        exclude_patterns (List[str], optional): Skip files containing these patterns
            Example: ['backup', 'important', 'keep']
        verbose (bool): If True, print detailed information

    Returns:
        Tuple[List[str], List[str]]: (successfully_processed, failed_files)

    Raises:
        ValueError: If directory doesn't exist or is not a directory
        PermissionError: If insufficient permissions to access directory
    """

    # Input validation
    if not directory or not isinstance(directory, str):
        raise ValueError("Directory must be a non-empty string")

    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")

    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")

    # Calculate cutoff time (7 days ago)
    time_unit_mpl = dict(s=1, m=60, h=3600, d=3600*24, w=3600*24*7)
    dt = t * time_unit_mpl[time_unit]
    past_time = time.time() - dt
    cutoff_datetime = datetime.datetime.fromtimestamp(past_time)

    time_threshold = f'{t} [{time_unit}]'

    if verbose:
        print(f"{'=' * 60}")
        print(f"Directory: {directory}")
        print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL DELETION'}")
        print(f"Recursive: {recursive}")
        print(f"Cutoff time: {cutoff_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"File extensions filter: {file_extensions}")
        print(f"Exclude patterns: {exclude_patterns}")
        print(f"{'=' * 60}")

    successfully_processed = []
    failed_files = []

    def should_process_file(file_path: Path) -> bool:
        """Check if file should be processed based on filters"""

        # Check file extension filter
        if file_extensions:
            if file_path.suffix.lower() not in [ext.lower() for ext in file_extensions]:
                return False

        # Check exclude patterns
        if exclude_patterns:
            file_name = file_path.name.lower()
            for pattern in exclude_patterns:
                if pattern.lower() in file_name:
                    if verbose:
                        print(f"  SKIPPED (excluded pattern): {file_path}")
                    return False

        return True

    def process_file(file_path: Path) -> bool:
        """Process a single file - check age and delete if newer than threshold"""
        try:
            # Get file modification time
            file_mtime = file_path.stat().st_mtime
            file_datetime = datetime.datetime.fromtimestamp(file_mtime)

            # Check if file is newer than theshold
            if file_mtime > past_time:
                if verbose:
                    print(f"  NEWER THAN {time_threshold}: {file_path}")
                    print(f"    Modified: {file_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

                if not dry_run:
                    file_path.unlink()  # Delete the file
                    if verbose:
                        print(f"    DELETED: {file_path}")
                else:
                    if verbose:
                        print(f"    WOULD DELETE: {file_path}")

                successfully_processed.append(str(file_path))
                return True
            else:
                if verbose:
                    print(f"  OLDER THAN {time_threshold} (keeping): {file_path}")
                    print(f"    Modified: {file_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                return False

        except (OSError, IOError) as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            if verbose:
                print(f"  ERROR: {error_msg}")
            failed_files.append(error_msg)
            return False

    try:
        # Get files to process
        if recursive:
            file_iterator = dir_path.rglob('*')
        else:
            file_iterator = dir_path.iterdir()

        # Process files
        total_files = 0
        processed_files = 0

        for item in file_iterator:
            if item.is_file():
                total_files += 1

                if should_process_file(item):
                    if process_file(item):
                        processed_files += 1

        # Summary
        if verbose:
            print(f"\n{'=' * 60}")
            print(f"SUMMARY:")
            print(f"Total files examined: {total_files}")
            print(f"Files newer than {time_threshold}: {processed_files}")
            print(f"Files {'would be deleted' if dry_run else 'deleted'}: {len(successfully_processed)}")
            print(f"Errors encountered: {len(failed_files)}")
            print(f"{'=' * 60}")

            if failed_files:
                print("\nERRORS:")
                for error in failed_files:
                    print(f"  - {error}")

    except PermissionError as e:
        raise PermissionError(f"Insufficient permissions to access directory: {directory}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error processing directory: {str(e)}") from e

    return successfully_processed, failed_files


def delete_files_newer_than(directory: str, dry_run: bool = True, t: float = 1.0, time_unit='d') -> None:
    """
    Simplified version - just delete files newer than t [time_unit]

    Args:
        directory (str): Path to the directory to process
        dry_run (bool): If True, only simulate deletion (safer default)
        t: float: Time threshold in units of time_unit
        time_unit (str): Unit of time, e.g. 'd' for days
    """
    try:
        processed, failed = _delete_files_newer_than(
            directory=directory,
            dry_run=dry_run,
            t=t,
            time_unit=time_unit,
            verbose=True
        )

        if not dry_run and processed:
            print(f"\nSUCCESS: Deleted {len(processed)} files newer than {time} [{time_unit}]")
        elif dry_run and processed:
            print(f"\nDRY RUN: Would delete {len(processed)} files newer than {time} [{time_unit}]")
        else:
            print(f"\nNo files newer than {time} [{time_unit}] found in {directory}")

    except Exception as e:
        print(f"ERROR: {str(e)}")
