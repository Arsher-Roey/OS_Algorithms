def run(
    ref_string: list[int],
    frame_count: int,
    mode: str = "LFU",
) -> tuple[list[dict], int]:
    frames: list[int | None] = [None] * frame_count
    counts: list[int] = [0] * frame_count
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
                counts[idx] = 1
            else:
                if mode == "MFU":
                    target_count = max(counts)
                else:
                    target_count = min(counts)

                idx = counts.index(target_count)
                evicted = frames[idx]
                frames[idx] = page
                counts[idx] = 1
        else:
            idx = frames.index(page)
            counts[idx] += 1

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
