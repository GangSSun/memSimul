class Prefetcher:
    def __init__(self):
        self.last_address = None
        self.stride = None

    def prefetch(self, address):
        if self.last_address is not None:
            new_stride = address - self.last_address
            if new_stride == self.stride:
                return [address + new_stride]
            self.stride = new_stride
        self.last_address = address
        return []
