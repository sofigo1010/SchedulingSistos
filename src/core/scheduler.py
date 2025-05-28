from dataclasses import dataclass
from typing import List, Dict, Any
from data_io.process_loader import Process
from scheduling.fifo import schedule as fifo_schedule, ScheduleResult as FIFOResult
from scheduling.sjf import schedule as sjf_schedule
from scheduling.srt import schedule as srt_schedule
from scheduling.rr import schedule as rr_schedule
from scheduling.priority import schedule as priority_schedule

@dataclass
class ScheduleResult:
    timeline: List[tuple]             # lista de (pid, start, end)
    waiting_times: Dict[str, int]     # tiempos de espera por pid
    completion_times: Dict[str, int]  # tiempo de finalización por pid


def run_scheduling(
    processes: List[Any],
    algorithm: str,
    quantum: int = None
) -> ScheduleResult:
    alg = algorithm.lower()
    if alg == 'fifo':
        # first in first out: el que llega primero sale primero
        res = fifo_schedule(processes)
    elif alg == 'sjf':
        # shortest job first: ejecuta primero el proceso con menor duración
        res = sjf_schedule(processes)
    elif alg == 'srt':
        # shortest remaining time: como SJF pero permite interrupción
        res = srt_schedule(processes)
    elif alg == 'rr':
        # round robin: usa quantum para rebanadas de tiempo
        if quantum is None:
            raise ValueError("RR requiere quantum")
        res = rr_schedule(processes, quantum=quantum)
    elif alg == 'priority':
        # priority: ejecuta primero procesos con mayor prioridad
        res = priority_schedule(processes)
    else:
        raise ValueError(f"Algoritmo desconocido: {algorithm}")

    # timeline y waiting_times del algoritmo
    timeline = res.timeline
    waiting_times = getattr(res, 'waiting_times', {})

    # calcular completion_times:
    # para cada pid, se toma el tiempo de fin más alto de su timeline
    completion_times: Dict[str, int] = {}
    for pid, start, end in timeline:
        prev = completion_times.get(pid, 0)
        completion_times[pid] = max(prev, end)  # así se guarda el momento en que acaba cada proceso

    # devuelve ScheduleResult con todos los datos
    return ScheduleResult(
        timeline=timeline,
        waiting_times=waiting_times,
        completion_times=completion_times
    )
