"""
Creates paths for automatically organizing files.
Allows filename modification: If arg added (deleted) to func => add (delete) arg to stored function output files.
Hash filename of long paths.

Two schemes:
    1. By module => Module -> submodules -> class tree (until classes in module by default) -> func
    2. By class  => Class organization is a class to be inherited. Sets path: parentDir -> subfolder (optionally specified) -> inheritance_tree -> func_name.
(1) is the most appropiate.
"""
import os
import sys
import inspect
import warnings
import numpy as np
import pandas as pd
import datetime
from copy import deepcopy
from collections.abc import Iterable
from pathlib import Path
from .fmt import dict_to_id, encoder, hash_string
from .inspection import get_class_that_defined_method

dataDir = "data"
figDir = "figs"

def time_since_last_update(parent_dir, ext='lzma'):
    """
    Returns a pandas Series with the time since last update of each file in parent_dir.
    """
    t = {}
    today = datetime.datetime.now()
    for f in os.listdir(parent_dir):
        if ext is None or f.endswith(ext):
            path = os.path.join(parent_dir, f)
            last_update = today - pd.to_datetime(Path(path).stat().st_mtime, unit='s')
            t[path] = last_update
    return pd.Series(t).sort_values()

def hash_path(path):
    """
    Hashes the filename (keeping the extension and parentDir) of a path.
    """
    parentDir = os.path.dirname(path)
    filename = os.path.basename(path)
    filename, ext = os.path.splitext(filename)
    filename = hash_string(filename)
    return os.path.join(parentDir, f"{filename}{ext}")

def class_path(func, include_classes="file", skip=1):
    """
    returns module path and func_name.

    include_classes:   'file': path: module -> class tree contained in func file -> func_name.
                       'all': path: module -> full class tree -> func_name.
    """
    func_name = func.__name__
    module = func.__module__
    if include_classes:
        func_class = get_class_that_defined_method(func)
        if func_class is not None:
            if include_classes == "file":
                clsmembers = inspect.getmembers(sys.modules[module], inspect.isclass)
                cls_names, clss = zip(*clsmembers)
                class_tree = "/".join([c.__name__ for c in func_class.mro()[:-skip][::-1] if c in clss])
            elif include_classes == "all":
                class_tree = "/".join([c.__name__ for c in func.__class__.mro()[:-skip][::-1]])
            else:
                raise ValueError(f"include_classes: {include_classes} not valid. Available: 'file', 'all', ''.")
        else:
            class_tree = ""
    else:
        class_tree = ""
    path = os.path.join(class_tree, func_name)
    return path

def saving_path(Dir, ext, func, keys={}, subfolder="", return_dir=False, funcname_in_filename=False, iterable_maxsize=3, **kwargs):
    """Tree path: Dir -> subfolder -> module -> (classes) -> func_name."""
    func_path = inspect.getabsfile(func).replace('.py', '')
    module_head = func.__module__.split('.')[0]
    if module_head == '__main__':
        parentDir = os.path.join(Dir,
                                 subfolder,
                                 module_head,
                                 class_path(func=func, **kwargs)
                                 )
        warnings.warn(f"Module {module_head} is '__main__'. Saving in {parentDir}.", RuntimeWarning)
    else:
        path_split = func_path.split(module_head + '/')
        parentDir = os.path.join(path_split[0],
                                 Dir,
                                 subfolder,
                                 module_head,
                                 *path_split[1:],
                                 class_path(func=func, **kwargs)
                                 )
    Path(parentDir).mkdir(exist_ok=True, parents=True)
    if return_dir:
        return parentDir
    else:
        if funcname_in_filename:
            filename = parentDir.split("/")[-1] + f"_{dict_to_id(keys, iterable_maxsize=iterable_maxsize)}_.{ext}"
        else:
            filename = f"{dict_to_id(keys, iterable_maxsize=iterable_maxsize)}_.{ext}"
        return os.path.join(parentDir, filename)

def figpath(ext="png", **kwargs):
    return saving_path(figDir, ext, **kwargs)

def datapath(ext="lzma", **kwargs):
    return saving_path(dataDir, ext, **kwargs)

