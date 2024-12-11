import datetime
import os
from collections import OrderedDict
import memsimul as me
import ampm, stride, best_offset as bo, ghb, sms



if __name__ == "__main__":
    filepath = "D:/OneDrive-Personal/OneDrive/VSC/Python/지능형/project/memSimul/trace/prank_afterCache.txt"  # Path to the trace file
    output_directory = "D:/OneDrive-Personal/OneDrive/VSC/Python/지능형/project/memSimul/result"  # Directory to save results
    algorithm_name = "prank"  # Example algorithm name parsed from the trace file name
    prefetcher_name = "no_prefetcher"  # Example prefetcher name

    # Example: Using no prefetcher
    prefetcher = stride.Prefetcher()

    simulator = me.MemorySimulator(cache_size=128, ram_size_mb=2048, prefetcher=prefetcher)
    simulator.load_trace_file(filepath)
    simulator.simulate()
    simulator.save_results_to_file(directory=output_directory, algorithm_name=algorithm_name, prefetcher_name=prefetcher_name)