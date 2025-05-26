from typing import List, Dict, Any
from data_io.process_loader import Process
from scheduling.fifo import schedule as fifo_schedule, ScheduleResult as FIFOResult
from scheduling.sjf import schedule as sjf_schedule
from scheduling.srt import schedule as srt_schedule
from scheduling.rr import schedule as rr_schedule
from scheduling.priority import schedule as priority_schedule


def run_scheduling(processes: List[Process], algorithm: str, **kwargs) -> FIFOResult:
    """
    Orquesta la ejecución de un algoritmo de scheduling.

    :param processes: lista de Process
    :param algorithm: 'fifo', 'sjf', 'srt', 'rr', 'priority'
    :param kwargs: parámetros específicos (por ej. quantum para rr)
    :return: ScheduleResult con timeline y waiting_times
    """
    algo = algorithm.lower()
    if algo == 'fifo':
        return fifo_schedule(processes, **kwargs)
    elif algo == 'sjf':
        return sjf_schedule(processes, **kwargs)
    elif algo == 'srt':
        return srt_schedule(processes, **kwargs)
    elif algo == 'rr':
        return rr_schedule(processes, **kwargs)
    elif algo == 'priority':
        return priority_schedule(processes, **kwargs)
    else:
        raise ValueError(f"Algoritmo desconocido: {algorithm}")
