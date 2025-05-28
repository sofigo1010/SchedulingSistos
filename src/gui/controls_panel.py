import customtkinter as ctk
import tkinter as tk

class ControlsPanel(ctk.CTkFrame):
    """
    Panel con dos pestañas: Calendarización y Sincronización.
    - Calendarización: selección de algoritmos, quantum, delay,
      carga de procesos, ejecución, métricas generales, info por PID y visor de archivo de procesos.
    - Sincronización: selección de modo, carga de procesos, recursos y acciones,
      delay, ejecución, métricas generales, info por PID y visor de archivos de sync.
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

        # ---------------- CALENDARIZACIÓN ----------------
        cal_tab = tabview.tab("Calendarización")
        cal_tab.grid_rowconfigure(11, weight=1)
        cal_tab.grid_columnconfigure((0,1), weight=1)

        # Botones carga / ver procesos
        btn_load = ctk.CTkButton(cal_tab, text="Cargar procesos", command=self.callbacks.get('load'))
        btn_load.grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="ew")
        btn_view = ctk.CTkButton(cal_tab, text="Ver procesos", command=self.callbacks.get('view_process_file'))
        btn_view.grid(row=1, column=0, columnspan=2, pady=(0,10), sticky="ew")

        # Checkboxes de algoritmos
        self.algo_vars = {}
        algos = ['fifo','sjf','srt','rr','priority']
        for i, a in enumerate(algos):
            var = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                cal_tab,
                text=a.upper(),
                variable=var,
                command=lambda algo=a: self._on_algo_toggle(algo)
            )
            r, c = divmod(i, 2)
            cb.grid(row=r+2, column=c, sticky="w", padx=10, pady=2)
            self.algo_vars[a] = var

        # Quantum RR
        lbl_q = ctk.CTkLabel(cal_tab, text="Quantum (RR):")
        lbl_q.grid(row=6, column=0, padx=10, pady=(10,2), sticky="w")
        self.quantum_var = tk.StringVar(value='4')
        self.quantum_entry = ctk.CTkEntry(cal_tab, textvariable=self.quantum_var, width=80)
        self.quantum_entry.grid(row=6, column=1, padx=10, pady=(10,2), sticky="w")
        self.quantum_entry.configure(state='disabled')

        # Delay
        lbl_delay = ctk.CTkLabel(cal_tab, text="Delay (ms):")
        lbl_delay.grid(row=7, column=0, padx=10, pady=(5,2), sticky="w")
        self.delay_var = tk.StringVar(value='500')
        entry_delay = ctk.CTkEntry(cal_tab, textvariable=self.delay_var, width=80)
        entry_delay.grid(row=7, column=1, padx=10, pady=(5,2), sticky="w")

        # Botones Ejecutar / Pausar / Limpiar
        btns = ctk.CTkFrame(cal_tab)
        btns.grid(row=8, column=0, columnspan=2, pady=10)
        ctk.CTkButton(btns, text="Ejecutar", command=self._on_run).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns, text="Pausar", command=self.callbacks.get('pause')).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns, text="Limpiar", command=self.callbacks.get('clear')).grid(row=0, column=2, padx=5)

        # Visor métricas y procesos
        self.metrics_box = ctk.CTkTextbox(cal_tab, height=100)
        self.metrics_box.grid(row=9, column=0, columnspan=2, padx=10, pady=(5,2), sticky="nsew")
        self.metrics_box.insert("0.0", "Métricas...\n")
        self.metrics_box.configure(state="disabled")

        self.info_box = ctk.CTkTextbox(cal_tab, height=100)
        self.info_box.grid(row=10, column=0, columnspan=2, padx=10, pady=(2,10), sticky="nsew")
        self.info_box.insert("0.0", "Detalles proceso...\n")
        self.info_box.configure(state="disabled")

        # Visor de archivo de procesos
        self.file_view_box = ctk.CTkTextbox(cal_tab, height=150)
        self.file_view_box.grid(row=11, column=0, columnspan=2, padx=10, pady=(0,10), sticky="nsew")
        self.file_view_box.insert("0.0", "Contenido del archivo aquí...\n")
        self.file_view_box.configure(state="disabled")

        # ---------------- SINCRONIZACIÓN ----------------
        sync_tab = tabview.tab("Sincronización")
        sync_tab.grid_rowconfigure(13, weight=1)
        sync_tab.grid_columnconfigure(0, weight=1)

        # Modo sincronización
        lbl_mode = ctk.CTkLabel(sync_tab, text="Modo:")
        lbl_mode.grid(row=0, column=0, sticky="w", padx=10, pady=(10,2))
        self.sync_var = tk.StringVar(value="mutex")
        ctk.CTkOptionMenu(sync_tab, variable=self.sync_var, values=["mutex","semaphore"]) \
            .grid(row=1, column=0, sticky="w", padx=10, pady=(0,10))

        # Carga y vista de archivos
        ctk.CTkButton(sync_tab, text="Cargar procesos", command=self.callbacks.get('load')) \
            .grid(row=2, column=0, sticky="ew", padx=10, pady=(5,2))
        ctk.CTkButton(sync_tab, text="Ver procesos", command=self.callbacks.get('view_process_file')) \
            .grid(row=3, column=0, sticky="ew", padx=10, pady=(0,5))
        ctk.CTkButton(sync_tab, text="Cargar recursos", command=self.callbacks.get('load_resources')).grid(row=4, column=0, sticky="ew", padx=10, pady=2)
        ctk.CTkButton(sync_tab, text="Ver recursos", command=self.callbacks.get('view_resources_file')).grid(row=5, column=0, sticky="ew", padx=10, pady=(0,5))
        ctk.CTkButton(sync_tab, text="Cargar acciones", command=self.callbacks.get('load_actions')).grid(row=6, column=0, sticky="ew", padx=10, pady=(2,5))
        ctk.CTkButton(sync_tab, text="Ver acciones", command=self.callbacks.get('view_actions_file')).grid(row=7, column=0, sticky="ew", padx=10, pady=(0,10))

        # Delay sincronización
        lbl_sync_delay = ctk.CTkLabel(sync_tab, text="Delay (ms):")
        lbl_sync_delay.grid(row=8, column=0, sticky="w", padx=10, pady=(5,2))
        self.sync_delay_var = tk.StringVar(value='500')
        ctk.CTkEntry(sync_tab, textvariable=self.sync_delay_var, width=80).grid(row=9, column=0, sticky="w", padx=10, pady=(2,10))

        # Botones sync
        btns2 = ctk.CTkFrame(sync_tab)
        btns2.grid(row=10, column=0, pady=5)
        ctk.CTkButton(btns2, text="Ejecutar", command=self._on_sync_run).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns2, text="Pausar", command=self.callbacks.get('pause')).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns2, text="Limpiar", command=self.callbacks.get('clear')).grid(row=0, column=2, padx=5)

        # Visores de sync
        self.sync_metrics_box = ctk.CTkTextbox(sync_tab, height=100)
        self.sync_metrics_box.grid(row=11, column=0, padx=10, pady=(5,2), sticky="nsew")
        self.sync_metrics_box.insert("0.0", "Métricas sync...\n")
        self.sync_metrics_box.configure(state="disabled")

        self.sync_info_box = ctk.CTkTextbox(sync_tab, height=100)
        self.sync_info_box.grid(row=12, column=0, padx=10, pady=(2,10), sticky="nsew")
        self.sync_info_box.insert("0.0", "Detalles sync...\n")
        self.sync_info_box.configure(state="disabled")

        self.sync_file_view_box = ctk.CTkTextbox(sync_tab, height=150)
        self.sync_file_view_box.grid(row=13, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.sync_file_view_box.insert("0.0", "Contenido sync...\n")
        self.sync_file_view_box.configure(state="disabled")

    def _on_algo_toggle(self, algo):
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

    def display_file_content(self, content):
        self.file_view_box.configure(state="normal")
        self.file_view_box.delete("0.0", "end")
        self.file_view_box.insert("0.0", content)
        self.file_view_box.configure(state="disabled")

    def display_sync_file_content(self, content):
        self.sync_file_view_box.configure(state="normal")
        self.sync_file_view_box.delete("0.0", "end")
        self.sync_file_view_box.insert("0.0", content)
        self.sync_file_view_box.configure(state="disabled")
