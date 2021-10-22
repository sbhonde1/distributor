import ray
ray.init()


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
        # print("run")
        results = ray.get(self.futures)
        return results

    def __call__(self, *args, **kwargs):
        # print("call", args, kwargs)
        self.kwargs["func_args"] = args[0]
        wrapper = Wrapper.remote(self.args[0], self.kwargs["func_args"])
        self.futures.append(wrapper.run.remote())
        return self


@ray.remote
class Wrapper(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.args[0](self.args[1])
        return result


