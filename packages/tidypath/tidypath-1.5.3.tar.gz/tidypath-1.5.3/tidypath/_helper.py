"""
Helper functions
"""
import re

def merge_nested_dict(d, keys, key_default=None):
    """
    Returns the result of merging several keys of a dictionary.
    
    Attrs:
            - d:             nested dictionary
            - keys:          d keys to be merged. can be a string of the form 'k' or 'k1+k2+...', or other iterables containing the keys.
            - key_default:   if a key does not belong to d => it is searched in d[key_default]
    """
    if isinstance(keys, str):
        key_add = set(re.findall(r'(?:^|(?<=\+))(\w+)', keys))
        key_remove = set(re.findall(r'(?<=-)(\w+)', keys))
    else:
        key_add = set(keys)
        key_remove = set()
    
    if not key_add and key_remove:
        key_add = set(["all"])
        
    d_keys = set(d)
    keys_in_d = key_add.intersection(d_keys)
    keys_in_default = key_add - keys_in_d
    
    if not keys_in_default.issubset(set(d[key_default])):
        raise RuntimeError("Some keys don't belong to d or d[key_default]")
    else:    
        d_merged = {}    
        for k in keys_in_d:
            d_merged.update(d[k])
        d_default = d[key_default]
        d_merged.update({k: d_default[k] for k in keys_in_default})
        for k in key_remove:
            if k in d_merged:
                del d_merged[k]
            else:
                for k_i in d[k]:
                    del d_merged[k_i]
        return d_merged

class NoFigure():
    """
    Fill type for plotly/matplotlib figures, if the package is not available.
    Allows tidypath.savefig to work with matplotlib/plotly when the other one is not present.
    """
    pass