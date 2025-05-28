from typing import List
from data_io.process_loader import Process

class ScheduleResult:
    """
    Resultado de un scheduling:
      - timeline: lista de tuplas (pid, start_cycle, end_cycle)
      - waiting_times: dict {pid: waiting_time}
    """
    def __init__(self, timeline, waiting_times):
        self.timeline = timeline
        self.waiting_times = waiting_times


def schedule(processes: List[Process], **kwargs) -> ScheduleResult:
    """
    First-In-First-Out scheduling. Ejecuta los procesos en orden de llegada.
    """
    # Ordenar por arrival_time
    procs = sorted(processes, key=lambda p: p.arrival_time)
    timeline = []         # [(pid, start, end), ...]
    waiting_times = {}    # {pid: waiting_time}
    current_time = 0

    for p in procs:
        # Si la CPU está ocupada hasta la llegada del proceso
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        start = current_time
        end = start + p.burst_time
        # Registrar en timeline
        timeline.append((p.pid, start, end))
        # Tiempo de espera: desde arrival hasta inicio
        waiting_times[p.pid] = start - p.arrival_time
        # Avanzar el reloj
        current_time = end

    return ScheduleResult(timeline, waiting_times)
