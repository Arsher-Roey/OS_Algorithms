def run(ref_string: list[int], frame_count: int) -> tuple[list[dict], int]:
    frames: list[int | None] = [None] * frame_count
    ref_bits: list[int] = [0] * frame_count
    hand: int = 0
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
                ref_bits[idx] = 1
            else:
                while True:
                    if ref_bits[hand] == 0:
                        evicted = frames[hand]
                        frames[hand] = page
                        ref_bits[hand] = 1
                        hand = (hand + 1) % frame_count
                        break
                    else:
                        ref_bits[hand] = 0
                        hand = (hand + 1) % frame_count
        else:
            idx = frames.index(page)
            ref_bits[idx] = 1

        steps.append({
            "page":    page,
            "frames":  list(frames),
            "fault":   fault,
            "evicted": evicted,
        })

    return steps, faults
