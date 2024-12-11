class Prefetcher:
    def __init__(self):
        self.history = []

    def prefetch(self, address):
        self.history.append(address)
        if len(self.history) > 3:
            self.history.pop(0)
        if len(self.history) == 3:
            stride1 = self.history[1] - self.history[0]
            stride2 = self.history[2] - self.history[1]
            if stride1 == stride2:
                return [self.history[2] + stride1]
        return []
