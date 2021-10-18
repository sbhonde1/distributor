from distributor.wrapper import Compute


@Compute
def calculate(n):
    def square(x):
        return x * x
    result = []
    for i in range(n):
        result.append(square(i))
    return result


print(calculate(10).run())
# print(square(2))