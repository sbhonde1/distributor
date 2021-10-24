class NpuModel:
    # TODO: Modify this as you see fit

    def __init__(self, *args, **kwargs):
        print("NpuModel init()", args, kwargs)
        self.args = args
        self.kwargs = kwargs
        self.model_type = None

    def artifacts(self, x):
        self.artifact = x
        self.model = x['model']

    def get_model(self):
        return self.model

    def run(self):
        return None

    def save(self):
        return None

    def load(self):
        return None

