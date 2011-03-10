class BaseCommand(object):
    def __init__(self):
        pass

    def call(self, *args, **kwargs):
        raise NotImplementedError("Call not implemented")

