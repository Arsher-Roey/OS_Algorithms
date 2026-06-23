from __future__ import annotations

from typing import Any

# COMPUTATION NG NEED
def compute_need(maximum: list[list[int]], allocation: list[list[int]]) -> list[list[int]]:
    return [
        [max(maximum[i][j] - allocation[i][j], 0) for j in range(len(maximum[i]))]
        for i in range(len(maximum))
    ]


def _validate_inputs(
    processes: list[str],
    resources: list[str],
    available: list[int],
    allocation: list[list[int]],
    maximum: list[list[int]],
) -> str | None:
    n = len(processes)
    m = len(resources)

    if n == 0:
        return "At least one process is required."
    if m == 0:
        return "At least one resource type is required."
    if len(available) != m:
        return f"Available vector must have {m} entries (one per resource type)."
    if len(allocation) != n or len(maximum) != n:
        return f"Allocation and Maximum matrices must have {n} rows (one per process)."
    for i, row in enumerate(allocation):
        if len(row) != m:
            return f"Allocation row for {processes[i]} must have {m} columns."
    for i, row in enumerate(maximum):
        if len(row) != m:
            return f"Maximum row for {processes[i]} must have {m} columns."

    for i in range(n):
        for j in range(m):
            if allocation[i][j] < 0 or maximum[i][j] < 0 or available[j] < 0:
                return "Resource counts cannot be negative."
            if allocation[i][j] > maximum[i][j]:
                return (
                    f"{processes[i]} cannot allocate more of {resources[j]} "
                    f"({allocation[i][j]}) than its maximum claim ({maximum[i][j]})."
                )

    return None

# BANKERS ALGORITHM
def bankers_safe_state(
    processes: list[str],
    resources: list[str],
    available: list[int],
    allocation: list[list[int]],
    maximum: list[list[int]],
) -> dict[str, Any]:
  # CHECK FOR SAFE STATE

    error = _validate_inputs(processes, resources, available, allocation, maximum)
    if error:
        return {
            "valid": False,
            "error": error,
            "safe": False,
            "safe_sequence": [],
            "steps": [f"Input error: {error}"],
            "work_trace": [],
            "need": [],
            "finish": [],
        }

    n = len(processes)
    m = len(resources)
    work = [int(v) for v in available]
    need = compute_need(maximum, allocation)
    finish = [False] * n
    steps: list[str] = []
    work_trace: list[dict[str, Any]] = []
    safe_sequence: list[str] = []

    steps.append("Initialize Work = Available and compute Need = Max - Allocation for each process.")
    steps.append(f"Work = [{', '.join(str(v) for v in work)}]")
    for i in range(n):
        need_str = ", ".join(f"{resources[j]}={need[i][j]}" for j in range(m))
        steps.append(f"Need({processes[i]}) = ({need_str})")

    iteration = 1
    while True:
        found = False
        for i in range(n):
            if finish[i]:
                continue
            if all(need[i][j] <= work[j] for j in range(m)):
                steps.append(
                    f"Step {iteration}: {processes[i]} can finish because "
                    f"Need({processes[i]}) <= Work."
                )
                release = ", ".join(
                    f"{resources[j]}+{allocation[i][j]}" for j in range(m)
                )
                steps.append(
                    f"  → Pretend {processes[i]} completes and releases "
                    f"Allocation({processes[i]}): {release}."
                )
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(processes[i])
                work_trace.append({
                    "process": processes[i],
                    "work": work.copy(),
                })
                steps.append(f"  → Work = [{', '.join(str(v) for v in work)}]")
                iteration += 1
                found = True
                break

        if not found:
            break

    safe = all(finish)
    if safe:
        steps.append(
            "All processes can finish in some order. "
            f"Safe sequence: {' → '.join(safe_sequence)}."
        )
    else:
        blocked = [processes[i] for i in range(n) if not finish[i]]
        steps.append(
            "No process can proceed with the remaining Work. "
            f"System is in an unsafe state. Blocked processes: {', '.join(blocked)}."
        )

    return {
        "valid": True,
        "error": None,
        "safe": safe,
        "safe_sequence": safe_sequence,
        "steps": steps,
        "work_trace": work_trace,
        "need": need,
        "finish": finish,
        "work_final": work,
        "processes": list(processes),
        "resources": list(resources),
        "available": [int(v) for v in available],
        "allocation": [row.copy() for row in allocation],
        "maximum": [row.copy() for row in maximum],
    }

# example ng bankers 
def sample_bankers_scenario() -> dict[str, Any]:
    
    return {
        "processes": ["P0", "P1", "P2", "P3", "P4"],
        "resources": ["A", "B", "C"],
        "available": [3, 3, 2],
        "allocation": [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ],
        "maximum": [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ],
    }
