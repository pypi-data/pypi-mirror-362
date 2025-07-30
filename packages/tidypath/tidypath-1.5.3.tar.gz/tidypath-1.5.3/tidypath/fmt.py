"""
Encode dictionaries in strings and decode them. Useful for automatically asigning filenames.
Includes hashing.
"""
import numpy as np
import math
import os
import hashlib

##############################################################################################################################
"""                                                  I. Getopt utils                                                       """
##############################################################################################################################

def encoder(x, ndigits=2, iterables=(list, tuple, np.ndarray), iterable_maxsize=3):
    """x -> string version of x"""
    if isinstance(x, float):
        if math.isinf(x) or math.isnan(x):
            return str(x)
        elif x == int(x):
            return str(int(x))
        else:
            return str(round(x, ndigits=ndigits)).replace('.', '--')
    elif isinstance(x, int):
        return str(x)
    elif callable(x) and hasattr(x, "__name__"):
        return x.__name__
    elif isinstance(x, dict):
        if len(x) >= iterable_maxsize:
            return "{}-values".format(str(len(x)))
        else:
            return dict_to_id(x, ndigits=ndigits, join_char="-", iterable_maxsize=iterable_maxsize)
    elif isinstance(x, iterables):
        if len(x) >= iterable_maxsize:
            return "{}-values".format(str(len(x)))
        else:
            return '-'.join([encoder(sub_x) for sub_x in x])
    else:
        return str(x)

def decoder(x, iterables=(list, tuple, np.ndarray)):
    """string version of x -> x"""
    if isinstance(x, str):
        if x.lower() == "none":
            return None
        elif x.lower() == "false":
            return False
        elif x.lower() == "true":
            return True
        elif "--" in x:
            return float(x.replace("--", "."))
        elif "." in x:
            try:
                return float(x)
            except:
                return x
        else:
            try:
                return int(x)
            except:
                return x
    elif isinstance(x, iterables):
        return [decoder(sub_x) for sub_x in x]
    else:
        try: # check if x is an integer
            x_int = int(x)
            if x_int == x:
                return x_int
            else:
                return x
        except:
            return x

def getopt_printer(opts):
    """Prints getopt input in a readable way."""
    print('\n'.join(f'{opt} => {arg}' for opt, arg in (("Args", "Values"), *opts)))

def dict_to_id(*args, ndigits=2, join_char="_", iterable_maxsize=3, **kwargs):
    """Generate ID of the form k1-v1_k2-v2... for k_i, v_i keys and values of the dictionary d or the kwargs."""
    key_formatter = lambda k: k.replace("_", "-")
    d = args[0] if len(args) > 0 else kwargs
    return join_char.join([f"{key_formatter(k)}-{encoder(d[k], ndigits=ndigits, iterable_maxsize=iterable_maxsize)}" for k in sorted(d.keys())])

def id_to_dict(identifier):
    """Inverse of dict_to_id."""
    s = identifier.split("/")[-1] # retain filename only
    s = os.path.splitext(s)[0] # remove extension
    d = {}
    for split in s.split("_"):
        var_value = split.split("-")
        if len(var_value) > 1:
            if "" in var_value: # value is a float
                var_value_arr = np.array(var_value)
                idx_dot = np.argwhere(var_value_arr == "")[0, 0]
                key_idx = 0 if idx_dot == 2 else slice(0, idx_dot-2)
                d["-".join(var_value[key_idx])] = decoder(f"{var_value_arr[idx_dot-1]}--{var_value_arr[idx_dot+1]}")
            else:
                d["-".join(var_value[:-1])] = decoder(var_value[-1])
    return d

def id_updater(filename, update_dict, mode="add"):
    """
    Modifies filename by updating the underlying dict.
    Attrs:
        - filename:    id to be modified
        - update_dict: dict to use for updating the id. if update_dict={} => filename rearranged according to other_utils.dict_to_id.
        - mode:        - "add":    add update_dict to the id.
                       - "delete": delete update_dict from the id.
    Returns modified filename.
    """
    split_dirs = filename.split("/")
    parentDir = "/".join(split_dirs[:-1])
    file = split_dirs[-1]
    d = id_to_dict(file)
    if mode == "add":
        d.update(update_dict)
    elif mode == "delete":
        d = {k: v for k, v in d.items() if k not in update_dict.keys()}
    var_values = [part.split("-") for part in file.split("_")]
    init = "_".join([part[0] for part in var_values if len(part) == 1])
    ext = os.path.splitext(file)[1]
    new_filename = os.path.join(parentDir, f"{init}_{dict_to_id(d)}{ext}")

    return new_filename

def id_renamer(update_dict, parentDir, key=None, mode="add"):
    """
    Modifies id of files in parentDir by updating the underlying dict.
    Attrs:
        - update_dict: dict to use for updating the id
        - parentDir: folder where files are located.
        - key: string contained in the file for it to be modified.
        - mode:   - "add": add update_dict to the id.
                  - "delete": delete update_dict from the id.
    Returns #modified files.
    NOTE: If update_dict={} => filenames will be rearranged according to other_utils.dict_to_id.
    """
    r = 0
    for file in os.listdir(parentDir):
        if key is None or key in file:
            old_filename = os.path.join(parentDir, file)
            new_filename = id_updater(old_filename, update_dict, mode=mode)
            os.rename(old_filename, new_filename)
            r += 1
    return r


##############################################################################################################################
"""                                                     II. Other.                                                         """
##############################################################################################################################

def hash_file(filename, blocksize=65536):
    """
    Returns the SHA256 hash of the file.
    Autogenerated by copilot. Do not trust it.
    """
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()

def hash_string(s):
    """
    Returns the SHA256 hash of the string.
    """
    return hashlib.sha256(s.encode('utf-8')).hexdigest()
