from typing import Dict

def compute_avg_waiting_time(waiting_times: Dict[str, int]) -> float:
    """
    Calcula el Average Waiting Time (AWT) dado un dict {pid: waiting_time}.
    """
    if not waiting_times:
        return 0.0
    total = sum(waiting_times.values())
    count = len(waiting_times)
    return total / count


def compute_total_waits(waiting_counts: Dict[str, int]) -> int:
    """
    Suma el total de veces que cualquier proceso ha tenido que esperar.
    """
    return sum(waiting_counts.values())


def compute_waiting_rate(waiting_counts: Dict[str, int], total_cycles: int) -> float:
    """
    Calcula la proporción de ciclos de espera vs ciclos totales.
    """
    if total_cycles <= 0:
        return 0.0
    total_waits = sum(waiting_counts.values())
    return total_waits / total_cycles


def compute_throughput(completions: Dict[str, int], total_time: int) -> float:
    """
    Throughput = #procesos completados / total_time

    completions: dict de pid a ciclo de finalización
    total_time: número total de ciclos (si <= 0, se calcula como max(cycle)+1)
    """
    if not completions:
        return 0.0

    # Si el caller no proporcionó un total_time válido, lo inferimos
    if total_time <= 0:
        total_time = max(completions.values()) + 1

    return len(completions) / total_time


def compute_avg_turnaround_time(
    completion_times: Dict[str, int],
    arrival_times: Dict[str, int]
) -> float:
    """
    Calcula el Average Turnaround Time (TAT) dado:
      - completion_times: {pid: ciclo de finalización}
      - arrival_times:    {pid: ciclo de llegada}

    TAT_i = finish_i – arrival_i
    Se devuelve el promedio sobre todos los procesos.
    """
    if not completion_times:
        return 0.0

    total = 0
    for pid, finish in completion_times.items():
        at = arrival_times.get(pid, 0)
        total += (finish - at)

    return total / len(completion_times)
