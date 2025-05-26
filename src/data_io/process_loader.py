from dataclasses import dataclass
from typing import List

@dataclass
class Process:
    pid: str
    burst_time: int
    arrival_time: int
    priority: int


def load_processes(path: str) -> List[Process]:
    """
    Lee un archivo de procesos con formato por línea:
        <PID>, <BT>, <AT>, <Priority>
    y devuelve una lista de Process.
    """
    processes: List[Process] = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 4:
                raise ValueError(f"Formato inválido en línea: '{line}'")
            pid, bt, at, pr = parts
            processes.append(
                Process(
                    pid=pid,
                    burst_time=int(bt),
                    arrival_time=int(at),
                    priority=int(pr)
                )
            )
    return processes