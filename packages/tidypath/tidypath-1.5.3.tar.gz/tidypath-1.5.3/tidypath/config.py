"""
Config specs for the decorators 'savedata', 'savefig'.

To modify the default config, set the following environmental variables before importing tidypath:

- TIDYPATH_KEYS_DEFAULT
- TIDYPATH_KEYS_DEFAULT_DATA
- TIDYPATH_KEYS_DEFAULT_FIG
- TIDYPATH_KEYS_ADD_POSONLY_TO_ALL
- TIDYPATH_EXT_DEFAULT_DATA
- TIDYPATH_EXT_DEFAULT_FIG
- TIDYPATH_FUNCNAME_IN_FILENAME_DEFAULT_DATA
- TIDYPATH_FUNCNAME_IN_FILENAME_DEFAULT_FIG
- TIDYPATH_RETURN_FIG_DEFAULT
"""

import os
import warnings

# YAML needed to use file based Numba config
try:
    import yaml
    _HAVE_YAML = True
except ImportError:
    _HAVE_YAML = False

# this is the name of the user supplied configuration file
_config_fname = '.tidypath_config.yaml'

class _EnvReloader(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.old_environ = {}
        self.update(force=True)

    def update(self, force=False):
        new_environ = {}

        # first check if there's a .phdu_config.yaml and use values from that
        if os.path.exists(_config_fname) and os.path.isfile(_config_fname):
            if not _HAVE_YAML:
                msg = ("A tidypath config file is found but YAML parsing "
                       "capabilities appear to be missing. "
                       "To use this feature please install `pyyaml`. e.g. "
                       "`conda install pyyaml`.")
                warnings.warn(msg)
            else:
                with open(_config_fname, 'rt') as f:
                    y_conf = yaml.safe_load(f)
                if y_conf is not None:
                    for k, v in y_conf.items():
                        new_environ['TIDYPATH_' + k.upper()] = v

        # clobber file based config with any locally defined env vars
        for name, value in os.environ.items():
            if name.startswith('TIDYPATH_'):
                new_environ[name] = value
        # We update the config variables if at least one PDHU environment
        # variable was modified.  This lets the user modify values
        # directly in the config module without having them when
        # reload_config() is called by the compiler.
        if force or self.old_environ != new_environ:
            self.process_environ(new_environ)
            # Store a copy
            self.old_environ = dict(new_environ)

    def process_environ(self, environ):
        def _readenv(name, ctor, default):
            """
            Attrs:
                    - name:    name of the environment variable
                    - ctor:    constructor for the value of the env var. Takes a value v1 of type t1 and returns a value v2 of type t2.
                    - default: default value for the env var.
            """
            value = environ.get(name)
            if value is None:
                return default() if callable(default) else default
            try:
                return ctor(value)
            except Exception:
                warnings.warn("environ %s defined but failed to parse '%s'" %
                              (name, value), RuntimeWarning)
                return default

        def optional_str(x):
            """
            Examples:
                        ENV_VAR = _readenv(TIDYPATH_ENV_VAR, optional_str, None)
                        ENV_VAR = _readenv(TIDYPATH_ENV_VAR, optional_str,
                                           (val if condition
                                            else None))
            """
            return str(x) if x is not None else None

        def to_bool(x):
            if isinstance(x, str):
                if x.lower() in ["true", "t", "y", "yes"]:
                    return True
                elif x.lower() in ["false", "f", "n", "no"]:
                    return False
                else:
                    raise ValueError(f"x:str must be one of ['true', 'false', yes', no'] and the corresponding 1 character equivalents. Received {x}")
            elif isinstance(x, int):
                if x > 1:
                    raise ValueError(f"x:int must be 0 or 1. Received {x}")
                return x == 1
            else:
                raise TypeError("x must be of type 'str' or 'int'. Received {}".format(type(x)))

        KEYS_DEFAULT = _readenv("TIDYPATH_KEYS_DEFAULT", str, "kwargs_full")
        KEYS_DEFAULT_DATA = _readenv("TIDYPATH_KEYS_DEFAULT_DATA", str, KEYS_DEFAULT)
        KEYS_DEFAULT_FIG = _readenv("TIDYPATH_KEYS_DEFAULT_FIG", str, KEYS_DEFAULT)
        KEYS_ADD_POSONLY_TO_ALL = _readenv("TIDYPATH_KEYS_ADD_POSONLY_TO_ALL", to_bool, False)

        EXT_DEFAULT_DATA = _readenv("TIDYPATH_EXT_DEFAULT_DATA", str, "lzma")
        EXT_DEFAULT_FIG = _readenv("TIDYPATH_EXT_DEFAULT_FIG", str, "pdf")

        FUNCNAME_IN_FILENAME_DEFAULT_DATA = _readenv("TIDYPATH_FUNCNAME_IN_FILENAME_DEFAULT_DATA", to_bool, False)
        FUNCNAME_IN_FILENAME_DEFAULT_FIG = _readenv("TIDYPATH_FUNCNAME_IN_FILENAME_DEFAULT_FIG", to_bool, True)

        RETURN_FIG_DEFAULT = _readenv("TIDYPATH_RETURN_FIG_DEFAULT", to_bool, False)

        # Inject the configuration values into the module globals
        for name, value in locals().copy().items():
            if name.isupper():
                globals()[name] = value

_env_reloader = _EnvReloader()


def reload_config():
    """
    Reload the configuration from environment variables, if necessary.
    """
    _env_reloader.update()
