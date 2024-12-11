import datetime
import os
from collections import OrderedDict

class MemorySimulator:
    def __init__(self, cache_size=64, ram_size_mb=2048, prefetcher=None):
        """Initialize the memory simulator with a given cache size, RAM size, and prefetcher."""
        self.cache = OrderedDict()  # Cache as an ordered dictionary for LRU
        self.cache_size = cache_size  # Maximum number of entries in the cache
        self.memory = OrderedDict()  # Simulated memory with LRU eviction
        self.max_ram_size = ram_size_mb * 1024 * 1024  # Convert MB to bytes
        self.current_ram_usage = 0
        self.operations = []  # Record of operations for debugging
        self.prefetcher = prefetcher  # Prefetcher instance
        self.stats = {
            'access_count': 0,
            'cache_hit': 0,
            'cache_miss': 0,
            'writes': 0,
            'reads': 0,
            'inst_reads': 0,
            'inst_writes': 0,
            'prefetches': 0,
            'useless_prefetches': 0
        }
        self.prefetched_addresses = set()  # Track prefetched addresses

    def load_trace_file(self, filepath):
        """Load memory access trace from a file."""
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    op_type = int(parts[0])  # Operation type
                    address = int(parts[1], 16)  # Convert address from hex to int
                    self.operations.append((op_type, address))

    def read(self, address, is_instruction=False):
        """Simulate a memory read operation."""
        self.stats['access_count'] += 1
        if is_instruction:
            self.stats['inst_reads'] += 1
        else:
            self.stats['reads'] += 1

        if address in self.cache:
            self.stats['cache_hit'] += 1
            self.cache.move_to_end(address)  # Update for LRU
            if address in self.prefetched_addresses:
                self.stats['prefetches'] += 1  # Count as a prefetch hit
                self.prefetched_addresses.remove(address)  # Mark as used
        else:
            self.stats['cache_miss'] += 1
            if address in self.memory:
                value = self.memory[address]
                self._add_to_cache(address, value)

            # Check for unused prefetches
            unused_prefetches = self.prefetched_addresses - {address}
            self.stats['useless_prefetches'] += len(unused_prefetches)
            self.prefetched_addresses = set()  # Reset prefetched addresses

            # Trigger prefetcher if available
            if self.prefetcher:
                prefetch_addresses = self.prefetcher.prefetch(address)
                for p_address in prefetch_addresses:
                    if p_address not in self.cache and p_address not in self.memory:
                        self._add_to_cache(p_address, hash(p_address))
                        self.prefetched_addresses.add(p_address)

    def write(self, address, is_instruction=False):
        """Simulate a memory write operation."""
        self.stats['access_count'] += 1
        if is_instruction:
            self.stats['inst_writes'] += 1
        else:
            self.stats['writes'] += 1

        value = hash(address)  # Example: storing a hash as the value
        self._add_to_memory(address, value)
        self._add_to_cache(address, value)

    def _add_to_memory(self, address, value):
        """Add a memory entry to the simulated RAM, evicting if necessary."""
        address_str = str(address)  # Convert address to string
        entry_size = len(address_str.encode('utf-8')) + len(str(value).encode('utf-8'))  # Estimate size in bytes
        while self.current_ram_usage + entry_size > self.max_ram_size:
            evicted_address, evicted_value = self.memory.popitem(last=False)  # Evict oldest entry
            evicted_address_str = str(evicted_address)  # Convert evicted address to string
            evicted_size = len(evicted_address_str.encode('utf-8')) + len(str(evicted_value).encode('utf-8'))
            self.current_ram_usage -= evicted_size
        self.memory[address] = value
        self.current_ram_usage += entry_size

    def _add_to_cache(self, address, value):
        """Add a memory entry to the cache, evicting if necessary."""
        if address in self.cache:
            self.cache.move_to_end(address)  # Update for LRU
        else:
            if len(self.cache) >= self.cache_size:
                self.cache.popitem(last=False)  # Evict the least recently used entry
            self.cache[address] = value

    def simulate(self):
        """Run the simulation based on loaded operations."""
        for op_type, address in self.operations:
            if op_type == 0:
                self.read(address)
            elif op_type == 1:
                self.write(address)
            elif op_type == 2:
                self.read(address, is_instruction=True)
            elif op_type == 3:
                self.write(address, is_instruction=True)

    def save_results_to_file(self, directory=".", algorithm_name="default", prefetcher_name="no_prefetcher"):
        """Save the simulation results to a formatted file in the specified directory."""
        if not os.path.exists(directory):
            os.makedirs(directory)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(directory, f"{timestamp}-{algorithm_name}-{prefetcher_name}.txt")

        # Calculate Total Hit Rate, Miss Rate, Prefetch Hit Rate
        total_access = self.stats['access_count']
        total_hit = self.stats['cache_hit']
        total_miss = self.stats['cache_miss']
        total_prefetch_hits = self.stats['prefetches']  # Prefetch hits already tracked
        total_prefetches = self.stats['prefetches'] + self.stats['useless_prefetches']

        total_hit_rate = total_hit / total_access if total_access > 0 else 0
        total_miss_rate = total_miss / total_access if total_access > 0 else 0
        prefetch_hit_rate = (total_prefetch_hits / total_prefetches) * 100 if total_prefetches > 0 else 0

        with open(filename, 'w') as f:
            f.write("=========================Simulation Results=========================" + "\n")
            f.write(f"Access count : \t{self.stats['access_count']}\n")
            f.write(f"[HIT] : \t{self.stats['cache_hit']}\t  [MISS] : \t{self.stats['cache_miss']}\n")
            f.write(f"[DATA READS] : \t{self.stats['reads']}\t  [DATA WRITES] : \t{self.stats['writes']}\n")
            f.write(f"[INST READS] : \t{self.stats['inst_reads']}\t  [INST WRITES] : \t{self.stats['inst_writes']}\n")
            f.write(f"[PREFETCHES] : \t{total_prefetches}\t  [USELESS PREFETCHES] : \t{self.stats['useless_prefetches']}\n")
            f.write(f"Current RAM Usage : \t{self.current_ram_usage // (1024 * 1024)} MB / {self.max_ram_size // (1024 * 1024)} MB\n")
            f.write("=========================SUMMARY=========================" + "\n")
            f.write(f"[TOTAL HIT RATE] : \t{total_hit_rate:.2f}\n")
            f.write(f"[TOTAL MISS RATE] : \t{total_miss_rate:.2f}\n")
            f.write(f"[PREFETCH HIT RATE] : \t{prefetch_hit_rate:.2f}\n")
            f.write("=========================END=========================" + "\n")
        print(f"Results saved to {filename}")





class Prefetcher:
    def prefetch(self, address):
        """No prefetching policy."""
        return []


