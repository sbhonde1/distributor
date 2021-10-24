class PytorchModel:
    # TODO: Modify this as you see fit
    def __init__(self, *args, **kwargs):
        print("PytorchModel init()")
        self.args = args
        self.kwargs = kwargs

    def load(self):
        print("PyTorch load()")
        return None

    def save(self):
        print("PyTOrch save()")
        return None

    def run(self):
        print("PyTorch run()")
        return None


class XgboostModel:
    # TODO: Modify this as you see fit
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def load(self):
        return None

    def save(self):
        return None
