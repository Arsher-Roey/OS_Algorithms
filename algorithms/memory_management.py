from __future__ import annotations

from math import ceil
from typing import Any


def _clone_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [block.copy() for block in blocks]


def simulate_mft(partitions: list[int], jobs: list[dict[str, Any]], policy: str) -> dict[str, Any]:
    """Simulate fixed-partition allocation.

    Policies are interpreted to match the classroom distinction:
    - Best Fit: a job targets the globally smallest partition that can hold it; if that
      exact best partition is occupied, the job waits.
    - First Fit: a job takes the first free partition that can hold it.
    - Best Available Fit: a job takes the smallest currently free partition that can hold it.
    """
    fixed = [
        {"index": idx + 1, "size": int(size), "job": None, "fragment": 0}
        for idx, size in enumerate(partitions)
        if int(size) > 0
    ]
    steps: list[str] = []
    waiting: list[dict[str, Any]] = []

    for job in jobs:
        name = str(job["name"])
        size = int(job["size"])
        steps.append(f"Checking {name} ({size}K).")

        target = None
        reason = ""

        if policy == "Best Fit":
            candidates = [p for p in fixed if p["size"] >= size]
            if not candidates:
                reason = f"No partition is large enough for {name}."
            else:
                best_size = min(p["size"] for p in candidates)
                best_partitions = [p for p in fixed if p["size"] == best_size and p["size"] >= size]
                free_best = [p for p in best_partitions if p["job"] is None]
                if free_best:
                    target = sorted(free_best, key=lambda p: p["index"])[0]
                    reason = f"Best Fit selects Partition {target['index']} ({target['size']}K), the smallest partition that can hold {name}."
                else:
                    reason = f"The best-sized partition for {name} is {best_size}K, but it is occupied, so {name} waits."

        elif policy == "First Fit":
            for part in fixed:
                if part["job"] is None and part["size"] >= size:
                    target = part
                    reason = f"First Fit selects Partition {part['index']} because it is the first free partition large enough."
                    break
            if target is None:
                reason = f"No free partition can currently hold {name}."

        else:  # Best Available Fit
            free_candidates = [p for p in fixed if p["job"] is None and p["size"] >= size]
            if free_candidates:
                target = sorted(free_candidates, key=lambda p: (p["size"], p["index"]))[0]
                reason = f"Best Available Fit selects Partition {target['index']} ({target['size']}K), the smallest free partition that can hold {name}."
            else:
                reason = f"No available free partition can hold {name}."

        if target is None:
            waiting.append(job.copy())
            steps.append(f"→ {reason}")
        else:
            target["job"] = {"name": name, "size": size}
            target["fragment"] = target["size"] - size
            steps.append(f"→ {reason} Internal fragmentation = {target['size']}K - {size}K = {target['fragment']}K.")

    total_internal = sum(int(part["fragment"] or 0) for part in fixed if part["job"] is not None)
    return {
        "policy": policy,
        "partitions": fixed,
        "waiting": waiting,
        "steps": steps,
        "total_internal": total_internal,
    }


