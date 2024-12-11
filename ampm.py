class Prefetcher:
    def __init__(self):
        self.pages = {}

    def prefetch(self, address):
        page_index = address >> 12  # Page index
        page_offset = address & 0xFFF  # Offset within the page
        if page_index not in self.pages:
            self.pages[page_index] = [0] * 16
        access_map = self.pages[page_index]
        access_map[page_offset >> 8] = 1
        prefetch_candidates = []
        for i, accessed in enumerate(access_map):
            if accessed:
                prefetch_candidates.append((page_index << 12) + (i << 8))
        return prefetch_candidates
