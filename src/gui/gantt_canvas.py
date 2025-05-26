import customtkinter as ctk
import tkinter as tk
from typing import List, Tuple, Dict, Callable


class GanttCanvas(ctk.CTkFrame):
    """
    Canvas con scroll bidireccional para diagramas de Gantt:
      - draw_schedule / draw_schedule_delayed: 3-tuplas (pid,start,end)
      - draw_sync    / draw_sync_delayed:      4-tuplas (cycle,pid,resource,state)
      - pausa y click handler
    """
    def __init__(
        self,
        master,
        on_item_click: Callable[..., None] = None,
        width=800,
        height=400,
        row_height=40,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.row_height = row_height
        self.on_item_click = on_item_click
        self._jobs: List[str] = []  # track of scheduled after jobs

        # Determine effective background
        fg = self.cget("fg_color")
        if isinstance(fg, (list, tuple)) and len(fg) == 2:
            mode = ctk.get_appearance_mode()
            bg_color = fg[1] if mode == "dark" else fg[0]
        else:
            bg_color = fg

        # Canvas and scroll bars
        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg_color)
        self.h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.v_scroll = ctk.CTkScrollbar(self, orientation="vertical",   command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Color map: key -> color
        self.color_map: Dict[str, str] = {}
        self.default_colors = [
            "#4f81bd", "#c0504d", "#9bbb59", "#8064a2", "#4bacc6",
            "#f79646", "#92a9cf", "#d1b2d8", "#b8d7a3", "#a4bdd2"
        ]

    def clear(self):
        """Clear all drawings and cancel pending jobs"""
        for job in self._jobs:
            self.after_cancel(job)
        self._jobs.clear()
        self.canvas.delete("all")

    def pause(self):
        """Pause animation: cancel pending jobs"""
        for job in self._jobs:
            self.after_cancel(job)
        self._jobs.clear()

    def _get_color(self, key: str) -> str:
        if key not in self.color_map:
            idx = len(self.color_map) % len(self.default_colors)
            self.color_map[key] = self.default_colors[idx]
        return self.color_map[key]

    def draw_schedule(self, timeline: List[Tuple[str, int, int]]):
        """Immediate draw for scheduling: (pid, start, end)"""
        self.clear()
        pids: List[str] = []
        for pid, _, _ in timeline:
            if pid not in pids:
                pids.append(pid)
        max_t = max((e for _, _, e in timeline), default=0)
        self.canvas.config(scrollregion=(0, 0, max_t*20+100, len(pids)*self.row_height))
        for pid, s, e in timeline:
            row = pids.index(pid)
            y1 = row*self.row_height
            y2 = y1 + self.row_height*0.8
            x1 = s*20 + 50
            x2 = e*20 + 50
            color = self._get_color(pid)
            rid = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            tid = self.canvas.create_text((x1+x2)/2, y1+self.row_height*0.4, text=pid, fill="white")
            tag = f"proc_{pid}"
            self.canvas.addtag_withtag(tag, rid)
            self.canvas.addtag_withtag(tag, tid)
            if self.on_item_click:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, p=pid: self.on_item_click(p))

    def draw_schedule_delayed(self, timeline: List[Tuple[str, int, int]], delay_ms: int = 500):
        """Delayed draw for scheduling blocks"""
        self.clear()
        pids: List[str] = []
        for pid, _, _ in timeline:
            if pid not in pids:
                pids.append(pid)
        max_t = max((e for _, _, e in timeline), default=0)
        self.canvas.config(scrollregion=(0, 0, max_t*20+100, len(pids)*self.row_height))
        for i, (pid, s, e) in enumerate(timeline):
            job = self.after(delay_ms*i, lambda p=pid, st=s, en=e: self._draw_schedule_block(p, st, en, pids))
            self._jobs.append(job)

    def _draw_schedule_block(self, pid: str, start: int, end: int, pids: List[str]):
        row = pids.index(pid)
        y1 = row*self.row_height
        y2 = y1 + self.row_height*0.8
        x1 = start*20 + 50
        x2 = end*20 + 50
        color = self._get_color(pid)
        rid = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        tid = self.canvas.create_text((x1+x2)/2, y1+self.row_height*0.4, text=pid, fill="white")
        tag = f"proc_{pid}"
        self.canvas.addtag_withtag(tag, rid)
        self.canvas.addtag_withtag(tag, tid)
        if self.on_item_click:
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, p=pid: self.on_item_click(p))

    def draw_sync(self, timeline: List[Tuple[int, str, str, str]]):
        """Immediate draw for synchronization: (cycle, pid, resource, state)"""
        self.clear()
        resources: List[str] = []
        for _, _, res, _ in timeline:
            if res not in resources:
                resources.append(res)
        max_c = max((c for c, _, _, _ in timeline), default=0)
        self.canvas.config(scrollregion=(0,0, max_c*20+100, len(resources)*self.row_height))
        for cycle, pid, res, state in timeline:
            row = resources.index(res)
            y1 = row*self.row_height
            y2 = y1 + self.row_height*0.8
            x1 = cycle*20 + 50
            x2 = x1 + 20
            color = "#70ad47" if state == "ACCESED" else "#c00000"
            rid = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            tid = self.canvas.create_text((x1+x2)/2, y1+self.row_height*0.4, text=pid, fill="white")
            tag = f"sync_{pid}_{cycle}_{res}"
            self.canvas.addtag_withtag(tag, rid)
            self.canvas.addtag_withtag(tag, tid)
            if self.on_item_click:
                # callback recibe pid, estado
                self.canvas.tag_bind(tag, "<Button-1>", lambda e, p=pid, st=state: self.on_item_click(p, st))

    def draw_sync_delayed(self, timeline: List[Tuple[int, str, str, str]], delay_ms: int = 500):
        """Delayed draw for synchronization blocks"""
        self.clear()
        resources: List[str] = []
        for _, _, res, _ in timeline:
            if res not in resources:
                resources.append(res)
        max_c = max((c for c, _, _, _ in timeline), default=0)
        self.canvas.config(scrollregion=(0,0, max_c*20+100, len(resources)*self.row_height))
        for i, (cycle, pid, res, state) in enumerate(timeline):
            job = self.after(delay_ms*i, lambda c=cycle, p=pid, r=res, st=state: 
                self._draw_sync_block(c, p, r, st, resources)
            )
            self._jobs.append(job)

    def _draw_sync_block(self, cycle: int, pid: str, res: str, state: str, resources: List[str]):
        row = resources.index(res)
        y1 = row*self.row_height
        y2 = y1 + self.row_height*0.8
        x1 = cycle*20 + 50
        x2 = x1 + 20
        color = "#70ad47" if state == "ACCESED" else "#c00000"
        rid = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        tid = self.canvas.create_text((x1+x2)/2, y1+self.row_height*0.4, text=pid, fill="white")
        tag = f"sync_{pid}_{cycle}_{res}"
        self.canvas.addtag_withtag(tag, rid)
        self.canvas.addtag_withtag(tag, tid)
        if self.on_item_click:
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, p=pid, st=state: self.on_item_click(p, st))