def _merge_holes(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocks = sorted(blocks, key=lambda b: b["start"])
    merged: list[dict[str, Any]] = []
    for block in blocks:
        if merged and merged[-1]["type"] == "hole" and block["type"] == "hole":
            merged[-1]["size"] += block["size"]
        else:
            merged.append(block.copy())
    # Recompute 
    pos = 0
    for block in merged:
        block["start"] = pos
        pos += block["size"]
    return merged


def _allocate_mvt(blocks: list[dict[str, Any]], job: dict[str, Any], policy: str) -> tuple[list[dict[str, Any]], bool, str]:
    size = int(job["size"])
    name = str(job["name"])
    holes = [block for block in blocks if block["type"] == "hole" and block["size"] >= size]
    if not holes:
        total_free = sum(block["size"] for block in blocks if block["type"] == "hole")
        if total_free >= size:
            return blocks, False, f"{name} needs {size}K. Total free memory is {total_free}K, but no single hole is large enough. External fragmentation detected."
        return blocks, False, f"{name} needs {size}K, but only {total_free}K free memory is available."

    if policy == "First Fit":
        target = holes[0]
    elif policy == "Best Fit":
        target = min(holes, key=lambda h: (h["size"], h["start"]))
    else:  # Worst Fit
        target = max(holes, key=lambda h: (h["size"], -h["start"]))

    new_blocks: list[dict[str, Any]] = []
    for block in blocks:
        if block is target:
            new_blocks.append({
                "type": "job",
                "name": name,
                "size": size,
                "start": block["start"],
            })
            remaining = block["size"] - size
            if remaining > 0:
                new_blocks.append({
                    "type": "hole",
                    "name": "Free",
                    "size": remaining,
                    "start": block["start"] + size,
                })
        else:
            new_blocks.append(block.copy())

    new_blocks = _merge_holes(new_blocks)
    return new_blocks, True, f"{policy} places {name} ({size}K) into the hole starting at {target['start']}K with size {target['size']}K."


def _release_mvt(blocks: list[dict[str, Any]], names: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    released: list[str] = []
    wanted = {n.strip().upper() for n in names if n.strip()}
    new_blocks: list[dict[str, Any]] = []
    for block in blocks:
        if block["type"] == "job" and str(block.get("name", "")).upper() in wanted:
            released.append(str(block["name"]))
            new_blocks.append({
                "type": "hole",
                "name": "Free",
                "size": block["size"],
                "start": block["start"],
            })
        else:
            new_blocks.append(block.copy())
    return _merge_holes(new_blocks), released


def _compact_mvt(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compacted: list[dict[str, Any]] = []
    pos = 0
    for block in blocks:
        if block["type"] == "os":
            compacted.append({**block, "start": pos})
            pos += block["size"]
    for block in blocks:
        if block["type"] == "job":
            compacted.append({**block, "start": pos})
            pos += block["size"]
    total = sum(block["size"] for block in blocks)
    remaining = total - pos
    if remaining > 0:
        compacted.append({"type": "hole", "name": "Free", "size": remaining, "start": pos})
    return compacted


def _hole_count(blocks: list[dict[str, Any]]) -> int:
    return sum(1 for block in blocks if block["type"] == "hole")


def simulate_mvt(
    total_memory: int,
    os_size: int,
    initial_jobs: list[dict[str, Any]],
    release_jobs: list[str],
    incoming_jobs: list[dict[str, Any]],
    policy: str,
    compaction: bool,
) -> dict[str, Any]:
    total_memory = int(total_memory)
    os_size = int(os_size)
    if total_memory <= os_size:
        raise ValueError("Total memory must be larger than the OS size.")

    blocks: list[dict[str, Any]] = [
        {"type": "os", "name": "OS", "size": os_size, "start": 0},
        {"type": "hole", "name": "Free", "size": total_memory - os_size, "start": os_size},
    ]
    steps: list[str] = [f"Memory starts with OS = {os_size}K and one free hole = {total_memory - os_size}K."]
    stages: list[dict[str, Any]] = [{"label": "Initial Memory", "blocks": _clone_blocks(blocks)}]
    waiting: list[dict[str, Any]] = []
    incoming_status: list[dict[str, Any]] = []
    release_status: list[dict[str, Any]] = []
    compaction_used = False

    # 1) Load the initial jobs in the selected policy order.
    for job in initial_jobs:
        blocks, ok, message = _allocate_mvt(blocks, job, policy)
        steps.append(message)
        if not ok:
            waiting_job = job.copy()
            waiting_job["phase"] = "initial"
            waiting.append(waiting_job)
    stages.append({"label": "After Initial Allocation", "blocks": _clone_blocks(blocks)})

    # 2) Release jobs to create holes. Report invalid release names instead of failing silently.
    if release_jobs:
        before_names = {str(b.get("name", "")).upper() for b in blocks if b["type"] == "job"}
        blocks, released = _release_mvt(blocks, release_jobs)
        released_set = {name.upper() for name in released}
        for name in release_jobs:
            clean = name.strip()
            if not clean:
                continue
            release_status.append({"name": clean, "released": clean.upper() in released_set})
        missing = [item["name"] for item in release_status if not item["released"]]
        if released:
            msg = "Released jobs: " + ", ".join(released) + ". Adjacent holes are merged."
            if missing:
                msg += " Not found: " + ", ".join(missing) + "."
            steps.append(msg)
        else:
            steps.append("No matching jobs were released." + (" Not found: " + ", ".join(missing) + "." if missing else ""))
        stages.append({"label": "After Release / Fragmented Memory", "blocks": _clone_blocks(blocks)})

    # 3) In With Compaction mode, compaction is a real separate visual process.
    #    It happens after releases whenever scattered holes exist, not only after an incoming failure.
    if compaction and _hole_count(blocks) > 1:
        stages.append({"label": "Before Compaction", "blocks": _clone_blocks(blocks)})
        total_free_before = sum(block["size"] for block in blocks if block["type"] == "hole")
        blocks = _compact_mvt(blocks)
        compaction_used = True
        steps.append(
            f"Compaction moves allocated jobs together and merges scattered free spaces into one {total_free_before}K hole."
        )
        stages.append({"label": "After Compaction", "blocks": _clone_blocks(blocks)})

    # 4) Allocate incoming jobs. If compaction was not yet used and a fragmented failure occurs,
    #    compact on demand and retry.
    for job in incoming_jobs:
        blocks, ok, message = _allocate_mvt(blocks, job, policy)
        steps.append(message)
        status = {"name": str(job["name"]), "size": int(job["size"]), "status": "Allocated" if ok else "Waiting"}
        if not ok and compaction:
            total_free = sum(block["size"] for block in blocks if block["type"] == "hole")
            if total_free >= int(job["size"]) and _hole_count(blocks) > 1:
                stages.append({"label": f"Before Compaction for {job['name']}", "blocks": _clone_blocks(blocks)})
                blocks = _compact_mvt(blocks)
                compaction_used = True
                steps.append(f"Compaction merges free space into one {total_free}K hole, then retries {job['name']}.")
                stages.append({"label": "After Compaction", "blocks": _clone_blocks(blocks)})
                blocks, ok, message = _allocate_mvt(blocks, job, policy)
                steps.append("Retry after compaction: " + message)
                status["status"] = "Allocated after compaction" if ok else "Waiting"
        if not ok:
            waiting_job = job.copy()
            waiting_job["phase"] = "incoming"
            waiting.append(waiting_job)
        incoming_status.append(status)

    stages.append({"label": "Final Memory Map", "blocks": _clone_blocks(blocks)})
    free_total = sum(block["size"] for block in blocks if block["type"] == "hole")
    largest_hole = max([block["size"] for block in blocks if block["type"] == "hole"] or [0])
    external_frag = max(0, free_total - largest_hole)

    return {
        "policy": policy,
        "compaction": compaction,
        "compaction_used": compaction_used,
        "blocks": blocks,
        "stages": stages,
        "waiting": waiting,
        "incoming_status": incoming_status,
        "release_status": release_status,
        "steps": steps,
        "free_total": free_total,
        "largest_hole": largest_hole,
        "external_fragmentation": external_frag,
    }

def simulate_paging(total_memory: int, os_size: int, page_size: int, job_size: int, logical_address: int) -> dict[str, Any]:
    total_memory = int(total_memory)
    os_size = int(os_size)
    page_size = int(page_size)
    job_size = int(job_size)
    logical_address = int(logical_address)
    if page_size <= 0:
        raise ValueError("Page size must be greater than zero.")
    if total_memory <= 0 or job_size <= 0:
        raise ValueError("Memory and job size must be greater than zero.")

    total_frames = total_memory // page_size
    os_frames = ceil(os_size / page_size)
    if os_frames >= total_frames:
        raise ValueError("The OS occupies all available frames.")

    pages_needed = ceil(job_size / page_size)
    free_frames = list(range(os_frames, total_frames))
    if pages_needed > len(free_frames):
        raise ValueError("There are not enough frames for this job.")

    # Assign non-contiguously when possible so the visual clearly shows paging.
    even = free_frames[::2]
    odd = free_frames[1::2]
    frame_order = even + odd
    assigned = frame_order[:pages_needed]
    page_table = {page: assigned[page] for page in range(pages_needed)}

    internal_fragmentation = pages_needed * page_size - job_size
    address_valid = 0 <= logical_address < job_size
    address_result: dict[str, Any] | None = None
    steps: list[str] = [
        f"Total frames = {total_memory}K / {page_size}K = {total_frames} frames.",
        f"OS occupies ceil({os_size}K / {page_size}K) = {os_frames} frame(s).",
        f"Job needs ceil({job_size}K / {page_size}K) = {pages_needed} page(s).",
        f"Internal fragmentation = allocated {pages_needed * page_size}K - job {job_size}K = {internal_fragmentation}K.",
    ]

    if address_valid:
        p = logical_address // page_size
        d = logical_address % page_size
        f = page_table[p]
        pa = f * page_size + d
        address_result = {"p": p, "d": d, "f": f, "pa": pa}
        steps.extend([
            f"Logical Address {logical_address}K: p = LA / page size = {logical_address} / {page_size} = {p}.",
            f"Offset d = LA % page size = {logical_address} % {page_size} = {d}.",
            f"Page table maps page {p} to frame {f}.",
            f"Physical Address = frame × page size + offset = {f} × {page_size} + {d} = {pa}K.",
        ])
    else:
        steps.append(f"Logical Address {logical_address}K is outside the job address space 0 to {job_size - 1}K.")

    frames: list[dict[str, Any]] = []
    assigned_reverse = {frame: page for page, frame in page_table.items()}
    for frame in range(total_frames):
        if frame < os_frames:
            frames.append({"frame": frame, "type": "os", "label": "OS"})
        elif frame in assigned_reverse:
            frames.append({"frame": frame, "type": "page", "label": f"P{assigned_reverse[frame]}", "page": assigned_reverse[frame]})
        else:
            frames.append({"frame": frame, "type": "free", "label": "Free"})

    return {
        "total_frames": total_frames,
        "os_frames": os_frames,
        "pages_needed": pages_needed,
        "page_size": page_size,
        "job_size": job_size,
        "logical_address": logical_address,
        "internal_fragmentation": internal_fragmentation,
        "page_table": page_table,
        "frames": frames,
        "address_valid": address_valid,
        "address_result": address_result,
        "steps": steps,
    }
