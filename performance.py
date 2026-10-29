"""Compare sequential and threaded metadata collection for the same files."""
import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def inspect_file(path):
    try:
        return path, os.path.getsize(path)
    except OSError:
        return path, None


def measure(files, threaded=False, workers=4):
    start = time.perf_counter()
    if threaded:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(inspect_file, files))
    else:
        results = [inspect_file(path) for path in files]
    return time.perf_counter() - start, results


def main():
    parser = argparse.ArgumentParser(description='Compare file metadata processing methods')
    parser.add_argument('folder', help='Folder to benchmark')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    if not os.path.isdir(args.folder) or args.workers < 1:
        parser.error('Choose an existing folder and at least one worker')
    paths = [str(path) for path in Path(args.folder).rglob('*') if path.is_file()]
    if not paths:
        print('No files found in that folder.')
        return
    times = []
    for _ in range(3):
        sequential, a = measure(paths)
        parallel, b = measure(paths, threaded=True, workers=args.workers)
        assert a == b, 'Results differ between methods'
        times.append((sequential, parallel))
    seq = sum(x for x, _ in times) / len(times)
    threaded = sum(y for _, y in times) / len(times)
    print(f'Files: {len(paths)}; threads: {args.workers}; 3 runs')
    print(f'Sequential average: {seq:.4f} seconds')
    print(f'Threaded average:   {threaded:.4f} seconds')
    print(f'Speed-up (seq/threaded): {seq / threaded:.2f}x')
    print('Amdahl example: 80% parallelisable, 4 workers -> '
          f'{1 / (0.2 + 0.8 / 4):.2f}x theoretical maximum.')
    print('These are measurements of file metadata I/O, not a CPU-heavy workload.')


if __name__ == '__main__':
    main()
