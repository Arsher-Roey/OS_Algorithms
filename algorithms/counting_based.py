"""
algorithms/counting_based.py
=============================
Counting-Based Page Replacement — LFU or MFU.

LFU (Least Frequently Used)
  Eviction policy: Evict the page with the smallest reference count.
  Ties broken by lowest frame index (approximates FIFO among equally-cold pages).

MFU (Most Frequently Used)
  Eviction policy: Evict the page with the LARGEST reference count.
  Counter-intuitive but useful as a study: assumes highly-used pages are less
  likely to be needed again in the near future.

Select the variant via the `mode` parameter: "LFU" (default) or "MFU".

Time complexity : O(n · f)
Space complexity: O(f)
"""


def run(
    ref_string: list[int],
    frame_count: int,
    mode: str = "LFU",
) -> tuple[list[dict], int]:
    """
    Simulate LFU or MFU page replacement.

    Args:
        ref_string  – ordered list of page-number references
        frame_count – number of physical memory frames
        mode        – "LFU" (default) or "MFU"

    Returns:
        (steps, total_faults)

    Step dict keys:
        page    – page number referenced this step
        frames  – list[int | None] snapshot of all frames after this step
        fault   – True if a page fault occurred
        evicted – page that was evicted (None if no eviction this step)
    """
    frames: list[int | None] = [None] * frame_count
    # Per-frame reference count; reset to 1 when a new page is loaded
    counts: list[int] = [0] * frame_count
    steps: list[dict] = []
    faults = 0

    for page in ref_string:
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                # Place in first empty slot
                idx = frames.index(None)
                frames[idx] = page
                counts[idx] = 1
            else:
                # Choose victim by policy
                if mode == "MFU":
                    # Evict the MOST frequently used page
                    target_count = max(counts)
                else:
                    # Evict the LEAST frequently used page (default LFU)
                    target_count = min(counts)

                # Left-to-right tie-breaking (earliest frame index)
                idx = counts.index(target_count)
                evicted = frames[idx]
                frames[idx] = page
                counts[idx] = 1          # reset count for the newly loaded page
        else:
            # Hit — increment the reference count for this page
            idx = frames.index(page)
            counts[idx] += 1

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
