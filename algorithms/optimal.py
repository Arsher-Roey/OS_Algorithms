def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    frames: list[int | None] = [None] * frame_count
    steps: list[dict] = []
    faults = 0

    for i, page in enumerate(ref_string):
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                idx = frames.index(None)
                frames[idx] = page
            else:
                future = ref_string[i + 1:]

                def _next_use(p: int) -> int | float:
                    try:
                        return future.index(p)
                    except ValueError:
                        return float("inf")

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
