import customtkinter as ctk
import tkinter as tk

class ControlsPanel(ctk.CTkFrame):
    """
    Panel con dos pestañas: Calendarización y Sincronización.
    - Calendarización: selección de algoritmos, quantum, delay,
      carga de procesos, ejecución, métricas generales e info por PID.
    - Sincronización: selección de modo, carga de procesos, recursos y acciones,
      delay, ejecución, métricas generales e info por PID con estado.
    """
    def __init__(self, master, callbacks: dict, **kwargs):
        super().__init__(master, **kwargs)
        self.callbacks = callbacks
        self._build_tabs()

    def _build_tabs(self):
        tabview = ctk.CTkTabview(self, width=300)
        tabview.add("Calendarización")
        tabview.add("Sincronización")
        tabview.pack(fill="y", side="left", padx=10, pady=10)

        # ==================== CALENDARIZACIÓN ====================
        cal_tab = tabview.tab("Calendarización")
        cal_tab.grid_rowconfigure(9, weight=1)
        cal_tab.grid_columnconfigure((0,1), weight=1)

        # 0: Cargar procesos
        ctk.CTkButton(cal_tab, text="Cargar procesos",
                      command=self.callbacks.get('load')) \
            .grid(row=0, column=0, columnspan=2, pady=(10,5))

        # 1-3: Checkboxes de algoritmos
        self.algo_vars = {}
        algos_list = ['fifo','sjf','srt','rr','priority']
        for idx, algo in enumerate(algos_list):
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(cal_tab, text=algo.upper(), variable=var,
                                 command=lambda a=algo: self._on_algo_toggle(a))
            r, c = divmod(idx, 2)
            cb.grid(row=r+1, column=c, sticky="w", padx=10, pady=2)
            self.algo_vars[algo] = var

        # 4: Quantum (RR)
        ctk.CTkLabel(cal_tab, text="Quantum (RR):") \
            .grid(row=4, column=0, padx=10, pady=(10,2), sticky="w")
        self.quantum_var = tk.StringVar(value='4')
        self.quantum_entry = ctk.CTkEntry(cal_tab, textvariable=self.quantum_var, width=80)
        self.quantum_entry.grid(row=4, column=1, padx=10, pady=(10,2), sticky="w")
        self.quantum_entry.configure(state='disabled')

        # 5: Delay
        ctk.CTkLabel(cal_tab, text="Delay (ms):") \
            .grid(row=5, column=0, padx=10, pady=(5,2), sticky="w")
        self.delay_var = tk.StringVar(value='500')
        ctk.CTkEntry(cal_tab, textvariable=self.delay_var, width=80) \
            .grid(row=5, column=1, padx=10, pady=(5,2), sticky="w")

        # 6: Botones Ejecutar / Pausar / Limpiar
        btns = ctk.CTkFrame(cal_tab)
        btns.grid(row=6, column=0, columnspan=2, pady=15)
        ctk.CTkButton(btns, text="Ejecutar", command=self._on_run) \
            .grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns, text="Pausar", command=self.callbacks.get('pause')) \
            .grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns, text="Limpiar", command=self.callbacks.get('clear')) \
            .grid(row=0, column=2, padx=5)

        # 7: Métricas generales
        self.metrics_box = ctk.CTkTextbox(cal_tab, height=100, width=280)
        self.metrics_box.grid(row=7, column=0, columnspan=2,
                              padx=10, pady=(5,2), sticky="nsew")
        self.metrics_box.insert("0.0", "Aquí aparecerán las métricas...\n")
        self.metrics_box.configure(state="disabled")

        # 8: Info de proceso individual
        self.info_box = ctk.CTkTextbox(cal_tab, height=100, width=280)
        self.info_box.grid(row=8, column=0, columnspan=2,
                           padx=10, pady=(2,10), sticky="nsew")
        self.info_box.insert("0.0", "Aquí aparecerán detalles del proceso...\n")
        self.info_box.configure(state="disabled")

        # ==================== SINCRONIZACIÓN ====================
        sync_tab = tabview.tab("Sincronización")
        sync_tab.grid_rowconfigure(10, weight=1)
        sync_tab.grid_columnconfigure(0, weight=1)

        # 0: Modo de sincronización
        ctk.CTkLabel(sync_tab, text="Modo sincronización:") \
            .grid(row=0, column=0, sticky="w", padx=10, pady=(10,2))
        self.sync_var = tk.StringVar(value="mutex")
        ctk.CTkOptionMenu(sync_tab, variable=self.sync_var,
                           values=["mutex", "semaphore"]) \
            .grid(row=1, column=0, sticky="w", padx=10, pady=(0,10))

        # 2: Cargar procesos
        ctk.CTkButton(sync_tab, text="Cargar procesos",
                      command=self.callbacks.get('load')) \
            .grid(row=2, column=0, sticky="ew", padx=10, pady=(5,2))

        # 3: Cargar recursos
        ctk.CTkButton(sync_tab, text="Cargar recursos",
                      command=self.callbacks.get('load_resources')) \
            .grid(row=3, column=0, sticky="ew", padx=10, pady=2)

        # 4: Cargar acciones
        ctk.CTkButton(sync_tab, text="Cargar acciones",
                      command=self.callbacks.get('load_actions')) \
            .grid(row=4, column=0, sticky="ew", padx=10, pady=(2,10))

        # 5: Delay sincronización
        ctk.CTkLabel(sync_tab, text="Delay (ms):") \
            .grid(row=5, column=0, sticky="w", padx=10, pady=(5,2))
        self.sync_delay_var = tk.StringVar(value='500')
        ctk.CTkEntry(sync_tab, textvariable=self.sync_delay_var, width=80) \
            .grid(row=6, column=0, sticky="w", padx=10, pady=(2,10))

        # 7: Botones Ejecutar / Pausar / Limpiar
        btns2 = ctk.CTkFrame(sync_tab)
        btns2.grid(row=7, column=0, pady=5)
        ctk.CTkButton(btns2, text="Ejecutar",
                      command=self._on_sync_run) \
            .grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns2, text="Pausar",
                      command=self.callbacks.get('pause')) \
            .grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns2, text="Limpiar",
                      command=self.callbacks.get('clear')) \
            .grid(row=0, column=2, padx=5)

        # 8: Métricas generales de sincronización
        self.sync_metrics_box = ctk.CTkTextbox(sync_tab, height=100, width=280)
        self.sync_metrics_box.grid(row=8, column=0,
                                   padx=10, pady=(5,2), sticky="nsew")
        self.sync_metrics_box.insert("0.0", "Aquí aparecerán métricas de sync...\n")
        self.sync_metrics_box.configure(state="disabled")

        # 9: Info de proceso individual en sincronización
        self.sync_info_box = ctk.CTkTextbox(sync_tab, height=100, width=280)
        self.sync_info_box.grid(row=9, column=0,
                                padx=10, pady=(2,10), sticky="nsew")
        self.sync_info_box.insert("0.0", "Aquí aparecerán detalles de sync...\n")
        self.sync_info_box.configure(state="disabled")

    def _on_algo_toggle(self, algo: str):
        # Habilita/deshabilita quantum para RR
        if algo == 'rr':
            state = 'normal' if self.algo_vars['rr'].get() else 'disabled'
            self.quantum_entry.configure(state=state)

    def _on_run(self):
        algos = [a for a, var in self.algo_vars.items() if var.get()]
        quantum = int(self.quantum_var.get()) if 'rr' in algos else None
        delay = int(self.delay_var.get())
        self.callbacks.get('run')(algorithms=algos, quantum=quantum, delay=delay)

    def _on_sync_run(self):
        mode = self.sync_var.get()
        delay = int(self.sync_delay_var.get())
        self.callbacks.get('run_sync')(mode=mode, delay=delay)
