"""
Analyze variables passed to functions, parent class, merge wrapper and wrapped signatures.
"""
import inspect
import functools

def classify_call_attrs(func, args, kwargs, add_pos_only_to_all=False):
    """
    Classify function args and kwargs passed during function call
    
    NOTE:  Probably could be done more efficiently relying more on inspect.getargspec(func) or inspect.signature(func), but realized later.
    NOTE2: For position-only arguments f(*args), 
           usually referred in the docs as f(pos1, pos2, /, pos_or_kwd,...)  ('/' indicates end of position-only-args),
           only provides the number of *args.
    
    Example: dict()
    
    Returns: dict containing
        "kwargs_defaults"  =>  default kwargs that were not modified.
        "kwargs"           =>  kwargs passed during function call.
        "kwargs_full"      =>  kws_defaults + kws.
        "pos_only"         =>  length of *args (position-only arguments)
        "args"             =>  position-or-keyword arguments (are called static in the code).
        "all"              =>  add_pos_only_to_all == False => all attrs except pos_only: kwargs_full + args
                               else                         => all attrs: kwargs_full + args + pos_only
    """
    code = func.__code__
    num_kwonly = code.co_kwonlyargcount
    if num_kwonly > 0: # func has keyword-only args: f(*args, k1=v1, ..., kn=vn)
        kwonly_defaults = func.__kwdefaults__
    else:
        kwonly_defaults = {}

    num_defaults = 0 if func.__defaults__ is None else len(func.__defaults__) # f(k1=v1,...)
    num_static = code.co_argcount - num_defaults                              # f(k1,k2)
    if num_defaults > 0:
        args_default = code.co_varnames[:code.co_argcount][-num_defaults:]
        kwargs_defaults = dict(zip(args_default, func.__defaults__))
                                      
        kwargs_positional_keys = [k for k in args_default if k not in kwargs]         # f(k1, k2=v2, ...) called as f(v1, v2, ...) 
        kwargs_positional = dict(zip(kwargs_positional_keys, args[num_static:]))
        num_kwargs_positional = len(kwargs_positional)
        
        kwargs = {**kwargs_positional, **kwargs}        
    else:
        num_kwargs_positional = 0
        kwargs_defaults = {}
        
    kwargs_defaults.update(kwonly_defaults)
                    
    full_kwargs = {**kwargs_defaults, **kwargs}
    static_attrs = {k: v for k, v in zip(code.co_varnames[:num_static], args)}    
    attrs = {**static_attrs, **full_kwargs} 
    
    pos_only_name = [p.name for p in inspect.signature(func).parameters.values() if p.kind.name == "VAR_POSITIONAL"]
    if pos_only_name:
        pos_only_name = f"*{pos_only_name[0]}"
    else:
        pos_only_name = "*pos_only"
    pos_only = {pos_only_name: len(args) - num_static - num_kwargs_positional}
    if add_pos_only_to_all:
        attrs.update(pos_only)
    
    key_opts = dict(kwargs_defaults = kwargs_defaults,
                    kwargs = kwargs,      
                    kwargs_full = full_kwargs,
                    args = static_attrs,
                    pos_only = pos_only,
                    all = attrs
    )
    return key_opts

def merge_wrapper_signatures(wrapper, wrapper_params):
    """
    Add parameters from the wrapper function (called by @functools.wraps) to its signature.
    Wrapper params are assumed to be keyword-only.
    
    Attrs:
            - wrapper:           wrapper function
            - wrapper_params:    params of wrapper to be added to the signature.
    """
    sig = inspect.signature(wrapper, follow_wrapped=True)
    sigw = inspect.signature(wrapper, follow_wrapped=False)
    params = tuple(sig.parameters.values())
    params_extra = tuple(p for p_name, p in sigw.parameters.items() if p_name in wrapper_params)
    if len(params) > 0 and params[-1].kind.name == "VAR_KEYWORD": # f(any_args, **kwargs)
        params_full = (*params[:-1], *params_extra, params[-1])
    else:
        params_full = (*params, *params_extra)
    return sig.replace(parameters=params_full)

def get_class_that_defined_method(meth, default=None):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__, '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', default)  # handle special descriptor objects

def delete_cls_self_arg(args):
    if args:
        if inspect.isclass(args[0]) or isinstance(args[0], get_class_that_defined_method(func, default=type(None))): # classmethod or instance method
            args = args[1:]
    return args