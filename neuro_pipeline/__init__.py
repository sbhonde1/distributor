
def artifacts(*artifact_args):
    # TODO: Modify this as you see fit
    print("artifact()", artifact_args[0][0])
    def decorator(*args):

        print("wrapper() ", args[0])
        # args[0].set_model(artifact_args[0][0])
        print("wrapper() ", args[0].__name__)
        return args[0]
    return decorator
