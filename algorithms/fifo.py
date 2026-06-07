"""
algorithms/fifo.py
==================
First-In First-Out (FIFO) Page Replacement Algorithm.

Eviction policy: The page that has been in memory the longest is replaced.
A simple queue tracks insertion order; the front of the queue is always
the oldest resident page.

Time complexity : O(n)  where n = len(ref_string)
Space complexity: O(f)  where f = frame_count
"""


def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    """
    Simulate FIFO page replacement.

    Args:
        ref_string  – ordered list of page-number references
        frame_count – number of physical memory frames

    Returns:
        (steps, total_faults)

    Step dict keys:
        page    – page number referenced this step
        frames  – list[int | None] snapshot of all frames after this step
        fault   – True if a page fault occurred
        evicted – page that was evicted (None if frames not full yet)
    """
    frames: list[int | None] = [None] * frame_count
    # FIFO queue — front is the oldest page
    queue: list[int] = []
    steps: list[dict] = []
    faults = 0

    for page in ref_string:
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                # Free slot available — fill it
                idx = frames.index(None)
                frames[idx] = page
                queue.append(page)
            else:
                # All frames occupied — evict the oldest
                evicted = queue.pop(0)
                idx = frames.index(evicted)
                frames[idx] = page
                queue.append(page)

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
