import os
import re
import memsimul as me
import ampm, stride, best_offset as bo, ghb, sms
import ML, RL

if __name__ == "__main__":
    trace_directory = "D:/OneDrive-Personal/OneDrive/VSC/Python/지능형/project/memSimul/trace"  # Trace files directory
    output_directory = "D:/OneDrive-Personal/OneDrive/VSC/Python/지능형/project/memSimul/result"  # Directory to save results

    # 사용할 프리페처 목록
    prefetchers = [
        me.Prefetcher(),
        stride.Prefetcher(),
        ampm.Prefetcher(),
        bo.Prefetcher(),
        ghb.Prefetcher(),
        sms.Prefetcher(),
        ML.AIMLPrefetcher(),
        RL.AIPrefetcher()
    ]

    # Trace 디렉토리의 모든 파일에 대해 실행
    for trace_file in os.listdir(trace_directory):
        if trace_file.endswith("_afterCache.txt"):  # 트레이스 파일 이름 필터링
            filepath = os.path.join(trace_directory, trace_file)
            
            # 파일 이름에서 알고리즘 이름 추출
            match = re.search(r"(.+?)_afterCache", trace_file)
            if match:
                algorithm_name = match.group(1)
            else:
                print(f"Skipping file {trace_file}: Unable to extract algorithm name.")
                continue
            
            for prefetcher in prefetchers:
                print(f"Processing {trace_file} with {prefetcher.name} prefetcher...")
                simulator = me.MemorySimulator(cache_size=128, ram_size_mb=2048, prefetcher=prefetcher)
                simulator.load_trace_file(filepath)
                simulator.simulate()
                simulator.save_results_to_file(
                    directory=output_directory,
                    algorithm_name=algorithm_name,
                    prefetcher_name=prefetcher.name
                )
