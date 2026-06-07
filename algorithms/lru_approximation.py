"""
algorithms/lru_approximation.py
================================
LRU Approximation — Clock / Second-Chance Algorithm.

Eviction policy: A circular "clock" of frames is maintained.  Each frame has
a *reference bit* (R).  When a page is accessed, R is set to 1.  On a fault,
the clock hand sweeps forward:
  - If R == 1  → clear R (give a "second chance") and advance the hand.
  - If R == 0  → evict this page.

This is also known as the "Clock Algorithm" or "Second-Chance Algorithm".
It approximates LRU with O(1) amortised eviction cost.

Time complexity : O(n · f)  worst-case (full sweep each fault)
Space complexity: O(f)
"""


def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    """
    Simulate the Clock (LRU Approximation) page replacement algorithm.

    Args:
        ref_string  – ordered list of page-number references
        frame_count – number of physical memory frames

    Returns:
        (steps, total_faults)

    Step dict keys:
        page    – page number referenced this step
        frames  – list[int | None] snapshot of all frames after this step
        fault   – True if a page fault occurred
        evicted – page that was evicted (None if no eviction this step)
    """
    frames: list[int | None] = [None] * frame_count
    ref_bits: list[int] = [0] * frame_count   # reference bit per frame slot
    hand: int = 0                              # clock hand position
    steps: list[dict] = []
    faults = 0

    for page in ref_string:
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                # Fill the first empty slot (initial load phase)
                idx = frames.index(None)
                frames[idx] = page
                ref_bits[idx] = 1
            else:
                # Clock sweep to find a victim
                while True:
                    if ref_bits[hand] == 0:
                        # Evict this page
                        evicted = frames[hand]
                        frames[hand] = page
                        ref_bits[hand] = 1
                        hand = (hand + 1) % frame_count
                        break
                    else:
                        # Second chance: clear R bit and advance
                        ref_bits[hand] = 0
                        hand = (hand + 1) % frame_count
        else:
            # Hit — set the reference bit for the accessed page
            idx = frames.index(page)
            ref_bits[idx] = 1

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
