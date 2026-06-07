"""
algorithms/lru.py
=================
Least Recently Used (LRU) Page Replacement Algorithm.

Eviction policy: Evict the page that has not been referenced for the longest
time.  An ordered list tracks recency — the front holds the least recently
used page and the back holds the most recently used page.

Time complexity : O(n · f)
Space complexity: O(f)
"""


def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    """
    Simulate LRU page replacement.

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
    # Recency stack: index 0 = least recently used, index -1 = most recent
    recency: list[int] = []
    steps: list[dict] = []
    faults = 0

    for page in ref_string:
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                # Free slot available
                idx = frames.index(None)
                frames[idx] = page
            else:
                # Evict the least recently used page
                lru_page = recency[0]
                idx = frames.index(lru_page)
                evicted = lru_page
                frames[idx] = page
                recency.pop(0)
        else:
            # Hit — just update recency (remove old position, re-add at back)
            recency.remove(page)

        recency.append(page)

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
