class Prefetcher:
    def __init__(self):
        self.history = {}
        self.name = "sms"

    def prefetch(self, address):
        base_address = address & ~0xFFF  # Align to page boundary
        if base_address not in self.history:
            self.history[base_address] = set()
        offsets = self.history[base_address]
        prefetch_candidates = [base_address + (offset << 12) for offset in range(16) if offset not in offsets]
        offsets.add(address & 0xFFF)
        return prefetch_candidates
