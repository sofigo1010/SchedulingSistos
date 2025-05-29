from typing import List, Dict, Tuple
from data_io.process_loader import Process
from data_io.sync_loader import Resource, Action

class SyncResult:
    """
    Resultado de simulación de sincronización:
      - timeline: lista de tuplas (cycle, pid, resource, state)
      - waiting_counts: dict {pid: num_waits}
    """
    def __init__(self, timeline: List[Tuple[int, str, str, str]], waiting_counts: Dict[str, int]):
        self.timeline = timeline
        self.waiting_counts = waiting_counts


def simulate(processes: List[Process], resources: List[Resource], actions: List[Action]) -> SyncResult:
    """
    Simulación de acceso a recursos con Mutex Locks.
    Cada recurso permite un acceso por ciclo (count=1).
    """
    # Organizar actions por ciclo
    actions_by_cycle = {}
    for act in actions:
        actions_by_cycle.setdefault(act.cycle, []).append(act)

    # Estado de recursos siempre count=1 por ciclo
    original_counts = {res.name: 1 for res in resources}
    waiting_counts: Dict[str, int] = {p.pid: 0 for p in processes}
    timeline: List[Tuple[int, str, str, str]] = []  # (cycle, pid, resource, 'ACCESED'|'WAITING')

    max_cycle = max(actions_by_cycle.keys()) if actions_by_cycle else 0
    # Simular ciclo a ciclo
    for cycle in range(max_cycle + 1):
        # recursos disponibles al inicio de ciclo
        available = original_counts.copy()
        # procesar acciones en orden de llegada en ese ciclo
        for act in actions_by_cycle.get(cycle, []):
            if available.get(act.resource, 0) > 0:
                state = 'ACCESED'
                available[act.resource] -= 1
            else:
                state = 'WAITING'
                waiting_counts[act.pid] = waiting_counts.get(act.pid, 0) + 1
            timeline.append((cycle, act.pid, act.resource, state))
    return SyncResult(timeline, waiting_counts)