def filename_modifier(process_filename, func_or_directory=None, check_first=True, overwrite=False, **args):
    """
    Base function for adding/deleting/modifying function args encoded in the output filenames.

    Attrs:
        - process_filename:    function f(file, k_name, k, v) -> new_filename.
                               - k, v are the key and value of an arg.
                               - k_name is the string encoding of k. (replace '_' -> '-')
        - func (callable):     function (wrapped by savedata or savefig) for retrieving the corresponding directory where the outputs are stored.
        - directory (str):     directory where files are to be modified. It is recommended to pass the function instead of the directory.
        - check_first (bool):  whether to check the new filenames before applying any changes.
        - overwrite (bool):    whether to overwrite files when in conflict.
                               Examples:   add/modify/delete an arg -> two filenames are the same -> one remains.
        - args (kwargs):       Arguments to add/delete/modify in the filename.
    """
    if callable(func_or_directory):
        func = func_or_directory
        if func.__out__ == "data":
            directory = datapath(func=func.__wrapped__, return_dir=True)
        else:
            directory = figpath(func=func.__wrapped__, return_dir=True)
    elif isinstance(func_or_directory, str):
        directory = func_or_directory
    else:
        raise ValueError(f"func_or_directory {func_or_directory} not valid. Must be a function or a path.")

    args_sorted = {k: args[k] for k in sorted(args)}
    abort_changes = False
    avoid_files = [".ipynb_checkpoints", "__pycache__"]
    for k, v in args_sorted.items():
        check_first_k = deepcopy(check_first)
        print_long_filename_k = deepcopy(check_first)
        if abort_changes:
            break
        else:
            k_name = encoder(k).replace("_", "-")
            for file in os.listdir(directory):
                if file not in avoid_files:
                    new_filename = process_filename(file, k_name, k, v)
                    if new_filename is not None:
                        if len(new_filename) > 255:
                            if print_long_filename_k:
                                new_filename_hashed = hash_path(new_filename)
                                warnings.warn(f"Filename too long for '{file}'. Hashed to '{new_filename_hashed}'. Warning will not be shown again.", RuntimeWarning)
                                print_long_filename_k = False
                                new_filename = new_filename_hashed
                            else:
                                new_filename = hash_path(new_filename)
                        new_path = os.path.join(directory, new_filename)
                        if Path(new_path).exists() and not overwrite:
                            raise RuntimeError(f"'{new_filename}' already existing before modifying '{file}'. To delete repeated files pass 'overwrite=True'.")
                        else:
                            if check_first_k:
                                update_file = 0
                                while update_file not in ["y", "yes", "n", "no"]:
                                    update_file = input("Filename change example:\n\n'{}' -> '{}'\n\nProceed? [y/n]".format(file, new_filename)).lower()
                                check_first_k = False
                            else:
                                update_file = "y"
                            if update_file in ["y", "yes"]:
                                os.rename(os.path.join(directory, file),
                                          new_path)
                            else:
                                warnings.warn("Aborted filename changes.", RuntimeWarning)
                                abort_changes = True
                                break
    return

def add_arg(func_or_directory=None, check_first=True, overwrite=False, **args):
    """
    Encodes new function args into filename.
    Useful when:
        (1) Adding a new arg to a function wrapped by savedata. Allows loading the available data without recomputing.
        (2) Modifying figure names produced by a function.

    Attrs:
        - args (kwargs):       new arguments to encode into filename.
        - func (callable):     function (wrapped by savedata or savefig) for retrieving the corresponding directory where the outputs are stored.
        - directory (str):     directory where files are to be modified. It is recommended to pass the function instead of the directory.
        - check_first (bool):  whether to check the new filenames before applying any changes.
        - overwrite (bool):    whether to overwrite files when in conflict.
                               Example:   add an arg -> two filenames are the same -> one remains.
    """
    def process_filename(file, k_name, k, v):
        arg_val = dict_to_id({k:v})
        new_filename = None
        if arg_val not in file:
            args_in_file = np.sort(os.path.splitext(file)[0].split("_")[:-1] + [k])
            pos_new_arg = np.where(args_in_file == k)[0][0]
            if pos_new_arg == 0:
                new_filename = f"{arg_val}_{file}"
            else:
                if pos_new_arg + 1 == len(args_in_file):
                    insert_before = "."
                else:
                    insert_before = args_in_file[pos_new_arg + 1]
                new_filename = file.replace(f"_{insert_before}", f"_{arg_val}_{insert_before}")
            if new_filename == file:
                new_filename = None

        return new_filename

    filename_modifier(process_filename, func_or_directory=func_or_directory, check_first=check_first, overwrite=overwrite, **args)
    return

