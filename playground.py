from distributor.wrapper import Param_Compute
# from distributor.deco import Compute, Synchronized
import time
import ray
ray.init()


def _square(x):
    time.sleep(1e-3)
    return x * x


@Param_Compute(n=int(1e5))
def square(x):
    time.sleep(1e-3)
    return x * x

# @ray.remote
# @Synchronize
# def calculate(n):
#
#     result = []
#     for i in range(int(n)):
#         result.append(square(i))
#     result = ray.get(result)
#     return result


# def calculate(x)

print("ray")
n = int(1e5)
# n = 2
start = time.time()
ray_result = square(10).run()
# ray_result = ray.get(ray_obj)
print("time taken : ", time.time() - start)
print(len(ray_result), ray_result[0])


print("serial")
start = time.time()
result = []
for i in range(int(n)):
    result.append(_square(i))
print("time taken : ", time.time() - start)
print(result[:10])
