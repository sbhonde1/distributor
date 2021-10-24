import ray


@ray.remote
class Wrapper(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.args[0](self.args[1])
        return result

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


class _Param_Compute(object):

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
def Param_Compute(function=None, n=1):
    if function:
        return _Param_Compute(function)
    else:
        def wrapper(function):
            return _Param_Compute(function, n)

        return wrapper

class Compute(object):
    """
    This class is a decorator class which is a wrapper to x class that runs ray.
    We need to pass given function to ray class and then call it by using run method
    """

    def __init__(self, *args, **kwargs):
        print("init ", args, kwargs)
        self.args = args
        self.kwargs = kwargs
        self.futures = []

    def run(self):
        print("run")
        print(len(self.futures))

        results = ray.get(self.futures[0])
        print("ray results", results)
        print("run end")
        return results

    def __call__(self, *args, **kwargs):
        # print("call", args, kwargs)
        self.kwargs["func_args"] = args[0]
        # wrapper = Wrapper.remote(self.args[0], self.kwargs["func_args"])
        # self.futures.append(wrapper.run.remote())
        self.futures.append(f.remote(self.args[0], self.kwargs["func_args"]))
        # print("call", self.futures)
        return self


# class Compute_test1(object):
#     """
#     This class is a decorator class which is a wrapper to x class that runs ray.
#     We need to pass given function to ray class and then call it by using run method
#     """
#
#     def __init__(self, *args, **kwargs):
#         print("init ", args, kwargs)
#         self.args = args
#         self.kwargs = kwargs
#     futures = []
#     @staticmethod
#     def run():
#         print("run")
#         print(len(Compute_test1.futures))
#
#         results = ray.get(Compute_test1.futures[0])
#         print("ray results", results)
#         print("run end")
#         return results
#
#     def __call__(self, *args, **kwargs):
#         # print("call", args, kwargs)
#         self.kwargs["func_args"] = args[0]
#         # wrapper = Wrapper.remote(self.args[0], self.kwargs["func_args"])
#         # self.futures.append(wrapper.run.remote())
#         Compute_test1.futures.append(f.remote(self.args[0], self.kwargs["func_args"]))
#         # print("call", self.futures)
#         return self
#
# @ray.actor
# class Compute_ray(Compute_test1):
#     def __init__(self):
#         Compute_test1.__init__(self)
#     def run(self):

#
# class Synchronize(object):
#     def __init__(self, *args, **kwargs):
#         print("init ", args, kwargs)
#         self.args = args
#         self.kwargs = kwargs
#         self.futures = []
#
#     def set_futures(self, future):
#         self.futures.append(future)
#
#     def run(self):
#         results = ray.get(self.futures)
#         return results
#
#     def __call__(self, *args, **kwargs):
#
#         return self

