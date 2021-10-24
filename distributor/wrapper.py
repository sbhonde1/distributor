import ray


# @ray.remote
# class Wrapper(object):
#
#     def __init__(self, *args, **kwargs):
#         self.args = args
#         self.kwargs = kwargs
#
#     def run(self):
#         result = self.args[0](self.args[1])
#         return result

@ray.remote
def f(func, args):
    # print("f()", func.__name__, args)
    return func(args)


def parameterized_compute(n=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            objs = []
            for i in range(n):
                objs.append(f.remote(func, args[0]))
            return ray.get(objs)
        return wrapper
    return decorator


class _Compute(object):

    def __init__(self, func, n=1):
        self.func = func
        self.n = n
        self.futures = []

    def run(self):
        return ray.get(self.futures)

    def __call__(self, *args, **kwargs):
        for i in range(self.n):
            self.futures.append(f.remote(self.func, args[0]))
        return self

# wrap _Param_Compute to allow for deferred calling
def Compute(function=None, n=1):
    if function:
        return _Compute(function)
    else:
        def wrapper(function):
            return _Compute(function, n)

        return wrapper

