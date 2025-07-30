"""
Main uses: save and cache data, save figures, change figure color, timing.
"""
import math
import inspect
import warnings
import os
from pathlib import Path
from functools import wraps
from collections.abc import Iterable
from importlib.util import find_spec
from ._helper import NoFigure
from lzma import LZMAError
import _lzma
if find_spec("plotly") is None:
    plotly_figure = NoFigure
else:
    from plotly.graph_objs._figure import Figure as plotly_figure
if find_spec("matplotlib") is None:
    mpl_figure = NoFigure
else:
    from matplotlib.figure import Figure as mpl_figure
    import matplotlib.pyplot as plt

from . import storage, config
from .paths import datapath, figpath, hash_path
from .inspection import classify_call_attrs, merge_wrapper_signatures
from ._helper import merge_nested_dict

class SavedataSkippedComputation:
    pass

def _preprocess_keys_or_function(keys_or_function, keys, extra_keys):
    if isinstance(keys_or_function, Iterable):
        func = None
        if isinstance(keys_or_function, dict):
            extra_keys = keys_or_function
        else:
            keys = keys_or_function
    elif callable(keys_or_function):
        func = keys_or_function
    else:
        func = None
    return func, keys, extra_keys


def savedata(keys_or_function=None, include_classes="file",
             ext=config.EXT_DEFAULT_DATA, keys=config.KEYS_DEFAULT_DATA, extra_keys={},
             funcname_in_filename=config.FUNCNAME_IN_FILENAME_DEFAULT_DATA,
             overwrite=False, save=True, load_opts_default_save=True, return_path=False, #defaults for extra arguments
             max_str_length=255,
             skip_computation=False,
             iterable_maxsize=math.inf,
             load_opts={}, **save_opts):
    """
    Decorator for automatically saving output and then loading cached data.
    Default behavior:
        1st function call:   stores the data with extension 'ext'.
        rest:                loads stored data if the key args passed to the function coincide.

    If filename is too long, it is shortened by hashing it.


    NOTE (!) decorated funcs will have extra arguments:
        - save (bool).                 whether to save the output of the function.
        - overwrite (bool).            whether to overwrite the saved version.
        - funcname_in_filename(bool)   whether to include funcname in the filename.
        - keys (dict/str/iterable)    · str:       key of a keyword argument. Example: keys = 'x'.
                                                 "kwargs_defaults"  =>  default kwargs that were not modified.
                                                 "kwargs"           =>  kwargs passed during function call.
                                                 "kwargs_full"      =>  kws_defaults + kws.
                                                 "pos_only"         =>  length of *args
                                                 "args"             =>  attrs != **kwargs, *args.
                                                 "all"              if config.KEYS_ADD_POSONLY_TO_ALL  =>  all attrs
                                                                    else                               =>  all attrs except pos_only: kwargs_full + args
                                                 can combine options using "+" or "-". Example: "args+z", "x+y+kwargs", "all-y".
                                     · iterable: containing a combination of the available string keys (above). ["k1", "k2"] == "k1+k2".
        - extra_keys (dict):         additional keys to be included in the filename. They do not have to be arguments of the function.
        - skip_computation (bool).     whether to skip computation if the data is not stored.
        - ext (str/list/tuple):    storing extension. Selects 'storage' functions save_ext, load_ext.
                                   Supported: 'lzma' (default), 'bz2', 'json', 'csv', 'npz'.
        - return_path (bool).      whether to return the path of the saved data.

    Attrs:
        - function:                function to which the decorator is applied
        - include_classes:         include class tree in saving_path.
        - load_opts:               kws for storage.load_ext. default kws are those of 'saving_options', those specified update saving_options dict.
        - save_opts:               kws for storage.save_ext
        - load_opts_default_save:  use save_opts as default for load_opts.
        - max_str_length:          max length of filename. If exceeded, filename is shortened by hashing it.
        - iterable_maxsize:        max size of iterable keys. If exceeded, keys are shortened by counting val numbers.
        - rest:                    default behavior for decorated funcs extra arguments (above).

    Returns: Function decorator
    """
    func, keys, extra_keys = _preprocess_keys_or_function(keys_or_function, keys, extra_keys)

    if load_opts_default_save:
        load_opts = {**save_opts, **load_opts}

    def _savedata(func):
        @wraps(func)
        def wrapper(*args, overwrite=overwrite, keys=keys, extra_keys=extra_keys, save=save, funcname_in_filename=funcname_in_filename, skip_computation=skip_computation, ext=ext, return_path=return_path, **kwargs):
            key_opts = classify_call_attrs(func, args, kwargs, add_pos_only_to_all=config.KEYS_ADD_POSONLY_TO_ALL)
            save_keys = merge_nested_dict(key_opts, keys, key_default="all")
            if extra_keys:
                save_keys = {**extra_keys, **save_keys}

            def get_saving_path(ext):
                saving_path = datapath(keys=save_keys, func=func, ext=ext, include_classes=include_classes, funcname_in_filename=funcname_in_filename, iterable_maxsize=iterable_maxsize)
                filename = os.path.basename(saving_path)
                if len(filename) + len(ext) + 1 > max_str_length:
                    saving_path = hash_path(saving_path)
                    warnings.warn("Filename too long. Hashing it ...", RuntimeWarning)
                return saving_path

            result = None
            def compute(result, ext, saving_path):
                if result is None:
                    result = func(*args, **kwargs)
                if save:
                    getattr(storage, f"save_{ext}")(result, saving_path, **save_opts)
                return result

            if isinstance(ext, str):
                ext = [ext]

            if return_path:
                return [get_saving_path(ext_i) for ext_i in ext]
            else:
                for ext_i in ext:
                    saving_path = get_saving_path(ext_i)
                    if skip_computation and not Path(saving_path).exists():
                        warnings.warn("Skipping computation. Data not stored.", RuntimeWarning)
                        return SavedataSkippedComputation()
                    elif Path(saving_path).exists() and not overwrite:
                        try:
                            result = getattr(storage, f"load_{ext_i}")(saving_path, **load_opts)
                        except EOFError or LZMAError or _lzma.LZMAError:
                            if skip_computation:
                                warnings.warn("Corrupted file. Skipping computation ...", RuntimeWarning)
                                return SavedataSkippedComputation()
                            else:
                                warnings.warn("Corrupted file. Recomputing and storing ...", RuntimeWarning)
                                result = compute(result, ext_i, saving_path)
                        except KeyboardInterrupt:
                            raise KeyboardInterrupt
                        except Exception as e:
                            print(e)
                            if skip_computation:
                                warnings.warn("Corrupted file. Skipping computation ...", RuntimeWarning)
                                return SavedataSkippedComputation()
                            else:
                                warnings.warn("Corrupted file. Recomputing and storing ...", RuntimeWarning)
                                result = compute(result, ext_i, saving_path)
                    else:
                        result = compute(result, ext_i, saving_path)
                return result

        wrapper.__signature__ = merge_wrapper_signatures(wrapper, ["overwrite", "keys", "save", "funcname_in_filename", "skip_computation", "ext", "return_path"])
        wrapper.__out__ = "data"
        return wrapper

    if func is None:
        return _savedata
    else:
        return _savedata(func)


