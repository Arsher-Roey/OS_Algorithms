def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    frames: list[int | None] = [None] * frame_count
    recency: list[int] = []
    steps: list[dict] = []
    faults = 0

    for page in ref_string:
        fault = page not in frames
        evicted = None

        if fault:
            faults += 1
            if None in frames:
                idx = frames.index(None)
                frames[idx] = page
            else:
                lru_page = recency[0]
                idx = frames.index(lru_page)
                evicted = lru_page
                frames[idx] = page
                recency.pop(0)
        else:
            recency.remove(page)

        recency.append(page)

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
