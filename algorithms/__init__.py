from algorithms import fifo, optimal, lru, lru_approximation, counting_based

REGISTRY: dict = {
    "FIFO (First-In First-Out)":      fifo,
    "Optimal":                         optimal,
    "LRU (Least Recently Used)":       lru,
    "LRU Approximation":               lru_approximation,
    "Counting-Based Page Replacement": counting_based,
}
