import neuro_pipeline as pipe
from neuro_pipeline.objects import NpuModel
from neuro_pipeline.frameworks import PytorchModel

import torch

net = torch.nn.Sequential(
    torch.nn.Linear(4, 10),
    torch.nn.ReLU(),
    torch.nn.Linear(10, 1))

x = torch.rand((2, 4), requires_grad=False)


@pipe.artifacts([PytorchModel('model')])
class MyModel(NpuModel):
    def __init__(self):
        print("MyModel init()")
        super().__init__()
        self.artifact = None

    def prediction(self, x):
        print("prediction()")
        out = self.model(x)
        return out

    def run(self, x):
        print("run()")
        out = self.prediction(x)
        return out

model = MyModel()
model.artifacts({'model': net})
out = model.run(x)
