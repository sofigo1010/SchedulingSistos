from dataclasses import dataclass
from typing import List


@dataclass
class Resource:
    name: str
    count: int

@dataclass
class Action:
    pid: str
    action: str  # 'READ' o 'WRITE'
    resource: str
    cycle: int


def load_resources(path: str) -> List[Resource]:
    """
    Lee un archivo de recursos con formato por línea:
        <NOMBRE RECURSO>, <CONTADOR>
    y devuelve una lista de Resource.
    """
    resources: List[Resource] = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 2:
                raise ValueError(f"Formato inválido en línea de recursos: '{line}'")
            name, cnt = parts
            resources.append(Resource(name=name, count=int(cnt)))
    return resources


def load_actions(path: str) -> List[Action]:
    """
    Lee un archivo de acciones con formato por línea:
        <PID>, <ACCION>, <RECURSO>, <CICLO>
    y devuelve una lista de Action.
    """
    actions: List[Action] = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 4:
                raise ValueError(f"Formato inválido en línea de acciones: '{line}'")
            pid, act, res, cyc = parts
            actions.append(
                Action(
                    pid=pid,
                    action=act.upper(),
                    resource=res,
                    cycle=int(cyc)
                )
            )
    return actions
