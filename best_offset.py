class Prefetcher:
    def __init__(self):
        self.best_offset = 64  # Example offset in bytes

    def prefetch(self, address):
        return [address + self.best_offset]