def delete_arg(func_or_directory=None, arg=None, check_first=True, overwrite=False):
    """
    Delete encoded function arg from filename.
    Useful when:
        (1) Deleting an arg from a function wrapped by savedata. Allows loading the available data without recomputing.
        (2) Modifying figure names produced by a function.

    Attrs:
        - arg (str or iterable):       key of an arg (k in k=v) to be deleted, or an iterable containing keys.
        - func (callable):             function (wrapped by savedata or savefig) for retrieving the corresponding directory where the outputs are stored.
        - directory (str):             directory where files are to be modified. It is recommended to pass the function instead of the directory.
        - check_first (bool):          whether to check the new filenames before applying any changes.
        - overwrite (bool):            whether to overwrite files when in conflict.
                                       Examples:   Delete an arg -> two filenames are the same -> one remains.
    """
    if isinstance(arg, str):
        arg_dict = {arg: None}
    elif isinstance(arg, Iterable):
        if all(isinstance(a, str) for a in arg):
            arg_dict = {a: None for a in arg}
        else:
            raise ValueError(f"arg {arg} not valid. Must be a string or an iterable of strings.")
    else:
        raise ValueError(f"arg {arg} not valid. Must be a string or an iterable of strings.")

    def process_filename(file, k_name, k, v):
        if file.startswith(f"{k_name}-"):
            return "_".join(file.split("_")[1:])
        else:
            mid_file_k_name = f"_{k_name}-"
            if mid_file_k_name in file:
                arg_val_encoded = "{}{}".format(mid_file_k_name, file.split(mid_file_k_name)[1].split("_")[0])
                return file.replace(arg_val_encoded, "")
            else:
                return None

    filename_modifier(process_filename, func_or_directory=func_or_directory, check_first=check_first, overwrite=overwrite, **arg_dict)
    return

def modify_arg(func_or_directory=None, check_first=True, overwrite=False, **args):
    """
    Modified encoded function arg from filename.
    Useful when:
        (1) Renaming an arg value with a more suitable one (more comprehensible, better defined...), leaving the func output unchanged. Allows loading the available data without recomputing.
        (2) Modifying figure names produced by a function.

    Attrs:
        - args (kwargs):       arguments to modify in the filename.
        - func (callable):     function (wrapped by savedata or savefig) for retrieving the corresponding directory where the outputs are stored.
        - directory (str):     directory where files are to be modified. It is recommended to pass the function instead of the directory.
        - check_first (bool):  whether to check the new filenames before applying any changes.
        - overwrite (bool):    whether to overwrite files when in conflict.
                               Examples:   Modify an arg -> two filenames are the same -> one remains.
    """
    def process_filename(file, k_name, k, v):
        new_filename = None
        if file.startswith(f"{k_name}-"):
            new_filename = "_".join([dict_to_id({k:v})] + file.split("_")[1:])
        else:
            mid_file_k_name = f"_{k_name}-"
            if mid_file_k_name in file:
                arg_val_encoded = "{}{}".format(mid_file_k_name, file.split(mid_file_k_name)[1].split("_")[0])
                new_filename = file.replace(arg_val_encoded, "_{}".format(dict_to_id({k:v})))

        if new_filename == file:
            new_filename = None
        return new_filename

    filename_modifier(process_filename, func_or_directory=func_or_directory, check_first=check_first, overwrite=overwrite, **args)
    return

class Organizer():
    dataDir = dataDir
    figDir = figDir
    subfolder = ""

class ClassPath(Organizer):
    """
    Updates fig and data dir of the class as follows:
    parentDir -> subfolder -> inheritance_tree -> func_name
    """

    @classmethod
    def inheritance_path(cls, skip=2):
        return "/".join([c.__name__.lower() for c in cls.mro()[:-skip][::-1]])

    @classmethod
    def create_dir(cls, dirKey, depth=2):
        """Creates tree: parentDir -> subfolder -> inheritance_tree -> func_name"""
        path = os.path.join(getattr(cls, f"{dirKey}Dir"),
                            cls.subfolder,
                            cls.inheritance_path(),
                            sys._getframe(depth).f_code.co_name
                           )
        Path(path).mkdir(exist_ok=True, parents=True)
        return path

    @classmethod
    def create_figDir(cls):
        return cls.create_dir("fig")

    @classmethod
    def create_dataDir(cls):
        return cls.create_dir("data")
