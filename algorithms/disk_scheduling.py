def fcfs(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    order = []
    current = head
    total = 0

    for track in requests:
        total += abs(track - current)
        current = track
        order.append(str(track))

    return order, total


def sstf(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    remaining = list(requests)
    order = []
    current = head
    total = 0

    while remaining:
        closest = min(remaining, key=lambda t: abs(t - current))
        total += abs(closest - current)
        current = closest
        order.append(str(closest))
        remaining.remove(closest)

    return order, total


def scan(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    lower  = sorted([r for r in requests if r < head], reverse=True)
    higher = sorted([r for r in requests if r >= head])

    order = []
    current = head
    total = 0

    if direction == "up":
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track))
        for track in lower:
            total += abs(track - current)
            current = track
            order.append(str(track))
    else:
        for track in lower:
            total += abs(track - current)
            current = track
            order.append(str(track))
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track))

    return order, total


def cscan(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    lower  = sorted([r for r in requests if r < head])
    higher = sorted([r for r in requests if r >= head])

    order = []
    current = head
    total = 0

    if direction == "up":
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track) + "+")

        if lower:
            total += current
            total += lower[-1]
            current = 0
            for track in lower:
                order.append(str(track) + "+")
            current = lower[-1]

    else:
        lower_desc = sorted([r for r in requests if r <= head], reverse=True)
        higher_asc = sorted([r for r in requests if r > head], reverse=True)

        for track in lower_desc:
            total += abs(track - current)
            current = track
            order.append(str(track) + "+")

        if higher_asc:
            total += abs(current - (disk_size - 1))
            total += abs((disk_size - 1) - higher_asc[-1])
            current = disk_size - 1
            for track in higher_asc:
                order.append(str(track) + "+")
            current = higher_asc[-1]

    return order, str(total) + "+"


def look(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    lower  = sorted([r for r in requests if r < head], reverse=True)
    higher = sorted([r for r in requests if r >= head])

    order = []
    current = head
    total = 0

    if direction == "up":
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track))
        for track in lower:
            total += abs(track - current)
            current = track
            order.append(str(track))
    else:
        for track in lower:
            total += abs(track - current)
            current = track
            order.append(str(track))
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track))

    return order, total


def clook(requests: list[int], head: int, disk_size: int = 200, direction: str = "up"):
    lower  = sorted([r for r in requests if r < head])
    higher = sorted([r for r in requests if r >= head])

    order = []
    current = head
    total = 0

    if direction == "up":
        for track in higher:
            total += abs(track - current)
            current = track
            order.append(str(track))
        if lower:
            total += abs(current - lower[0])
            current = lower[0]
            for track in lower:
                total += abs(track - current)
                current = track
                order.append(str(track))
    else:
        lower_desc  = sorted([r for r in requests if r <= head], reverse=True)
        higher_desc = sorted([r for r in requests if r > head], reverse=True)

        for track in lower_desc:
            total += abs(track - current)
            current = track
            order.append(str(track))
        if higher_desc:
            total += abs(current - higher_desc[0])
            current = higher_desc[0]
            for track in higher_desc:
                total += abs(track - current)
                current = track
                order.append(str(track))

    return order, total


DIRECTION_ALGORITHMS = {"Scan", "C-Scan", "Look", "C-Look"}

DISK_REGISTRY = {
    "First Come, First-Served":   fcfs,
    "Shortest Seek Time First":   sstf,
    "Scan":                       scan,
    "C-Scan":                     cscan,
    "Look":                       look,
    "C-Look":                     clook,
}