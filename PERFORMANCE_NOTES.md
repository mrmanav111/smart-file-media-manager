# Task 8 — Performance and parallelism

Run `py performance.py "D:/music"` **after** opening the project in VS Code. The script performs three runs using the same file paths for two approaches: sequential metadata reads and threaded metadata reads (`ThreadPoolExecutor`, 4 workers). It checks that both approaches return the same data before reporting averages.

| Method | Average seconds (fill from actual output) |
|---|---|
| Sequential | — |
| Threaded (4 workers) | — |
| Speed-up (sequential / threaded) | — |

File metadata operations are mostly I/O-bound, so threads may help when waiting on slower storage, but can also be slower because of thread scheduling and futures overhead. CPU-bound Python code often benefits less from threads because of interpreter constraints, although details depend on Python version and libraries. Results vary with the storage device, cache, file count and system load. Do not invent the measurements.

**Amdahl's Law:** Speed-up = 1 / ((1-p) + p/n). For an illustrative workload that is 80% parallelisable on 4 workers, speed-up = 1 / (0.20 + 0.80/4) = 2.50x. This is a theoretical illustration, **not the measured performance** of the application. The remaining 20% of sequential work and parallel overhead limit gains. Threaded map over a collection of file paths demonstrates a Python equivalent of the parallel-query idea.
