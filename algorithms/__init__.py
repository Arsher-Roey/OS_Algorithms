"""
algorithms/__init__.py
======================
Central registry for all virtual-memory page-replacement algorithms.

Each algorithm module must expose a single function with this signature:

    def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
        \"\"\"
        Args:
            ref_string  – ordered list of page numbers to reference
            frame_count – number of physical memory frames available

        Returns:
            steps       – list of step dicts, one per page reference:
                            {
                              "page":    int,          # page number referenced this step
                              "frames":  list[int|None], # frame state after this step
                              "fault":   bool,         # True = page fault occurred
                              "evicted": int | None,   # page evicted (None if no eviction)
                            }
            faults      – total page fault count
        \"\"\"

To register a new algorithm:
    1. Create algorithms/your_algo.py  with a run() that matches the signature above.
    2. Import it here and add an entry to REGISTRY.
"""

from algorithms import fifo, optimal, lru, lru_approximation, counting_based

# Maps the exact string shown in the UI dropdown → algorithm module
REGISTRY: dict = {
    "FIFO (First-In First-Out)":      fifo,
    "Optimal":                         optimal,
    "LRU (Least Recently Used)":       lru,
    "LRU Approximation":               lru_approximation,
    "Counting-Based Page Replacement": counting_based,
}
