class Prefetcher:
    def __init__(self):
        self.best_offset = 64  # Example offset in bytes
        self.name = "best_offset"

    def prefetch(self, address):
        return [address + self.best_offset]