def savefig(keys_or_function=None, include_classes="file",
            ext=config.EXT_DEFAULT_FIG, keys=config.KEYS_DEFAULT_FIG, extra_keys={},
            funcname_in_filename=config.FUNCNAME_IN_FILENAME_DEFAULT_FIG, return_fig=config.RETURN_FIG_DEFAULT,
            max_str_length=255,
            iterable_maxsize=3,
            overwrite=True, save=True,  #defaults for extra arguments
            **save_opts):
    """
    Generates figsaver decorator.
    Figure returned by function is automatically saved. Compatible with matplotlib and plotly.
    If None or NaN is returned, avoid figure saving.

    If filename is too long, it is shortened by hashing it.

    NOTE (!) decorated funcs will have extra arguments:
        - return_fig (bool)            whether to return the figure (output of function).
        - save (bool).                 whether to save the figure.
        - overwrite (bool).            whether to overwrite the saved version.
        - funcname_in_filename(bool)   whether to include funcname in the filename.
        - keys (dict/str/iterable)   · str:       key of a keyword argument. Example: keys = 'x'.
                                                 "kwargs_defaults"  =>  default kwargs that were not modified.
                                                 "kwargs"           =>  kwargs passed during function call.
                                                 "kwargs_full"      =>  kws_defaults + kws.
                                                 "pos_only"         =>  length of *args. Also self and cls are counted as pos_only arguments.
                                                 "args"             =>  attrs != **kwargs, *args.
                                                 "all"              if config.KEYS_ADD_POSONLY_TO_ALL  =>  all attrs
                                                                    else                               =>  all attrs except pos_only: kwargs_full + args
                                                 can combine options using "+" or "-". Example: "args+z", "x+y+kwargs", "all-y".
                                     · iterable: containing a combination of the available string keys (above). ["k1", "k2"] == "k1+k2".
        - extra_keys (dict):         additional keys to be included in the filename. They do not have to be arguments of the function.
        - ext (str/list/tuple):    Storing extension. 'pdf' recommended for articles.
                                   Supported: any extension supported by matplotlib/plotly. Example: 'png', 'eps', 'html' (plotly), etc.


    Attrs:
        - function:                function to which the decorator is applied
        - include_classes:         include class tree in saving_path.
        - save_opts:               kws for saving function.
        - max_str_length:          max length of filename. If exceeded, filename is shortened by hashing it.
        - iterable_maxsize:        max size of iterable keys. If exceeded, keys are shortened by counting val numbers.
        - rest:                    default behavior for decorated funcs extra arguments (above).

    Returns: Function decorator
    """
    func, keys, extra_keys = _preprocess_keys_or_function(keys_or_function, keys, extra_keys)

    mpl_save_defaults = dict(bbox_inches="tight")

    def _savefig(func):
        @wraps(func)
        def wrapper(*args, overwrite=overwrite, keys=keys, save=save, return_fig=return_fig, funcname_in_filename=funcname_in_filename, ext=ext, **kwargs):
            fig = func(*args, **kwargs)
            is_mpl_axes = type(fig).__name__ == 'AxesSubplot'
            if isinstance(fig, (mpl_figure, plotly_figure)) or is_mpl_axes:
                key_opts = classify_call_attrs(func, args, kwargs, add_pos_only_to_all=config.KEYS_ADD_POSONLY_TO_ALL)
                save_keys = merge_nested_dict(key_opts, keys, key_default="all")
                if extra_keys:
                    save_keys = {**extra_keys, **save_keys}
                def get_saving_path(ext):
                    saving_path = figpath(keys=save_keys, func=func, ext=ext, include_classes=include_classes, funcname_in_filename=funcname_in_filename, iterable_maxsize=iterable_maxsize)
                    filename = os.path.basename(saving_path)
                    if len(filename) + len(ext) + 1 > max_str_length:
                        saving_path = hash_path(saving_path)
                        warnings.warn("Filename too long. Hashing it ...", RuntimeWarning)
                    return saving_path

                if is_mpl_axes:
                    fig = fig.get_figure()
                is_mpl = isinstance(fig, mpl_figure)

                if save:
                    if isinstance(ext, str):
                        ext = [ext]
                    for ext_i in ext:
                        saving_path = get_saving_path(ext_i)
                        if not Path(saving_path).exists() or overwrite:
                            if is_mpl:
                                fig.savefig(saving_path, format=ext_i, **{**mpl_save_defaults, **save_opts})
                            elif isinstance(fig, plotly_figure):
                                if ext_i == "html":
                                    fig.write_html(saving_path, **save_opts)
                                else:
                                    fig.write_image(saving_path, format=ext_i, **save_opts)
                            else:
                                raise TypeError(f"fig type '{type(fig)}' not valid. Available: 'matplotlib.figure.Figure', 'matplotlib.axes._subplots.AxesSubplot', 'plotly.grap_objs._figure.Figure'.")


                if return_fig:
                    return fig
                else:
                    if is_mpl:
                        plt.close(fig)
                    return
            elif fig is None or math.isnan(fig):
                warnings.warn("Expected output figure (plotly or matplotlib) and received None or NaN.", RuntimeWarning)
            else:
                warnings.warn("Expected output figure (plotly, matplotlib) or a flag for figure error computation (None, NaN), but received {}".format(type(fig)), RuntimeWarning)

        wrapper.__signature__ = merge_wrapper_signatures(wrapper, ["overwrite", "keys", "save", "funcname_in_filename", "return_fig", "ext"])
        wrapper.__out__ = "figure"
        return wrapper

    if func is None:
        return _savefig
    else:
        return _savefig(func)
