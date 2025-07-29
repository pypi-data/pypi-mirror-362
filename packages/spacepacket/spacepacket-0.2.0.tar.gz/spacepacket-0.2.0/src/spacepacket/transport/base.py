class Transport:
    def __init__(self):
        self.config = None

    def connect(self, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        pass

    def request(self, pdu):
        raise NotImplementedError

    def indication(self, pdu):
        pass

    def shutdown(self):
        pass
