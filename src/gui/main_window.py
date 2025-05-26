#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List

import customtkinter as ctk
from tkinter import filedialog, messagebox

# Aseguramos que el directorio `src/` esté en el PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Importamos nuestros módulos desde src/
from gui.styles import apply_theme
from gui.controls_panel import ControlsPanel
from gui.gantt_canvas import GanttCanvas
from data_io.process_loader import load_processes
from data_io.sync_loader import load_resources, load_actions
from core.scheduler import run_scheduling
from core.sync_engine import run_synchronization
from utils.metrics import (
    compute_avg_waiting_time,
    compute_total_waits,
    compute_avg_turnaround_time
)


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Sistemas Operativos")
        self.geometry("1400x700")
        apply_theme()

        # Layout: controles izquierda, resultados a la derecha
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Panel de controles
        self.controls = ControlsPanel(
            master=self,
            callbacks={
                'load':            self.on_load,
                'load_resources':  self.on_load_resources,
                'load_actions':    self.on_load_actions,
                'run':             self.on_run,
                'run_sync':        self.on_run_sync,
                'pause':           self.on_pause,
                'clear':           self.on_clear
            }
        )
        self.controls.grid(row=0, column=0, sticky="ns")

        # Contenedor para múltiples diagramas
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)

        # Lista para almacenar referencias a los GanttCanvas creados
        self.gantt_canvases: List[GanttCanvas] = []

        # Datos cargados
        self.processes = []
        self.resources = []
        self.actions = []

    def on_load(self):
        """Carga archivo de procesos."""
        path = filedialog.askopenfilename(
            title="Selecciona archivo de procesos",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return
        try:
            self.processes = load_processes(path)
            messagebox.showinfo("Carga exitosa", f"{len(self.processes)} procesos cargados.")
        except Exception as e:
            messagebox.showerror("Error al cargar procesos", str(e))

    def on_load_resources(self):
        """Carga archivo de recursos."""
        path = filedialog.askopenfilename(
            title="Selecciona archivo de recursos",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return
        try:
            self.resources = load_resources(path)
            messagebox.showinfo("Carga exitosa", f"{len(self.resources)} recursos cargados.")
        except Exception as e:
            messagebox.showerror("Error al cargar recursos", str(e))

    def on_load_actions(self):
        """Carga archivo de acciones."""
        path = filedialog.askopenfilename(
            title="Selecciona archivo de acciones",
            filetypes=[("Text files", "*.txt")]
        )
        if not path:
            return
        try:
            self.actions = load_actions(path)
            messagebox.showinfo("Carga exitosa", f"{len(self.actions)} acciones cargadas.")
        except Exception as e:
            messagebox.showerror("Error al cargar acciones", str(e))

    def on_run(self, algorithms=None, quantum=None, delay=0):
        """Ejecuta calendarización, muestra métricas y dibuja Gantt."""
        self.clear_canvases()
        algos = algorithms or [a for a,v in self.controls.algo_vars.items() if v.get()]
        if not algos:
            messagebox.showwarning("Atención", "Selecciona al menos un algoritmo.")
            return

        arrival_map = {p.pid: p.arrival_time for p in self.processes}
        mb = self.controls.metrics_box
        mb.configure(state="normal"); mb.delete("0.0","end")
        mb.insert("0.0", "Métricas por algoritmo:\n")
        for algo in algos:
            res = run_scheduling(self.processes, algo, quantum=quantum)
            awt = compute_avg_waiting_time(res.waiting_times)
            tw  = compute_total_waits(res.waiting_times)
            ta  = compute_avg_turnaround_time(res.completion_times, arrival_map)
            mb.insert("end", f" • {algo.upper():<8} AWT={awt:.2f}  TA={ta:.2f}  waits={tw}\n")
        mb.configure(state="disabled")

        for idx, algo in enumerate(algos):
            res = run_scheduling(self.processes, algo, quantum=quantum)
            frame = ctk.CTkFrame(self.results_frame)
            frame.grid(row=idx, column=0, sticky="ew", pady=10)
            frame.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(frame, text=algo.upper(), font=(None,16,"bold"))\
               .grid(row=0,column=0, padx=(0,10), sticky="w")
            gantt = GanttCanvas(
                master=frame, height=150,
                on_item_click=lambda pid, r=res: self.show_process_info(pid, r)
            )
            gantt.grid(row=1, column=0, columnspan=2, sticky="ew")
            self.gantt_canvases.append(gantt)
            if delay>0:
                gantt.draw_schedule_delayed(res.timeline, delay_ms=delay)
            else:
                gantt.draw_schedule(res.timeline)

    def on_run_sync(self, mode=None, delay=0):
        """Ejecuta sincronización, muestra métricas y dibuja Gantt de sincronización."""
        # 1) Limpia gráficos anteriores
        self.clear_canvases()

        # 2) Chequea que todo esté cargado
        if not (self.processes and self.resources and self.actions):
            messagebox.showwarning("Atención", "Carga procesos, recursos y acciones primero.")
            return

        # 3) Corre la simulación
        sync_res = run_synchronization(self.processes, self.resources, self.actions, mode=mode)

        # 4) Métricas generales: accesses vs waits
        mb = self.controls.sync_metrics_box
        total_accesses = len(sync_res.timeline)
        total_waits    = compute_total_waits(sync_res.waiting_counts)

        mb.configure(state="normal")
        mb.delete("0.0", "end")
        mb.insert("0.0", f"Total accesses: {total_accesses}\n")
        mb.insert("end",  f"Total waits:    {total_waits}\n")
        mb.configure(state="disabled")

        # 5) Crea el contenedor para el único Gantt de sincronización
        frame = ctk.CTkFrame(self.results_frame)
        frame.grid(row=0, column=0, sticky="ew", pady=10)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=mode.upper(), font=(None,16,"bold")) \
           .grid(row=0, column=0, padx=(0,10), sticky="w")

        # 6) Instancia el canvas con su handler de click
        gantt = GanttCanvas(
            master=frame,
            height=150,
            on_item_click=lambda pid, state: self.show_sync_info(pid, state, sync_res)
        )
        gantt.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.gantt_canvases.append(gantt)

        # 7) Dibuja animado o inmediato según delay
        if delay and delay > 0:
            gantt.draw_sync_delayed(sync_res.timeline, delay_ms=delay)
        else:
            gantt.draw_sync(sync_res.timeline)




    def show_process_info(self, pid, res):
        proc = next((p for p in self.processes if p.pid==pid), None)
        at, bt = (proc.arrival_time, proc.burst_time) if proc else (None,None)
        wt = res.waiting_times.get(pid,0)
        ct = res.completion_times.get(pid)
        ta = (ct-at) if (ct and at is not None) else None
        info = [f"PID: {pid}", f"Arrival: {at}", f"Burst: {bt}",
                f"Waiting: {wt}", f"TA: {ta}", f"Complete: {ct}"]
        ib = self.controls.info_box
        ib.configure(state="normal"); ib.delete("0.0","end")
        ib.insert("0.0","\n".join(info)); ib.configure(state="disabled")

    def show_sync_info(self, pid, state, res):
        """
        Al clicar un bloque de sync, muestra:
          - PID
          - Estado (ACCESED/WAITING)
          - Ciclo start y end (end = start + 1)
          - Número de waits de ese PID
        """
        # Localiza la primera tupla de este pid
        entry = next((t for t in res.timeline if t[1] == pid), None)
        if entry:
            cycle = entry[0]
            start = cycle
            end   = cycle + 1
        else:
            start = end = None

        waits = res.waiting_counts.get(pid, 0)

        info = [
            f"PID:     {pid}",
            f"Estado:  {state}",
            f"Start:   {start}",
            f"End:     {end}",
            f"Waits:   {waits}"
        ]
        ib = self.controls.sync_info_box
        ib.configure(state="normal")
        ib.delete("0.0", "end")
        ib.insert("0.0", "\n".join(info))
        ib.configure(state="disabled")

    def on_pause(self):
        """Pausa todas las animaciones de Gantt."""
        for canvas in self.gantt_canvases:
            canvas.pause()
        messagebox.showinfo("Pausa", "Simulación pausada.")

    def clear_canvases(self):
        for c in self.gantt_canvases:
            c.clear(); c.master.destroy()
        self.gantt_canvases.clear()

    def on_clear(self):
        self.clear_canvases()


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
