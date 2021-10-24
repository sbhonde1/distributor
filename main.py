# import ray
# ray.init()


# class ComputeThis:
#
#     def __init__(self, func):
#         self.func = func
#
#     def run(self,):
#         print("run")
#
#     def wrapper(self, *args, **kwargs):
#         print("wrapper")
#         self.func(*args, **kwargs)
#
#     def __call__(self, *args, **kwargs):
#         return self

def ComputeThis(*args):
    def run(cls):
        print("hello")
    return run



@ComputeThis(2)
class Bar:
    pass

# def square(x):
#     return x * x

print(Bar().__doc__)

# square(2).run()



