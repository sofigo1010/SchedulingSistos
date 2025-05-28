from typing import List
from data_io.process_loader import Process
from scheduling.fifo import ScheduleResult


def schedule(processes: List[Process], **kwargs) -> ScheduleResult:
    """
    Round Robin scheduling (preemptivo).
    Requiere 'quantum' 
    """
    quantum = kwargs.get('quantum')
    if quantum is None or quantum <= 0:
        raise ValueError("Round Robin requiere un quantum positivo")

    # Ordenar procesos por llegada
    procs = sorted(processes, key=lambda p: p.arrival_time)
    n = len(procs)
    current_time = 0
    timeline = []  # [(pid, start, end), ...]

    # Registros
    remaining = {p.pid: p.burst_time for p in procs}
    arrival = {p.pid: p.arrival_time for p in procs}
    finish_times = {}

    ready_queue: List[Process] = []
    i = 0  # índice de llegada

    while i < n or ready_queue:
        # Añadir nuevos procesos llegados
        while i < n and procs[i].arrival_time <= current_time:
            ready_queue.append(procs[i])
            i += 1
        if not ready_queue:
            # CPU idle hasta siguiente llegada
            current_time = procs[i].arrival_time
            continue
        # Tomar siguiente proceso
        p = ready_queue.pop(0)
        start = current_time
        run = min(quantum, remaining[p.pid])
        end = start + run
        # Registrar ejecución
        timeline.append((p.pid, start, end))
        remaining[p.pid] -= run
        current_time = end
        # Incorporar procesos que llegaron durante este quantum
        while i < n and procs[i].arrival_time <= current_time:
            ready_queue.append(procs[i])
            i += 1
        # Si aún no termina, reencolarlo
        if remaining[p.pid] > 0:
            ready_queue.append(p)
        else:
            finish_times[p.pid] = current_time

    # Calcular tiempos de espera
    waiting_times = {}
    for p in procs:
        turnaround = finish_times[p.pid] - arrival[p.pid]
        waiting_times[p.pid] = turnaround - p.burst_time

    return ScheduleResult(timeline, waiting_times)
