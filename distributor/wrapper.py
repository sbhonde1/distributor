import ray

ray.init()


# @ray.remote
class Compute(object):
    """
    This class is a decorator class which is a wrapper to x class that runs ray.
    We need to pass given function to ray class and then call it by using run method
    """

    def __init__(self, *args, **kwargs):
        print("init ", args, kwargs)
        self.args = args
        self.kwargs = kwargs

    # @ray.method(num_returns=1)
    def run(self):
        print("run")
        wrapper = Wrapper.remote(self.args[0], self.kwargs["func_args"])
        # wrapper.reset.remote()
        results = wrapper.run.remote()
        results = ray.get(results)
        return results
        # print(self.args[0](x))
        # print("run", self.args, self.kwargs)

    def __call__(self, *args, **kwargs):
        print("call", args, kwargs)
        self.kwargs["func_args"] = args[0]
        return self


@ray.remote
class Wrapper(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.args[0](self.args[1])
        return result


