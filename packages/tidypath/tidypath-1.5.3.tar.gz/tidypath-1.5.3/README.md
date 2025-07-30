# Tidypath

For people that have to compute and store a large variety of data and/or figures.
Check the [tidypath and PhD-utils slides](https://github.com/medinajorge/tidypath/blob/master/tidypath_and_phdu.odp) for an overview.

## Keep your files tidy!

Don't spend time creating directories, deciding filenames, saving, loading, etc. Decorators `savefig` & `savedata` will do it for you.

- `savedata` computes output and stores it in the first function call. Future calls reads it from memory. Default LZMA compression
- `savefig`  saves output figure.

Although recommended, it is not needed to start a new project using `tidypath`. You can continue using your previous code and apply `tidypath` on new code.

### savedata
Example function `slow_computation` in module `package.subpackages.module`
```
@savedata("x+z")
def slow_computation(x, y, *args, z=1, **kwargs):
    ...
    return result
```
1. Apply to function (result of any type).
2. Choose the variables to record in the filenames.
3. Optionally, choose file extension and other specifications. Supported: `lzma` (default), `bz2`, `npz`, `csv`, `JSON`.
4. Result will be saved at `data/subpackages/module/slow_computation/x-'x'_z-'z'_.lzma` ('x' = value of x passed to `slow_computation` during call)
5. If you want to recompute and overwrite, you can pass `overwrite=True` to `slow_computation`. The decorator adds the arguments: `save`, `overwrite`, `keys` and `funcname_in_filename`.

### savefig
```
@savefig("kwargs")
def plot_results(*args, **kwargs):
    ...
    return figure
```
- Same steps as  `savedata`. Only difference is the output type.
- Supports `matplotlib` and `plotly` and all figure extensions (`png`, `eps`, ...) including `html` (`plotly`).
- Decorator adds the same arguments as `savedata` plus `return_fig` (`bool`).

### Adaptable to code modifications
Caching data depends on the specific variables set to store, since they define the filenames. Suppose we want to add a new variable `method` indicating a new method for computing the results, but already computed results are still useful. We can

1. Modify the variables to record in the `savedata` decorator:

        @savedata("x+z")     =>    @savedata("x+z+method")

2. Assign `method='original'` to all existing pre-computed files:

        add_arg(slow_computation, method='original')

3. Now access is granted for the already computed data, and data corresponding to new methods will be stored in separate files.

Use the functions `add_arg`, `modify_arg`, `delete_arg` to ensure cached data is loaded after modifying function arguments.

## Example
- [tidypath and PhD-utils slides](https://github.com/medinajorge/PhD-utils/blob/master/tidypath_and_phdu.odp): instructions and use cases.
- [Defining functions](https://github.com/medinajorge/tidypath/blob/master/tests/analysis/variable1/measurement1.py)
- [Calling functions & modifying args](https://github.com/medinajorge/tidypath/blob/master/tests/Example.ipynb)

## Docs
[Github pages](https://medinajorge.github.io/tidypath/)

## Install
    pip install tidypath
