from typing import List
from data_io.process_loader import Process
from scheduling.fifo import ScheduleResult


def schedule(processes: List[Process], **kwargs) -> ScheduleResult:
    """
    Shortest Job First (no-preemptivo). En cada punto, elige el proceso con menor burst_time
    entre los que ya han llegado.
    """
    # Copia de lista para no modificar original
    procs = sorted(processes, key=lambda p: p.arrival_time)
    timeline = []
    waiting_times = {}
    current_time = 0
    ready_queue: List[Process] = []
    i = 0  # índice de llegada
    n = len(procs)

    while i < n or ready_queue:
        # Añadir a ready_queue todos los procesos que han llegado
        while i < n and procs[i].arrival_time <= current_time:
            ready_queue.append(procs[i])
            i += 1
        if not ready_queue:
            # Si no hay listos, adelantar al próximo arrival
            current_time = procs[i].arrival_time
            continue
        # Seleccionar el de burst más corto
        ready_queue.sort(key=lambda p: p.burst_time)
        p = ready_queue.pop(0)
        start = current_time
        end = start + p.burst_time
        timeline.append((p.pid, start, end))
        waiting_times[p.pid] = start - p.arrival_time
        current_time = end
    return ScheduleResult(timeline, waiting_times)
