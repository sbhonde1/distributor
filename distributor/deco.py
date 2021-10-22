import inspect
import ast
from . import util
import types
import ray
ray.init()



def concWrapper(f, args, kwargs):
    result = Compute.functions[f](*args, **kwargs)
    operations = [inner for outer in args + list(kwargs.values()) if type(outer) is argProxy for inner in outer.operations]
    return result, operations


class argProxy(object):
    def __init__(self, arg_id, value):
        self.arg_id = arg_id
        self.operations = []
        self.value = value

    def __getattr__(self, name):
        if name in ["__getstate__", "__setstate__"]:
            raise AttributeError
        if hasattr(self, 'value') and hasattr(self.value, name):
            return getattr(self.value, name)
        raise AttributeError

    def __setitem__(self, key, value):
        self.value.__setitem__(key, value)
        self.operations.append((self.arg_id, key, value))

    def __getitem__(self, key):
        return self.value.__getitem__(key)


class Synchronized(object):
    def __init__(self, func):
        callerframerecord = inspect.stack()[1][0]
        info = inspect.getframeinfo(callerframerecord)
        stack = inspect.stack()
        self.frame_info = info
        self.orig_f = func
        self.func = None
        self.ast = None
        self.__name__ = func.__name__

    def __get__(self, *args):
        print("get called")
        pass

    def __call__(self, *args, **kwargs):
        if self.func is None:
            source = inspect.getsourcelines(self.orig_f)[0]
            util.unindent(source)
            source = "".join(source)
            self.ast = ast.parse(source)
            rewriter = util.SchedulerRewriter(Compute.functions.keys(), self.frame_info)
            rewriter.visit(self.ast.body[0])
            ast.fix_missing_locations(self.ast)
            out = compile(self.ast, "<string>", "exec")
            scope = dict(self.orig_f.__globals__)
            exec(out, scope)
            self.func = scope[self.orig_f.__name__]
        return self.func(*args, **kwargs)


class Compute(object):
    functions = {}

    def __init__(self, *args, **kwargs):
        self.in_progress = False
        self.conc_args = []
        self.conc_kwargs = {}
        if len(args) > 0 and \
            hasattr(args[0], "__call__") and \
            hasattr(args[0], "__name__"):
            self.set_function(args[0])
        else:
            self.conc_args = args
            self.conc_kwargs = kwargs
        self.results = []
        self.assigns = []
        self.calls = []
        self.arg_proxies = {}
        """
        wrapper = Wrapper.remote(self.args[0], self.kwargs["func_args"])
        self.futures.append(wrapper.run.remote())
        """
        self.apply_async = lambda self, function, args: Wrapper.remote(function, args).run.remote()

    def __get__(self, *args):
        pass

    def call(self, target, *args, **kwargs):
        self.calls.append((target, self(*args, **kwargs)))

    def replace_with_proxies(self, args):
        args_iter = args.items() if type(args) is dict else enumerate(args)
        for i, arg in args_iter:
            if type(arg) is dict or type(arg) is list:
                if not id(arg) in self.arg_proxies:
                    self.arg_proxies[id(arg)] = argProxy(id(arg), arg)
                args[i] = self.arg_proxies[id(arg)]

    def __call__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], types.FunctionType):
            self.set_function(args[0])
            return self
        self.in_progress = True
        args = list(args)
        self.replace_with_proxies(args)
        self.replace_with_proxies(kwargs)
        result = Result(self.apply_async(self, concWrapper, [self.f_name, args, kwargs]))
        self.results.append(result)
        return result

    def set_function(self, func):
        Compute.functions[func.__name__] = func
        self.f_name = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__


class Result(object):
    def __init__(self, async_result):
        self.async_result = async_result

    def get(self):
        return ray.get(self.async_result)

    def result(self):
        return self.get()[0]

@ray.remote
class Wrapper(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.args[0](self.args[1])
        return result
