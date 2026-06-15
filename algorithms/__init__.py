from algorithms import fifo, optimal, lru, lru_approximation, counting_based

REGISTRY: dict = {
    "FIFO (First-In First-Out)":      fifo,
    "Optimal":                         optimal,
    "LRU (Least Recently Used)":       lru,
    "LRU Approximation":               lru_approximation,
    "Counting-Based Page Replacement": counting_based,
}

DEADLOCK_REGISTRY: dict = {
    "Banker's Algorithm":              deadlock.bankers_safe_state,
}

MEMORY_MANAGEMENT_REGISTRY: dict = {
    "MFT (Memory First-Fit)":           memory_management,
    "MVT (Memory Variable-Partitioning)": memory_management,
}

CPU_SCHEDULING_REGISTRY: dict = {
    "FCFS (First Come First Served)":   cpu_scheduling,
    "SJF (Shortest Job First)":         cpu_scheduling,
    "Priority Scheduling":               cpu_scheduling,
    "Round Robin (RR)":                  cpu_scheduling,
}

