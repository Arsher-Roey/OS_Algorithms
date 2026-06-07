"""
algorithms/optimal.py
=====================
Optimal (Bélády's) Page Replacement Algorithm.

Eviction policy: Evict the page whose next use is furthest in the future.
If a page will never be used again, it is chosen first (treated as infinitely
far away).  This produces the theoretically minimum number of page faults and
is used as a benchmark; it requires future knowledge of the reference string.

Time complexity : O(n · f)  where n = len(ref_string), f = frame_count
Space complexity: O(f)
"""


def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    """
    Simulate Optimal (Bélády's) page replacement.

    Args:
        ref_string  – ordered list of page-number references
        frame_count – number of physical memory frames

    Returns:
        (steps, total_faults)

    Step dict keys:
        page    – page number referenced this step
        frames  – list[int | None] snapshot of all frames after this step
        fault   – True if a page fault occurred
        evicted – page that was evicted (None if frames not full yet or no fault)
    """
    frames: list[int | None] = [None] * frame_count
    steps: list[dict] = []
    faults = 0

    for i, page in enumerate(ref_string):
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                # Free slot — place the page there
                idx = frames.index(None)
                frames[idx] = page
            else:
                # Evict the page whose next reference is furthest away
                future = ref_string[i + 1:]

                def _next_use(p: int) -> int | float:
                    try:
                        return future.index(p)
                    except ValueError:
                        return float("inf")   # never used again → evict first

                victim = max(frames, key=_next_use)
                idx = frames.index(victim)
                evicted = victim
                frames[idx] = page

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
