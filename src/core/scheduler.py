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
    waiting_times: Dict[str, int]     # {pid: tiempo de espera total}
    completion_times: Dict[str, int]   # {pid: tiempo de finalización}

def run_scheduling(
    processes: List[Any],
    algorithm: str,
    quantum: int = None
) -> ScheduleResult:
    """
    Llama al algoritmo indicado y empaqueta timeline, waiting_times y completion_times.
    """
    alg = algorithm.lower()
    if alg == 'fifo':
        res = fifo_schedule(processes)
    elif alg == 'sjf':
        res = sjf_schedule(processes)
    elif alg == 'srt':
        res = srt_schedule(processes)
    elif alg == 'rr':
        if quantum is None:
            raise ValueError("RR requiere quantum")
        res = rr_schedule(processes, quantum=quantum)
    elif alg == 'priority':
        res = priority_schedule(processes)
    else:
        raise ValueError(f"Algoritmo desconocido: {algorithm}")

    # timeline y waiting_times tal como los devuelve tu algoritmo
    timeline = res.timeline
    waiting_times = getattr(res, 'waiting_times', {})

    # Construir completion_times: el instante de finalización más alto de cada pid
    completion_times: Dict[str, int] = {}
    for pid, start, end in timeline:
        prev = completion_times.get(pid, 0)
        completion_times[pid] = max(prev, end)

    return ScheduleResult(
        timeline=timeline,
        waiting_times=waiting_times,
        completion_times=completion_times
    )