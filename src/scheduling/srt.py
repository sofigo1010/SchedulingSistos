from typing import List
from data_io.process_loader import Process
from scheduling.fifo import ScheduleResult


def schedule(processes: List[Process], **kwargs) -> ScheduleResult:
    """
    Shortest Remaining Time (preemptivo).
    En cada momento de llegada o finalización de ráfaga, selecciona el proceso con
    el menor tiempo restante.
    """
    # Copia e inicialización
    procs = sorted(processes, key=lambda p: p.arrival_time)
    n = len(procs)
    timeline = []  # [(pid, start, end), ...]
    waiting_times = {}

    # Tiempos restantes y llegadas
    remaining = {p.pid: p.burst_time for p in procs}
    arrival = {p.pid: p.arrival_time for p in procs}

    current_time = 0
    i = 0  # índice para llegada
    # Proceso en ejecución
    current_proc = None  # pid
    last_switch_time = 0

    while i < n or any(rem > 0 for rem in remaining.values()):
        # Incorporar nuevos procesos que llegan
        while i < n and procs[i].arrival_time <= current_time:
            i += 1
        # Seleccionar proceso con menor remaining > 0 y arrival <= current_time
        candidates = [p for p in procs
                      if p.arrival_time <= current_time and remaining[p.pid] > 0]
        if not candidates:
            # Saltar al próximo arrival
            current_time = procs[i].arrival_time
            continue
        # Elegir el que tenga el menor remaining
        candidates.sort(key=lambda p: remaining[p.pid])
        chosen = candidates[0]

        # Si cambiamos de proceso, cerrar bloque anterior
        if current_proc and current_proc != chosen.pid:
            timeline.append((current_proc, last_switch_time, current_time))
            last_switch_time = current_time
        # Si no había proceso, iniciar bloque
        if not current_proc:
            last_switch_time = current_time
        current_proc = chosen.pid

        # Ejecutar un ciclo completo (preemptivo por ciclo)
        remaining[current_proc] -= 1
        current_time += 1

        # Si el proceso termina, cerrar bloque y registrar finish
        if remaining[current_proc] == 0:
            timeline.append((current_proc, last_switch_time, current_time))
            # Tiempo de espera = finish - arrival - burst
            waiting_times[current_proc] = current_time - arrival[current_proc] - chosen.burst_time
            current_proc = None
            last_switch_time = current_time

    return ScheduleResult(timeline, waiting_times)
