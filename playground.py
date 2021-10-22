# from distributor.wrapper import Compute
from distributor.deco import Compute, Synchronized
import time


def _square(x):
    return x * x


@Compute
def square(x):
    return x * x


@Synchronized
def calculate(n):

    result = []
    for i in range(int(n)):
        result.append(square(i))
    return result


print("ray")
# n = 1e8
n = 10
start = time.time()
ray_result = calculate(n)
print(time.time() - start)
print(ray_result)


print("serial")
start = time.time()
result = []
for i in range(int(n)):
    result.append(_square(i))
print(time.time() - start)
print(result[:10])
