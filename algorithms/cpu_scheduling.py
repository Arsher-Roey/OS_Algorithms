from typing import List, Dict, Tuple


def _format_metrics(avg_wait: float, avg_turn: float, cpu_util: float) -> Tuple[str, str, str]:
    return (f"{avg_wait:.1f} ms", f"{avg_turn:.1f} ms", f"{cpu_util:.0f}%")


def _fcfs(processes: List[Dict]) -> Tuple[str, str, str, List[Dict]]:
    procs = sorted([p.copy() for p in processes], key=lambda p: p["arrival"])
    time = 0
    total_wait = 0
    total_turn = 0
    total_burst = 0
    timeline: List[Dict] = []

    for p in procs:
        arrival = p["arrival"]
        burst = p["burst"]
        start = max(time, arrival)
        wait = start - arrival
        finish = start + burst
        turn = finish - arrival

        total_wait += wait
        total_turn += turn
        total_burst += burst

        timeline.append({"pid": p["pid"], "start": start, "finish": finish})

        time = finish

    n = len(procs) or 1
    avg_wait = total_wait / n
    avg_turn = total_turn / n
    span = time - min((p["arrival"] for p in procs), default=0)
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def _sjf_nonpreemptive(processes: List[Dict]) -> Tuple[str, str, str, List[Dict]]:
    procs = [p.copy() for p in processes]
    procs.sort(key=lambda p: (p["arrival"], p["burst"]))

    time = 0
    completed = 0
    n = len(procs) or 1
    total_wait = 0
    total_turn = 0
    total_burst = 0

    ready: List[Dict] = []
    timeline: List[Dict] = []

    while completed < len(processes):
        # enqueue arrived
        for p in procs:
            if p.get("_enqueued"):
                continue
            if p["arrival"] <= time:
                ready.append(p)
                p["_enqueued"] = True

        if not ready:
            # jump to next arrival
            next_arrival = min(p["arrival"] for p in procs if not p.get("_enqueued"))
            time = max(time, next_arrival)
            continue

        # pick shortest burst
        ready.sort(key=lambda x: x["burst"]) 
        p = ready.pop(0)
        start = max(time, p["arrival"])
        wait = start - p["arrival"]
        finish = start + p["burst"]
        turn = finish - p["arrival"]

        total_wait += wait
        total_turn += turn
        total_burst += p["burst"]

        timeline.append({"pid": p["pid"], "start": start, "finish": finish})

        time = finish
        completed += 1

    avg_wait = total_wait / n
    avg_turn = total_turn / n
    span = time - min((p["arrival"] for p in procs), default=0)
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def _sjf_preemptive(processes: List[Dict]) -> Tuple[str, str, str, List[Dict]]:
    procs = [dict(p.copy(), _idx=i) for i, p in enumerate(processes)]
    procs.sort(key=lambda p: (p["arrival"], p["_idx"]))

    n = len(procs) or 1
    rem = {p["pid"]: p["burst"] for p in procs}
    time = 0
    total_burst = sum(p["burst"] for p in procs)
    timeline: List[Dict] = []
    last_active = {p["pid"]: None for p in procs}
    total_wait = {p["pid"]: 0 for p in procs}
    completion = {}

    arrived = set()
    i = 0
    while any(v > 0 for v in rem.values()):
        # enqueue newly arrived
        while i < len(procs) and procs[i]["arrival"] <= time:
            arrived.add(procs[i]["pid"])
            i += 1

        # pick ready process with smallest remaining time
        ready = [p for p in procs if p["pid"] in arrived and rem[p["pid"]] > 0]
        if not ready:
            # jump to next arrival
            if i < len(procs):
                time = procs[i]["arrival"]
                continue
            break

        ready.sort(key=lambda x: (rem[x["pid"]], x["_idx"]))
        cur = ready[0]
        pid = cur["pid"]

        # determine next event: either this process finishes, or a new arrival occurs
        next_arrival = procs[i]["arrival"] if i < len(procs) else None
        run_until = time + rem[pid]
        if next_arrival is not None and next_arrival < run_until:
            # run until next arrival
            slice_time = next_arrival - time
        else:
            slice_time = rem[pid]

        slice_start = time
        slice_end = time + slice_time
        rem[pid] -= slice_time
        time = slice_end

        # account waiting time
        if last_active[pid] is None:
            total_wait[pid] += max(0, slice_start - cur["arrival"])
        else:
            total_wait[pid] += max(0, slice_start - last_active[pid])
        last_active[pid] = time

        timeline.append({"pid": pid, "start": slice_start, "finish": slice_end})

        if rem[pid] == 0:
            completion[pid] = time

    total_wait_sum = sum(total_wait.values())
    total_turn_sum = sum((completion[pid] - next(p["arrival"] for p in procs if p["pid"] == pid)) for pid in completion)
    avg_wait = total_wait_sum / n
    avg_turn = total_turn_sum / n
    span = max(completion.values()) - min(p["arrival"] for p in procs) if completion else 0
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def _priority_preemptive(processes: List[Dict]) -> Tuple[str, str, str, List[Dict]]:
    procs = [dict(p.copy(), _idx=i) for i, p in enumerate(processes)]
    procs.sort(key=lambda p: (p["arrival"], p["_idx"]))

    n = len(procs) or 1
    rem = {p["pid"]: p["burst"] for p in procs}
    time = 0
    total_burst = sum(p["burst"] for p in procs)
    timeline: List[Dict] = []
    last_active = {p["pid"]: None for p in procs}
    total_wait = {p["pid"]: 0 for p in procs}
    completion = {}

    arrived = set()
    i = 0
    while any(v > 0 for v in rem.values()):
        while i < len(procs) and procs[i]["arrival"] <= time:
            arrived.add(procs[i]["pid"])
            i += 1

        ready = [p for p in procs if p["pid"] in arrived and rem[p["pid"]] > 0]
        if not ready:
            if i < len(procs):
                time = procs[i]["arrival"]
                continue
            break

        # pick highest priority (lowest numeric value), tie-breaker by arrival/_idx
        ready.sort(key=lambda x: (x.get("priority", 0), x["_idx"]))
        cur = ready[0]
        pid = cur["pid"]

        next_arrival = procs[i]["arrival"] if i < len(procs) else None
        run_until = time + rem[pid]
        if next_arrival is not None and next_arrival < run_until:
            slice_time = next_arrival - time
        else:
            slice_time = rem[pid]

        slice_start = time
        slice_end = time + slice_time
        rem[pid] -= slice_time
        time = slice_end

        if last_active[pid] is None:
            total_wait[pid] += max(0, slice_start - cur["arrival"])
        else:
            total_wait[pid] += max(0, slice_start - last_active[pid])
        last_active[pid] = time

        timeline.append({"pid": pid, "start": slice_start, "finish": slice_end})

        if rem[pid] == 0:
            completion[pid] = time

    total_wait_sum = sum(total_wait.values())
    total_turn_sum = sum((completion[pid] - next(p["arrival"] for p in procs if p["pid"] == pid)) for pid in completion)
    avg_wait = total_wait_sum / n
    avg_turn = total_turn_sum / n
    span = max(completion.values()) - min(p["arrival"] for p in procs) if completion else 0
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def _round_robin(processes: List[Dict], quantum: int) -> Tuple[str, str, str, List[Dict]]:
    # make copies and keep original order index to ensure FIFO tie-breaking
    procs = [dict(p.copy(), _idx=i) for i, p in enumerate(processes)]
    procs.sort(key=lambda p: (p["arrival"], p["_idx"]))
    n = len(procs) or 1
    rem = {p["pid"]: p["burst"] for p in procs}
    time = 0
    queue: List[Dict] = []
    total_wait = {p["pid"]: 0 for p in procs}
    last_active = {p["pid"]: None for p in procs}
    completion = {}
    total_burst = sum(p["burst"] for p in procs)

    timeline: List[Dict] = []

    while True:
        # enqueue arrivals in arrival order (stable by original input order)
        for p in procs:
            if p not in queue and p["arrival"] <= time and rem[p["pid"]] > 0:
                queue.append(p)

        if not queue:
            # if all done break
            if all(v == 0 for v in rem.values()):
                break
            # jump to next arrival
            next_arrivals = [p["arrival"] for p in procs if rem[p["pid"]] > 0 and p["arrival"] > time]
            if next_arrivals:
                time = min(next_arrivals)
                continue
            break

        p = queue.pop(0)
        pid = p["pid"]
        if last_active[pid] is None:
            total_wait[pid] += max(0, time - p["arrival"])
        else:
            total_wait[pid] += max(0, time - last_active[pid])

        slice_time = min(quantum, rem[pid])
        rem[pid] -= slice_time
        slice_start = time
        time += slice_time
        slice_end = time
        last_active[pid] = time

        # record this execution slice for the Gantt timeline
        timeline.append({"pid": pid, "start": slice_start, "finish": slice_end})

        # enqueue new arrivals that came during this quantum (preserve arrival/_idx order)
        for q in procs:
            if q not in queue and q["arrival"] <= time and rem[q["pid"]] > 0 and q != p:
                queue.append(q)

        if rem[pid] > 0:
            queue.append(p)
        else:
            completion[pid] = time

    total_wait_sum = sum(total_wait.values())
    total_turn_sum = sum((completion[pid] - next(p["arrival"] for p in procs if p["pid"] == pid)) for pid in completion)
    avg_wait = total_wait_sum / n
    avg_turn = total_turn_sum / n
    span = max(completion.values()) - min(p["arrival"] for p in procs) if completion else 0
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def _priority_nonpreemptive(processes: List[Dict]) -> Tuple[str, str, str, List[Dict]]:
    procs = [p.copy() for p in processes]
    time = 0
    ready: List[Dict] = []
    completed = 0
    total_wait = 0
    total_turn = 0
    total_burst = 0
    timeline: List[Dict] = []

    while completed < len(procs):
        for p in procs:
            if p.get("_enqueued"):
                continue
            if p["arrival"] <= time:
                ready.append(p)
                p["_enqueued"] = True

        if not ready:
            time = min(p["arrival"] for p in procs if not p.get("_enqueued"))
            continue

        ready.sort(key=lambda x: x.get("priority", 0))
        p = ready.pop(0)
        start = max(time, p["arrival"])
        wait = start - p["arrival"]
        finish = start + p["burst"]
        turn = finish - p["arrival"]

        total_wait += wait
        total_turn += turn
        total_burst += p["burst"]

        timeline.append({"pid": p["pid"], "start": start, "finish": finish})
        time = finish
        completed += 1

    n = len(procs) or 1
    avg_wait = total_wait / n
    avg_turn = total_turn / n
    span = time - min((p["arrival"] for p in procs), default=0)
    cpu_util = (total_burst / span * 100) if span > 0 else 100.0

    return _format_metrics(avg_wait, avg_turn, cpu_util) + (timeline,)


def run(algo: str, processes: List[Dict], time_quantum: int = 2):
    
    if algo == "First Come First Served (FCFS)":
        return _fcfs(processes)
    if algo == "Shortest Job First (SJF)":
        return _sjf_nonpreemptive(processes)
    if algo in ("Shortest Job First (SJF) - Preemptive", "Shortest Job First (SJF) Preemptive", "SRTF"):
        return _sjf_preemptive(processes)
    if algo == "Round Robin (RR)":
        return _round_robin(processes, time_quantum)
    if algo == "Priority Scheduling":
        return _priority_nonpreemptive(processes)
    if algo in ("Priority Scheduling (Preemptive)", "Priority Scheduling - Preemptive"):
        return _priority_preemptive(processes)
    # fallback: FCFS
    return _fcfs(processes)
