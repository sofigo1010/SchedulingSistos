from typing import List, Any
from data_io.process_loader import Process
from data_io.sync_loader import Resource, Action
from synchronization.mutex import simulate as mutex_sim
from synchronization.semaphore import simulate as sem_sim


def run_synchronization(processes: List[Process], resources: List[Resource],
                       actions: List[Action], mode: str = 'mutex') -> Any:
    """
    Orquesta la simulación de sincronización.

    :param processes: lista de Process
    :param resources: lista de Resource
    :param actions: lista de Action
    :param mode: 'mutex' o 'semaphore'
    :return: SyncResult con timeline y waiting_counts
    """
    m = mode.lower()
    if m == 'mutex':
        return mutex_sim(processes, resources, actions)
    elif m == 'semaphore':
        return sem_sim(processes, resources, actions)
    else:
        raise ValueError(f"Modo desconocido: {mode}")
