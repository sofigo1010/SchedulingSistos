# 🧠 Simulador de Sistemas Operativos

Este proyecto permite simular algoritmos clásicos de **calendarización de procesos** (scheduling) y **sincronización de acceso a recursos** (mutex y semáforos), usando una interfaz gráfica intuitiva con `CustomTkinter`.

La aplicación permite cargar archivos de entrada, seleccionar algoritmos y visualizar los resultados a través de diagramas de Gantt animados, junto con métricas de rendimiento.

---

## 🖼️ Interfaz Gráfica

La GUI está diseñada con `CustomTkinter` y ofrece dos pestañas principales:

- **Calendarización**  
  - Selección de algoritmo (`FIFO`, `SJF`, `SRT`, `RR`, `Priority`)  
  - Campo para `Quantum` en Round-Robin  
  - Delay en milisegundos para animación  
  - Carga de procesos y visor de su contenido  
  - Visualización de métricas globales y detalles por PID  

- **Sincronización**  
  - Selección del modo (`Mutex` o `Semaphore`)  
  - Carga y visor de archivos: procesos, recursos, acciones  
  - Delay en milisegundos para animación  
  - Métricas globales y detalles por PID  

Todos los resultados se presentan en diagramas de Gantt, ya sea de forma instantánea o animada paso a paso.

---

## 🧩 Algoritmos Implementados

### 🕒 Calendarización
- **FIFO** (First In, First Out)  
- **SJF** (Shortest Job First)  
- **SRT** (Shortest Remaining Time) – preemptivo  
- **RR** (Round Robin) – requiere `quantum`  
- **Priority** – no-preemptivo (prioridad numérica baja = más urgente)  

Cada algoritmo produce:  
1. **Timeline**: lista de segmentos `(PID, start, end)`  
2. **Waiting Times**: tiempo de espera por PID  
3. **Completion Times**: tiempo de finalización por PID  

### 🔐 Sincronización
- **Mutex**: un único acceso por recurso y ciclo  
- **Semaphore**: acceso múltiple (definido por `count`) por recurso y ciclo  

Resultados:  
- **Timeline**: lista de tuplas `(cycle, PID, resource, state)`  
- **Waiting Counts**: número de ciclos de espera por PID  

---

## 📊 Métricas Calculadas

- **Average Waiting Time (AWT)**  
- **Turnaround Time (TA)**  
- **Total Waits**  
- **Throughput**  
- **Waiting Rate**

---

## 📂 Estructura del Proyecto

```
data/
│   processes.txt
│   resources.txt
│   actions.txt

src/
├── core/
│   ├── scheduler.py
│   └── sync_engine.py

├── data_io/
│   ├── process_loader.py
│   └── sync_loader.py

├── gui/
│   ├── main_window.py       ← Punto de entrada
│   ├── controls_panel.py
│   ├── gantt_canvas.py
│   └── styles.py

├── scheduling/
│   ├── fifo.py
│   ├── sjf.py
│   ├── srt.py
│   ├── rr.py
│   └── priority.py

├── synchronization/
│   ├── mutex.py
│   └── semaphore.py

└── utils/
    └── metrics.py
```

---

## ✅ Requisitos y Dependencias

- **Python 3.7+**  
- **CustomTkinter** (GUI moderna sobre `tkinter`)

### Instalación rápida

```bash
pip install --upgrade pip
pip install customtkinter
```

> `tkinter` suele venir preinstalado en la mayoría de las distribuciones de Python.

---

## ▶️ Cómo Ejecutar

Desde la raíz del proyecto:

```bash
cd src/gui
python main_window.py
```

Se abrirá la ventana principal. Ahí podrás:

1. **Elegir** la pestaña **Calendarización** o **Sincronización**  
2. **Cargar** los archivos de texto correspondientes  
3. **Seleccionar** algoritmos o modo  
4. **Ejecutar** la simulación y ver resultados en Gantt y métricas  

---

## 📥 Formato de Archivos de Entrada

- **processes.txt**  
  ```
  PID, BurstTime, ArrivalTime, Priority
  ```
- **resources.txt**  
  ```
  ResourceName, Count
  ```
- **actions.txt**  
  ```
  PID, Action[READ|WRITE], ResourceName, Cycle
  ```


