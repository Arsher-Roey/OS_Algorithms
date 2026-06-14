import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
import io

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import algorithms
from algorithms.disk_scheduling import DISK_REGISTRY, DIRECTION_ALGORITHMS
from algorithms import memory_management as memalgo


COLORS = {
    "bg":               "#111316",
    "bg_panel":         "#1e2023",
    "bg_card":          "#1a1c1f",
    "bg_elevated":      "#282a2d",
    "bg_highest":       "#333538",

    "sidebar_bg":       "#111316",
    "sidebar_active":   "#1e2023",
    "sidebar_border":   "#4a8eff",

    "text_primary":     "#e2e2e6",
    "text_secondary":   "#c1c6d7",
    "text_muted":       "#8b90a0",
    "text_accent":      "#adc7ff",

    "primary":          "#4a8eff",
    "primary_light":    "#adc7ff",
    "secondary":        "#44dfab",
    "secondary_dark":   "#00bf8e",

    "border":           "#414754",
    "border_focus":     "#4a8eff",

    "status_running_bg":     "#003827",
    "status_running_fg":     "#44dfab",
    "status_waiting_bg":     "#1e2a3a",
    "status_waiting_fg":     "#adc7ff",
    "status_terminated_bg":  "#2a1a1a",
    "status_terminated_fg":  "#ffb4ab",
    "status_ready_bg":       "#2a2a1a",
    "status_ready_fg":       "#e2e2e6",

    "icon_cpu":     "#1a2a3a",
    "icon_mem":     "#1a2d2a",
    "icon_virt":    "#2d1a10",
    "icon_disk":    "#1a2040",
    "icon_sec":     "#2d1a1a",
}


FONTS = {
    "headline_lg": ("Inter", 28, "bold"),
    "headline_md": ("Inter", 20, "bold"),
    "headline_sm": ("Inter", 15, "bold"),
    "body_md":     ("Inter", 13, "normal"),
    "body_sm":     ("Inter", 11, "normal"),
    "label_caps":  ("Inter", 10, "bold"),
    "data_md":     ("JetBrains Mono", 12, "normal"),
    "data_sm":     ("JetBrains Mono", 11, "normal"),
    "nav":         ("Inter", 13, "normal"),
    "button":      ("Inter", 13, "bold"),
    "metric_val":  ("JetBrains Mono", 13, "bold"),
}


ABOUT_US_TEXT = (
    "The OS Simulator project is an educational platform designed to "
    "visualize complex kernel operations. Developed for students and "
    "enthusiasts to explore low-level system logic through interactive, "
    "real-time algorithmic execution."
)


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(
            master,
            width=240,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs
        )
        self.grid_propagate(False)
        self.navigate_callback = navigate_callback
        self.active_page = "Home"
        self.nav_buttons = {}

        self._build_logo()
        self._build_nav()
        self._build_about_us()

    def _build_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(20, 24))

        icon_box = ctk.CTkFrame(
            logo_frame,
            width=40, height=40,
            fg_color=COLORS["primary"],
            corner_radius=10,
        )
        icon_box.pack_propagate(False)
        icon_box.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            icon_box,
            text="⚙",
            font=("Inter", 18, "bold"),
            text_color="#ffffff",
        ).place(relx=0.5, rely=0.5, anchor="center")

        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.pack(side="left")

        ctk.CTkLabel(
            text_frame,
            text="OS Simulator",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Management Console",
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w")

    def _build_nav(self):
        nav_container = ctk.CTkFrame(self, fg_color="transparent")
        nav_container.pack(fill="x", pady=(0, 8))

        self.nav_items = [
            ("Home",                "Home",               "🏠"),
            ("CPU Scheduling",      "CPU Scheduling",     "⚙️"),
            ("Memory Management",   "Memory Management",  "🖥"),
            ("Virtual Memory",      "Virtual Memory",     "💾"),
            ("Disk Management",     "Disk Management",    "💿"),
            ("Security Management", "Security Management","🛡"),
        ]

        for label, page_key, icon in self.nav_items:
            btn = self._make_nav_button(nav_container, label, page_key, icon)
            self.nav_buttons[page_key] = btn

        self.set_active("Home")

    def _make_nav_button(self, parent, label, page_key, icon):
        btn = ctk.CTkButton(
            parent,
            text=f"  {icon}  {label}",
            font=FONTS["nav"],
            anchor="w",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["bg_elevated"],
            command=lambda pk=page_key: self.navigate_callback(pk),
        )
        btn.pack(fill="x", padx=12, pady=2)
        return btn

    def set_active(self, page_key):
        self.active_page = page_key
        for key, btn in self.nav_buttons.items():
            if key == page_key:
                btn.configure(
                    fg_color=COLORS["sidebar_active"],
                    text_color=COLORS["primary_light"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )

    def _build_about_us(self):
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_elevated"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(fill="x", padx=12, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text="About Us",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=14, pady=(12, 4))

        ctk.CTkLabel(
            card,
            text=ABOUT_US_TEXT,
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
            wraplength=190,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 14))


class HomePage(ctk.CTkFrame):

    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.navigate_callback = navigate_callback
        self._build_header()
        self._build_cards()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(32, 24))

        ctk.CTkLabel(
            header,
            text="Hi, what do you want to do?",
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Select a module to start the simulation and observe real-time algorithmic execution.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(4, 0))

    def _build_cards(self):
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.modules = [
            (
                "CPU Scheduling",
                "Dive deep into the heart of the operating system. Simulate First-Come-First-Served, "
                "Round Robin, and Shortest Job First algorithms. Visualize process states, burst times, "
                "and monitor context switching overhead in real-time.",
                "🖥",
                COLORS["icon_cpu"],
                "CPU Scheduling",
                "SYSTEM_CORE_V1",
            ),
            (
                "Memory Management",
                "Observe dynamic partitioning, fragmentation, and coalescing. Test and compare "
                "Best-fit vs Worst-fit allocation logic.",
                "🗂",
                COLORS["icon_mem"],
                "Memory Management",
                None,
            ),
            (
                "Virtual Memory",
                "Simulate paging, segmentation, and page replacement algorithms like LRU and FIFO. "
                "Monitor page faults and swap space.",
                "⚡",
                COLORS["icon_virt"],
                "Virtual Memory",
                None,
            ),
            (
                "Disk Management",
                "Analyze FCFS, SCAN, and C-SCAN disk scheduling. Visualize seek times and "
                "rotational latency on physical platter simulations.",
                "💾",
                COLORS["icon_disk"],
                "Disk Management",
                None,
            ),
            (
                "Security Management",
                "Manage Access Control Lists (ACL), capability lists, and simulate common system "
                "vulnerabilities and prevention.",
                "🛡",
                COLORS["icon_sec"],
                "Security Management",
                None,
            ),
        ]

        row0 = ctk.CTkFrame(scroll, fg_color="transparent")
        row0.pack(fill="x", pady=(0, 16))
        row0.columnconfigure(0, weight=3)
        row0.columnconfigure(1, weight=2)

        self._make_card(row0, self.modules[0], large=True).grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self._make_card(row0, self.modules[1], large=True).grid(row=0, column=1, sticky="nsew")

        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 16))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        row1.columnconfigure(2, weight=1)

        for i, module in enumerate(self.modules[2:]):
            self._make_card(row1, module).grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 12, 0))

    def _make_card(self, parent, module_data, large=False):
        title, desc, icon, icon_bg, page_key, badge = module_data

        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )

        inner_pad = 20 if large else 16

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=inner_pad, pady=(inner_pad, 0))

        icon_label = ctk.CTkFrame(
            top_row,
            width=52, height=52,
            fg_color=icon_bg,
            corner_radius=12,
        )
        icon_label.pack_propagate(False)
        icon_label.pack(side="left")

        ctk.CTkLabel(
            icon_label,
            text=icon,
            font=("Inter", 22),
        ).place(relx=0.5, rely=0.5, anchor="center")

        if badge:
            badge_frame = ctk.CTkFrame(
                top_row,
                fg_color=COLORS["bg_elevated"],
                corner_radius=99,
                border_width=1,
                border_color=COLORS["border"],
            )
            badge_frame.pack(side="right")
            ctk.CTkLabel(
                badge_frame,
                text=badge,
                font=FONTS["body_sm"],
                text_color=COLORS["text_muted"],
            ).pack(padx=10, pady=4)

        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=inner_pad, pady=(16, 0))

        ctk.CTkLabel(
            card,
            text=desc,
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            wraplength=320 if large else 240,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=inner_pad, pady=(6, 0))

        link_btn = ctk.CTkButton(
            card,
            text="Start Simulation  →",
            font=("Inter", 12, "bold"),
            text_color=COLORS["secondary"],
            fg_color="transparent",
            hover_color=COLORS["bg_elevated"],
            anchor="w",
            command=lambda pk=page_key: self.navigate_callback(pk),
        )
        link_btn.pack(anchor="w", padx=inner_pad - 6, pady=(10, inner_pad))

        return card


class CPUSchedulingPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        self.processes = [
            {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"pid": "P2", "arrival": 1, "burst": 5, "priority": 1},
            {"pid": "P3", "arrival": 2, "burst": 4, "priority": 3},
            {"pid": "P4", "arrival": 6, "burst": 2, "priority": 4},
        ]

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_controls_panel()

    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.rowconfigure(2, weight=1)
        main.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main,
            text="CPU Scheduling Module",
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            main,
            text="Visualize and analyze process execution using various scheduling algorithms.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        self.progress_var = ctk.DoubleVar(value=0.0)
        progress_bar = ctk.CTkProgressBar(
            main,
            variable=self.progress_var,
            height=8,
            corner_radius=4,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["primary"],
        )
        progress_bar.grid(row=2, column=0, sticky="ew", pady=(0, 16))

        self._build_gantt_area(main, row=3)

        self._build_process_table(main, row=4)

    def _build_gantt_area(self, parent, row):
        container = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
            height=160,
        )
        container.grid(row=row, column=0, sticky="ew", pady=(0, 12))
        container.pack_propagate(False)
        self._gantt_container = container
        lbl = ctk.CTkLabel(
            container,
            text="Gantt chart will render here after running a simulation.",
            font=FONTS["body_md"],
            text_color=COLORS["text_muted"],
        )
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def _draw_gantt(self, timeline: list[dict]):
        try:
            if hasattr(self, "_gantt_canvas") and self._gantt_canvas is not None:
                self._gantt_canvas.get_tk_widget().destroy()
        except Exception:
            pass

        for w in self._gantt_container.winfo_children():
            w.destroy()

        if not timeline:
            ctk.CTkLabel(
                self._gantt_container,
                text="No timeline available for selected algorithm.",
                font=FONTS["body_md"],
                text_color=COLORS["text_muted"],
            ).place(relx=0.5, rely=0.5, anchor="center")
            return

        pids = list({entry["pid"] for entry in timeline})
        pid_earliest = {pid: min(e["start"] for e in timeline if e["pid"] == pid) for pid in pids}
        pids.sort(key=lambda pid: pid_earliest[pid])
        y_pos = {pid: (len(pids) - 1 - i) for i, pid in enumerate(pids)}

        fig, ax = plt.subplots(figsize=(6, 1.5 + 0.5 * len(pids)))

        for entry in timeline:
            pid = entry["pid"]
            start = entry["start"]
            finish = entry["finish"]
            ax.broken_barh([(start, finish - start)], (y_pos[pid] - 0.4, 0.8), facecolors=COLORS["primary"])

        ax.set_yticks([y_pos[pid] for pid in pids])
        ax.set_yticklabels(pids)
        ax.set_xlabel("Time")
        ax.set_xlim(left=0)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self._gantt_container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        self._gantt_canvas = canvas

    def _build_process_table(self, parent, row):
        table_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        table_frame.grid(row=row, column=0, sticky="nsew")
        parent.rowconfigure(row, weight=1)

        header_bar = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_bar.pack(fill="x", padx=20, pady=(16, 0))

        ctk.CTkLabel(
            header_bar,
            text="Process Queue",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        add_btn = ctk.CTkButton(
            header_bar,
            text="⊕  Add Process",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["bg_elevated"],
            command=self._on_add_process,
        )
        add_btn.pack(side="right")

        COLUMNS = [
            ("PID",          1),
            ("Arrival Time", 2),
            ("Burst Time",   2),
            ("Priority",     1),
            ("Remove",       1),
        ]

        col_header = ctk.CTkFrame(table_frame, fg_color="transparent")
        col_header.pack(fill="x", padx=20, pady=(12, 4))

        for i, (col_name, weight) in enumerate(COLUMNS):
            col_header.columnconfigure(i, weight=weight)
            ctk.CTkLabel(
                col_header,
                text=col_name,
                font=FONTS["body_sm"],
                text_color=COLORS["text_muted"],
                anchor="w" if i == 0 else "center",
            ).grid(row=0, column=i, sticky="ew")

        divider = ctk.CTkFrame(table_frame, fg_color=COLORS["border"], height=1)
        divider.pack(fill="x", padx=20, pady=(0, 4))

        self.table_scroll = ctk.CTkScrollableFrame(
            table_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        self.table_scroll.pack(fill="both", expand=True, padx=4, pady=(0, 12))
        self.table_scroll.columnconfigure(list(range(len(COLUMNS))), weight=1)

        self._col_count = len(COLUMNS)
        self._col_weights = [w for _, w in COLUMNS]

        self._refresh_table()

    def _refresh_table(self):
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        for i, proc in enumerate(self.processes):
            self._add_process_row(i, proc)

    def _add_process_row(self, row_index, proc):
        row_bg = COLORS["bg_elevated"] if row_index % 2 == 0 else "transparent"

        row_frame = ctk.CTkFrame(
            self.table_scroll,
            fg_color=row_bg,
            corner_radius=6,
            height=44,
        )
        row_frame.pack(fill="x", padx=8, pady=2)
        row_frame.pack_propagate(False)

        for i, weight in enumerate(self._col_weights):
            row_frame.columnconfigure(i, weight=weight)

        ctk.CTkLabel(
            row_frame,
            text=proc["pid"],
            font=FONTS["data_md"],
            text_color=COLORS["primary_light"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(12, 0))

        for col_idx, key in enumerate(["arrival", "burst", "priority"], start=1):
            ctk.CTkLabel(
                row_frame,
                text=str(proc[key]),
                font=FONTS["data_md"],
                text_color=COLORS["text_primary"],
                anchor="center",
            ).grid(row=0, column=col_idx, sticky="ew")

        ctk.CTkButton(
            row_frame,
            text="🗑",
            width=28, height=28,
            font=("Inter", 14),
            fg_color="transparent",
            text_color=COLORS["text_muted"],
            hover_color=COLORS["bg_elevated"],
            command=lambda pid=proc["pid"]: self._remove_process(pid),
        ).grid(row=0, column=4, sticky="ew")

    def _remove_process(self, pid):
        self.processes = [p for p in self.processes if p["pid"] != pid]
        self._refresh_table()

    def _on_add_process(self):
        name = self.proc_name_entry.get().strip()
        burst = self.burst_entry.get().strip()
        arrival = self.arrival_entry.get().strip()
        priority_val = "1"
        if hasattr(self, "priority_entry"):
            priority_val = self.priority_entry.get().strip() or "1"

        if not name or not burst.isdigit() or not arrival.isdigit():
            return

        new_proc = {
            "pid":      name,
            "arrival":  int(arrival),
            "burst":    int(burst),
            "priority": int(priority_val) if priority_val.isdigit() else 1,
        }
        self.processes.append(new_proc)
        self._refresh_table()

        self.proc_name_entry.delete(0, "end")
        self.burst_entry.delete(0, "end")
        self.arrival_entry.delete(0, "end")
        if hasattr(self, "priority_entry"):
            self.priority_entry.delete(0, "end")

    def _build_controls_panel(self):
        panel = ctk.CTkFrame(
            self,
            width=290,
            fg_color=COLORS["bg_panel"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_propagate(False)

        scroll = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        scroll.pack(fill="both", expand=True)

        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(20, 16))

        ctk.CTkLabel(
            header_row,
            text="≡  Controls",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="ALGORITHM",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.algo_var = ctk.StringVar(value="Round Robin (RR)")
        algo_options = [
            "Round Robin (RR)",
            "First Come First Served (FCFS)",
            "Shortest Job First (SJF)",
            "Shortest Job First (SJF) - Preemptive",
            "Priority Scheduling",
            "Priority Scheduling (Preemptive)",
            "Multilevel Queue",
        ]

        ctk.CTkOptionMenu(
            scroll,
            variable=self.algo_var,
            values=algo_options,
            font=FONTS["body_md"],
            dropdown_font=FONTS["body_md"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["bg_highest"],
            button_hover_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=16, pady=(0, 8))

        self._divider(scroll)

        tq_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tq_row.pack(fill="x", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            tq_row,
            text="TIME QUANTUM (MS)",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(side="left")

        self.tq_value_label = ctk.CTkLabel(
            tq_row,
            text="2",
            font=FONTS["metric_val"],
            text_color=COLORS["primary_light"],
        )
        self.tq_value_label.pack(side="right")

        self.tq_slider = ctk.CTkSlider(
            scroll,
            from_=1, to=10,
            number_of_steps=9,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["primary"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_light"],
            command=self._on_tq_change,
        )
        self.tq_slider.set(2)
        self.tq_slider.pack(fill="x", padx=16, pady=(6, 0))

        tick_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tick_row.pack(fill="x", padx=16)
        ctk.CTkLabel(tick_row, text="1", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkLabel(tick_row, text="5", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left", expand=True)
        ctk.CTkLabel(tick_row, text="10", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="right")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="PROCESS CONFIGURATION",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 8))

        ctk.CTkLabel(scroll, text="Process Name", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=16)
        self.proc_name_entry = ctk.CTkEntry(
            scroll,
            placeholder_text="e.g. P5",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.proc_name_entry.pack(fill="x", padx=16, pady=(4, 10))

        bt_at_row = ctk.CTkFrame(scroll, fg_color="transparent")
        bt_at_row.pack(fill="x", padx=16, pady=(0, 8))
        bt_at_row.columnconfigure(0, weight=1)
        bt_at_row.columnconfigure(1, weight=1)
        bt_at_row.columnconfigure(2, weight=1)

        ctk.CTkLabel(bt_at_row, text="Burst Time", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(bt_at_row, text="Arrival Time", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).grid(row=0, column=1, sticky="w", padx=(8, 0))
        ctk.CTkLabel(bt_at_row, text="Priority", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).grid(row=0, column=2, sticky="w", padx=(8, 0))
        self.burst_entry = ctk.CTkEntry(
            bt_at_row,
            placeholder_text="ms",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.burst_entry.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        self.arrival_entry = ctk.CTkEntry(
            bt_at_row,
            placeholder_text="ms",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.arrival_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(4, 0))

        self.priority_entry = ctk.CTkEntry(
            bt_at_row,
            placeholder_text="1",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.priority_entry.grid(row=1, column=2, sticky="ew", padx=(8, 0), pady=(4, 0))

        ctk.CTkButton(
            scroll,
            text="＋  Add to Queue",
            font=FONTS["button"],
            height=44,
            corner_radius=8,
            fg_color=COLORS["secondary"],
            text_color="#003827",
            hover_color=COLORS["secondary_dark"],
            command=self._on_add_process,
        ).pack(fill="x", padx=16, pady=(0, 16))

        self._divider(scroll)

        ctk.CTkButton(
            scroll,
            text="▶  Run Simulation",
            font=FONTS["button"],
            height=52,
            corner_radius=10,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_light"],
            text_color="#ffffff",
            command=self._on_run_simulation,
        ).pack(fill="x", padx=16, pady=16)

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="METRICS",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 8))

        self.metrics_data = {
            "avg_wait":    ("Avg Waiting Time",  "4.2 ms",  COLORS["text_primary"]),
            "avg_turn":    ("Avg Turnaround",    "8.5 ms",  COLORS["text_primary"]),
            "cpu_util":    ("CPU Utilization",   "92%",     COLORS["secondary"]),
        }

        self.metric_labels = {}
        for key, (label, value, color) in self.metrics_data.items():
            self._make_metric_row(scroll, key, label, value, color)

        ctk.CTkFrame(scroll, fg_color="transparent", height=20).pack()

    def _make_metric_row(self, parent, key, label, value, color):
        row = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_elevated"],
            corner_radius=8,
            height=40,
        )
        row.pack(fill="x", padx=16, pady=3)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=label,
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
        ).pack(side="left", padx=12)

        val_label = ctk.CTkLabel(
            row,
            text=value,
            font=FONTS["metric_val"],
            text_color=color,
        )
        val_label.pack(side="right", padx=12)
        self.metric_labels[key] = val_label

    def update_metric(self, key, new_value):
        if key in self.metric_labels:
            self.metric_labels[key].configure(text=new_value)

    def _divider(self, parent):
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=0, pady=4)

    def _on_tq_change(self, value):
        self.tq_value_label.configure(text=str(int(value)))

    def _on_run_simulation(self):
        algo = self.algo_var.get()
        tq = int(self.tq_slider.get())
        print(f"[Simulation] Algorithm: {algo}, Time Quantum: {tq}ms")
        print(f"[Simulation] Processes: {self.processes}")

        try:
            from algorithms import cpu_scheduling

            avg_wait, avg_turn, cpu_util, timeline = cpu_scheduling.run(algo, self.processes, tq)

            self.progress_var.set(1.0)
            self.update_metric("avg_wait", avg_wait)
            self.update_metric("avg_turn", avg_turn)
            self.update_metric("cpu_util", cpu_util)
            try:
                self._draw_gantt(timeline)
            except Exception as _:
                pass
        except Exception as exc:
            print("[Simulation] Error running CPU scheduling:", exc)
            self.progress_var.set(1.0)
            self.update_metric("avg_wait", "N/A")
            self.update_metric("avg_turn", "N/A")
            self.update_metric("cpu_util", "N/A")



class MemoryManagementPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        self.scheme_var = ctk.StringVar(value="MFT")
        self.mft_policy_var = ctk.StringVar(value="Best Available Fit")
        self.mvt_policy_var = ctk.StringVar(value="First Fit")
        self.compaction_var = ctk.StringVar(value="No Compaction")
        self.paging_view_var = ctk.StringVar(value="Allocation View")

        self.control_widgets = []
        self.last_result = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_parameters_panel()
        self._load_sample_values()
        self._draw_empty_state()

    # ---------- layout ----------
    def _build_main_area(self):
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.columnconfigure(0, weight=1)
        self.main_area = main

        ctk.CTkLabel(
            main,
            text="Memory Management Module",
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            main,
            text="Visualize MFT, MVT, and Paging allocation processes with policy-based memory maps.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 18))

        self.summary_row = ctk.CTkFrame(main, fg_color="transparent")
        self.summary_row.pack(fill="x", pady=(0, 14))
        self._make_summary_card("Scheme", "MFT", "scheme")
        self._make_summary_card("Policy", "Best Available Fit", "policy")
        self._make_summary_card("Mode", "Fixed Partitions", "mode")

        self.visual_card = ctk.CTkFrame(
            main,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self.visual_card.pack(fill="both", expand=True, pady=(0, 14))

        header = ctk.CTkFrame(self.visual_card, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(16, 8))
        ctk.CTkLabel(
            header,
            text="Memory Map Visualization",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")
        self.visual_hint = ctk.CTkLabel(
            header,
            text="Choose a scheme and run a simulation",
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
        )
        self.visual_hint.pack(side="right")

        self.canvas_holder = ctk.CTkFrame(self.visual_card, fg_color=COLORS["bg_card"], corner_radius=12)
        self.canvas_holder.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.memory_canvas = tk.Canvas(
            self.canvas_holder,
            bg=COLORS["bg_card"],
            highlightthickness=0,
            height=370,
        )
        self.memory_canvas.pack(fill="both", expand=True, padx=8, pady=8)

        bottom_grid = ctk.CTkFrame(main, fg_color="transparent")
        bottom_grid.pack(fill="both", expand=True)
        bottom_grid.columnconfigure(0, weight=2)
        bottom_grid.columnconfigure(1, weight=1)

        self.log_card = ctk.CTkFrame(
            bottom_grid,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self.log_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        ctk.CTkLabel(
            self.log_card,
            text="Process Steps",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 6))
        self.step_output = ctk.CTkTextbox(
            self.log_card,
            height=190,
            fg_color=COLORS["bg_card"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10,
            font=FONTS["data_sm"],
            text_color=COLORS["text_secondary"],
            wrap="word",
        )
        self.step_output.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.step_output.configure(state="disabled")

        self.result_card = ctk.CTkFrame(
            bottom_grid,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self.result_card.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(
            self.result_card,
            text="Results",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 6))
        self.results_box = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.results_box.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _make_summary_card(self, label, value, key):
        card = ctk.CTkFrame(
            self.summary_row,
            fg_color=COLORS["bg_panel"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        ctk.CTkLabel(
            card,
            text=label.upper(),
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=14, pady=(10, 0))
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=FONTS["metric_val"],
            text_color=COLORS["primary_light"],
            anchor="w",
        )
        value_label.pack(fill="x", padx=14, pady=(3, 10))
        setattr(self, f"summary_{key}", value_label)

    def _build_parameters_panel(self):
        self.params = ctk.CTkScrollableFrame(
            self,
            width=260,
            fg_color=COLORS["bg_panel"],
            corner_radius=0,
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        self.params.grid(row=0, column=1, sticky="nsew")
        self._rebuild_parameters()

    def _rebuild_parameters(self, *_):
        for widget in self.params.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.params,
            text="☰ Parameters",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=20, pady=(24, 22))

        self._section_label(self.params, "MEMORY SCHEME")
        ctk.CTkOptionMenu(
            self.params,
            variable=self.scheme_var,
            values=["MFT", "MVT", "Paging"],
            command=self._on_scheme_changed,
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_light"],
            dropdown_fg_color=COLORS["bg_elevated"],
            dropdown_hover_color=COLORS["bg_highest"],
            dropdown_text_color=COLORS["text_primary"],
            text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=20, pady=(0, 18))

        scheme = self.scheme_var.get()
        if scheme == "MFT":
            self._build_mft_controls()
        elif scheme == "MVT":
            self._build_mvt_controls()
        else:
            self._build_paging_controls()

        self._divider(self.params)
        ctk.CTkButton(
            self.params,
            text="▶  Run Simulation",
            font=FONTS["button"],
            height=44,
            corner_radius=8,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_light"],
            command=self._run_simulation,
        ).pack(fill="x", padx=20, pady=(16, 10))

        ctk.CTkButton(
            self.params,
            text="↻  Load Sample",
            font=FONTS["button"],
            height=40,
            corner_radius=8,
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_highest"],
            command=self._load_sample_values,
        ).pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(
            self.params,
            text="✕  Clear Output",
            font=FONTS["button"],
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            hover_color=COLORS["bg_elevated"],
            command=self._draw_empty_state,
        ).pack(fill="x", padx=20, pady=(0, 24))

    def _build_mft_controls(self):
        self._section_label(self.params, "ALLOCATION POLICY")
        ctk.CTkOptionMenu(
            self.params,
            variable=self.mft_policy_var,
            values=["Best Fit", "First Fit", "Best Available Fit"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            dropdown_hover_color=COLORS["bg_highest"],
            text_color=COLORS["text_primary"],
            dropdown_text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=20, pady=(0, 18))

        self._section_label(self.params, "FIXED PARTITIONS")
        self.mft_partitions_entry = self._entry(self.params, "10, 6, 4, 4")
        self._hint(self.params, "Example: 10, 6, 4, 4")

        self._section_label(self.params, "JOB QUEUE")
        self.mft_jobs_entry = self._entry(self.params, "A=2, B=3, C=4, D=5, E=6")
        self._hint(self.params, "Example: A=2, B=3, C=4")

    def _build_mvt_controls(self):
        self._section_label(self.params, "ALLOCATION POLICY")
        ctk.CTkOptionMenu(
            self.params,
            variable=self.mvt_policy_var,
            values=["First Fit", "Best Fit", "Worst Fit"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            dropdown_hover_color=COLORS["bg_highest"],
            text_color=COLORS["text_primary"],
            dropdown_text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=20, pady=(0, 18))

        self._section_label(self.params, "COMPACTION MODE")
        ctk.CTkOptionMenu(
            self.params,
            variable=self.compaction_var,
            values=["No Compaction", "With Compaction"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            dropdown_hover_color=COLORS["bg_highest"],
            text_color=COLORS["text_primary"],
            dropdown_text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=20, pady=(0, 18))

        self._section_label(self.params, "MEMORY SETTINGS")
        row = ctk.CTkFrame(self.params, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(0, 12))
        self.mvt_total_entry = self._small_entry(row, "256")
        self.mvt_os_entry = self._small_entry(row, "40")
        ctk.CTkLabel(row, text="Total", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=0, sticky="w", pady=(3,0))
        ctk.CTkLabel(row, text="OS", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=1, sticky="w", pady=(3,0), padx=(8,0))

        self._section_label(self.params, "INITIAL JOBS")
        self.mvt_initial_entry = self._entry(self.params, "A=70, B=40, C=60, D=30")
        self._section_label(self.params, "RELEASE JOBS")
        self.mvt_release_entry = self._entry(self.params, "B, D")
        self._hint(self.params, "These jobs finish first, creating scattered holes.")
        self._section_label(self.params, "INCOMING JOBS")
        self.mvt_incoming_entry = self._entry(self.params, "E=65")
        self._hint(self.params, "Use this to see the difference between compaction on/off.")

    def _build_paging_controls(self):
        self._section_label(self.params, "PAGING VIEW")
        ctk.CTkOptionMenu(
            self.params,
            variable=self.paging_view_var,
            values=["Allocation View", "Address Translation View"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            dropdown_hover_color=COLORS["bg_highest"],
            text_color=COLORS["text_primary"],
            dropdown_text_color=COLORS["text_primary"],
        ).pack(fill="x", padx=20, pady=(0, 18))

        self._section_label(self.params, "MEMORY SETTINGS")
        row1 = ctk.CTkFrame(self.params, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(0, 12))
        self.paging_total_entry = self._small_entry(row1, "256")
        self.paging_os_entry = self._small_entry(row1, "48")
        ctk.CTkLabel(row1, text="Total", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=0, sticky="w", pady=(3,0))
        ctk.CTkLabel(row1, text="OS", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=1, sticky="w", pady=(3,0), padx=(8,0))

        row2 = ctk.CTkFrame(self.params, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 12))
        self.paging_page_entry = self._small_entry(row2, "16")
        self.paging_job_entry = self._small_entry(row2, "30")
        ctk.CTkLabel(row2, text="Page Size", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=0, sticky="w", pady=(3,0))
        ctk.CTkLabel(row2, text="Job Size", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).grid(row=1, column=1, sticky="w", pady=(3,0), padx=(8,0))

        self._section_label(self.params, "LOGICAL ADDRESS")
        self.paging_la_entry = self._entry(self.params, "10")
        self._hint(self.params, "Uses p = LA / page size, d = LA % page size.")

    # ---------- parameter helpers ----------
    def _section_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
            anchor="w",
        ).pack(fill="x", padx=20, pady=(10, 7))

    def _hint(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=210,
            justify="left",
        ).pack(fill="x", padx=20, pady=(0, 10))

    def _entry(self, parent, placeholder):
        entry = ctk.CTkEntry(
            parent,
            height=34,
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            placeholder_text=placeholder,
            text_color=COLORS["text_primary"],
        )
        entry.pack(fill="x", padx=20, pady=(0, 8))
        entry.insert(0, placeholder)
        return entry

    def _small_entry(self, parent, text):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        entry = ctk.CTkEntry(
            parent,
            height=34,
            width=92,
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
        )
        col = len(parent.grid_slaves(row=0))
        entry.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 0))
        entry.insert(0, text)
        return entry

    def _divider(self, parent):
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=20, pady=(12, 4))

    # ---------- parsing ----------
    def _parse_sizes(self, text: str) -> list[int]:
        values = []
        for raw in text.replace(";", ",").split(","):
            item = raw.strip().upper().replace("K", "")
            if not item:
                continue
            values.append(int(item))
        return values

    def _parse_jobs(self, text: str, prefix="J") -> list[dict]:
        jobs = []
        auto = 1
        for raw in text.replace(";", ",").split(","):
            item = raw.strip().replace("K", "").replace("k", "")
            if not item:
                continue
            if "=" in item:
                name, size = item.split("=", 1)
                name = name.strip() or f"{prefix}{auto}"
            else:
                name, size = f"{prefix}{auto}", item
            jobs.append({"name": name.strip(), "size": int(size.strip())})
            auto += 1
        return jobs

    def _parse_names(self, text: str) -> list[str]:
        return [item.strip() for item in text.replace(";", ",").split(",") if item.strip()]

    # ---------- actions ----------
    def _on_scheme_changed(self, value=None):
        self._rebuild_parameters()
        self._load_sample_values()
        self._draw_empty_state()

    def _load_sample_values(self):
        scheme = self.scheme_var.get()
        if scheme == "MFT" and hasattr(self, "mft_partitions_entry"):
            self._set_entry(self.mft_partitions_entry, "10, 6, 4, 4")
            self._set_entry(self.mft_jobs_entry, "A=2, B=3, C=4, D=5, E=6")
        elif scheme == "MVT" and hasattr(self, "mvt_total_entry"):
            self._set_entry(self.mvt_total_entry, "256")
            self._set_entry(self.mvt_os_entry, "40")
            self._set_entry(self.mvt_initial_entry, "A=70, B=40, C=60, D=30")
            self._set_entry(self.mvt_release_entry, "B, D")
            self._set_entry(self.mvt_incoming_entry, "E=65")
        elif scheme == "Paging" and hasattr(self, "paging_total_entry"):
            self._set_entry(self.paging_total_entry, "256")
            self._set_entry(self.paging_os_entry, "48")
            self._set_entry(self.paging_page_entry, "16")
            self._set_entry(self.paging_job_entry, "30")
            self._set_entry(self.paging_la_entry, "10")

    def _set_entry(self, entry, text):
        entry.delete(0, "end")
        entry.insert(0, text)

    def _run_simulation(self):
        try:
            scheme = self.scheme_var.get()
            if scheme == "MFT":
                partitions = self._parse_sizes(self.mft_partitions_entry.get())
                jobs = self._parse_jobs(self.mft_jobs_entry.get())
                result = memalgo.simulate_mft(partitions, jobs, self.mft_policy_var.get())
                self._render_mft(result)
            elif scheme == "MVT":
                total = int(self.mvt_total_entry.get())
                os_size = int(self.mvt_os_entry.get())
                initial = self._parse_jobs(self.mvt_initial_entry.get())
                release = self._parse_names(self.mvt_release_entry.get())
                incoming = self._parse_jobs(self.mvt_incoming_entry.get())
                result = memalgo.simulate_mvt(
                    total,
                    os_size,
                    initial,
                    release,
                    incoming,
                    self.mvt_policy_var.get(),
                    self.compaction_var.get() == "With Compaction",
                )
                self._render_mvt(result)
            else:
                result = memalgo.simulate_paging(
                    int(self.paging_total_entry.get()),
                    int(self.paging_os_entry.get()),
                    int(self.paging_page_entry.get()),
                    int(self.paging_job_entry.get()),
                    int(self.paging_la_entry.get()),
                )
                self._render_paging(result)
        except Exception as exc:
            self._show_error(str(exc))

    def _draw_empty_state(self):
        self.memory_canvas.delete("all")
        self.memory_canvas.create_text(
            520, 160,
            text="Choose MFT, MVT, or Paging, then click Run Simulation.",
            fill=COLORS["text_muted"],
            font=("Inter", 13),
            anchor="center",
        )
        self.visual_hint.configure(text="Ready")
        self._set_steps("Simulation output will appear here.")
        self._set_results([("Status", "Waiting"), ("Scheme", self.scheme_var.get())])
        self._update_summary(self.scheme_var.get(), "Not run", "Visualization")

    def _show_error(self, message):
        self.memory_canvas.delete("all")
        self.memory_canvas.create_text(520, 160, text="Input Error", fill=COLORS["status_terminated_fg"], font=("Inter", 18, "bold"))
        self.memory_canvas.create_text(520, 190, text=message, fill=COLORS["text_secondary"], font=("Inter", 12), width=760)
        self._set_steps("Please check your input values.\n\n" + message)
        self._set_results([("Status", "Error")])

    # ---------- renderers ----------
    def _render_mft(self, result):
        self.visual_hint.configure(text="Fixed partitions · one job per region")
        self._update_summary("MFT", result["policy"], "Fixed Partitions")
        self.memory_canvas.delete("all")
        self._draw_mft_map(result)
        self._set_steps("\n".join(f"{i+1}. {step}" for i, step in enumerate(result["steps"])))
        waiting = ", ".join(f"{j['name']}({j['size']}K)" for j in result["waiting"]) or "None"
        allocated = sum(1 for p in result["partitions"] if p["job"])
        self._set_results([
            ("Allocated", f"{allocated}/{len(result['partitions'])}"),
            ("Waiting", waiting),
            ("Internal Frag", f"{result['total_internal']}K"),
        ])

    def _render_mvt(self, result):
        mode = "With Compaction" if result["compaction"] else "No Compaction"
        self.visual_hint.configure(text="Variable partitions · holes and free-space list")
        self._update_summary("MVT", result["policy"], mode)
        self.memory_canvas.delete("all")
        self._draw_mvt_map(result)
        self._set_steps("\n".join(f"{i+1}. {step}" for i, step in enumerate(result["steps"])))
        waiting = ", ".join(f"{j['name']}({j['size']}K)" for j in result["waiting"]) or "None"
        self._set_results([
            ("Free Total", f"{result['free_total']}K"),
            ("Largest Hole", f"{result['largest_hole']}K"),
            ("External Frag", f"{result['external_fragmentation']}K"),
            ("Compaction Used", "Yes" if result["compaction_used"] else "No"),
            ("Waiting", waiting),
        ])

    def _render_paging(self, result):
        self.visual_hint.configure(text="Pages, frames, page table, and address translation")
        self._update_summary("Paging", self.paging_view_var.get(), f"Page Size {result['page_size']}K")
        self.memory_canvas.delete("all")
        self._draw_paging_map(result)
        self._set_steps("\n".join(f"{i+1}. {step}" for i, step in enumerate(result["steps"])))
        address = result.get("address_result")
        physical = f"{address['pa']}K" if address else "Invalid"
        self._set_results([
            ("Frames", str(result["total_frames"])),
            ("Pages Needed", str(result["pages_needed"])),
            ("Internal Frag", f"{result['internal_fragmentation']}K"),
            ("Physical Addr", physical),
        ])

    def _update_summary(self, scheme, policy, mode):
        self.summary_scheme.configure(text=scheme)
        self.summary_policy.configure(text=policy)
        self.summary_mode.configure(text=mode)

    def _set_steps(self, text):
        self.step_output.configure(state="normal")
        self.step_output.delete("1.0", "end")
        self.step_output.insert("1.0", text)
        self.step_output.configure(state="disabled")

    def _set_results(self, rows):
        for widget in self.results_box.winfo_children():
            widget.destroy()
        for label, value in rows:
            row = ctk.CTkFrame(self.results_box, fg_color=COLORS["bg_card"], corner_radius=8)
            row.pack(fill="x", pady=(0, 8))
            ctk.CTkLabel(row, text=label, font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).pack(side="left", padx=10, pady=9)
            ctk.CTkLabel(row, text=str(value), font=FONTS["metric_val"], text_color=COLORS["secondary"]).pack(side="right", padx=10, pady=9)

    # ---------- canvas drawing helpers ----------
    def _draw_rounded_rect(self, x1, y1, x2, y2, fill, outline=None, width=1):
        # Canvas rounded rectangle approximation using normal rectangle for compatibility.
        self.memory_canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline or COLORS["border"], width=width)

    def _draw_mft_map(self, result):
        c = self.memory_canvas
        partitions = result["partitions"]
        total_user = sum(p["size"] for p in partitions) or 1
        bar_x, bar_y, bar_w, bar_h = 70, 40, 260, 290
        os_h = 40
        user_h = bar_h - os_h

        c.create_text(bar_x, 18, text="Fixed Partition Memory", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        c.create_rectangle(bar_x, bar_y + user_h, bar_x + bar_w, bar_y + bar_h, fill=COLORS["bg_highest"], outline=COLORS["border"])
        c.create_text(bar_x + bar_w/2, bar_y + user_h + os_h/2, text="OS", fill=COLORS["text_primary"], font=("Inter", 12, "bold"))

        y = bar_y + user_h
        for part in partitions:
            h = max(34, user_h * part["size"] / total_user)
            y -= h
            job = part["job"]
            base_fill = COLORS["status_waiting_bg"] if job else COLORS["bg_elevated"]
            c.create_rectangle(bar_x, y, bar_x + bar_w, y + h, fill=base_fill, outline=COLORS["border"], width=2)
            c.create_text(bar_x + 10, y + 15, text=f"Partition {part['index']} · {part['size']}K", fill=COLORS["text_secondary"], font=("Inter", 10), anchor="w")
            if job:
                frag = int(part["fragment"])
                used_ratio = job["size"] / part["size"] if part["size"] else 1
                used_h = max(18, h * used_ratio)
                c.create_rectangle(bar_x + 12, y + h - used_h - 6, bar_x + bar_w - 12, y + h - 6, fill=COLORS["primary"], outline="")
                c.create_text(bar_x + bar_w/2, y + h - used_h/2 - 6, text=f"{job['name']} = {job['size']}K", fill="#ffffff", font=("Inter", 11, "bold"))
                if frag > 0:
                    c.create_text(bar_x + bar_w - 12, y + 30, text=f"unused {frag}K", fill=COLORS["secondary"], font=("Inter", 10), anchor="e")
            else:
                c.create_text(bar_x + bar_w/2, y + h/2 + 8, text="Free", fill=COLORS["text_muted"], font=("Inter", 11))

        qx = 390
        c.create_text(qx, 42, text="Waiting Queue", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        waiting = result["waiting"]
        if not waiting:
            c.create_rectangle(qx, 66, qx + 450, 116, fill=COLORS["status_running_bg"], outline=COLORS["border"])
            c.create_text(qx + 225, 91, text="All possible jobs were allocated", fill=COLORS["secondary"], font=("Inter", 12, "bold"))
        else:
            for i, job in enumerate(waiting):
                x = qx + (i % 4) * 110
                y = 70 + (i // 4) * 62
                c.create_rectangle(x, y, x + 96, y + 44, fill=COLORS["bg_elevated"], outline=COLORS["border"])
                c.create_text(x + 48, y + 15, text=job["name"], fill=COLORS["text_primary"], font=("Inter", 11, "bold"))
                c.create_text(x + 48, y + 31, text=f"{job['size']}K", fill=COLORS["text_muted"], font=("Inter", 10))

        c.create_text(qx, 170, text="Allocated Partitions", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        for i, part in enumerate(partitions):
            job_text = f"{part['job']['name']} ({part['job']['size']}K)" if part["job"] else "Free"
            frag_text = f"Frag: {part['fragment']}K" if part["job"] else ""
            y = 198 + i * 28
            c.create_text(qx, y, text=f"P{part['index']} · {part['size']}K", fill=COLORS["text_secondary"], font=("JetBrains Mono", 10), anchor="w")
            c.create_text(qx + 150, y, text=job_text, fill=COLORS["primary_light"], font=("JetBrains Mono", 10), anchor="w")
            c.create_text(qx + 300, y, text=frag_text, fill=COLORS["secondary"], font=("JetBrains Mono", 10), anchor="w")

    def _draw_memory_bar(self, blocks, x, y, w, h, title):
        c = self.memory_canvas
        total = sum(block["size"] for block in blocks) or 1
        c.create_text(x, y - 20, text=title, fill=COLORS["text_primary"], font=("Inter", 13, "bold"), anchor="w")
        pos_y = y
        for block in blocks:
            bh = max(24, h * block["size"] / total)
            if block["type"] == "os":
                fill = COLORS["bg_highest"]
                text = f"OS · {block['size']}K"
            elif block["type"] == "hole":
                fill = COLORS["bg_elevated"]
                text = f"HOLE · {block['size']}K"
            else:
                fill = COLORS["primary"]
                text = f"{block['name']} · {block['size']}K"
            c.create_rectangle(x, pos_y, x + w, pos_y + bh, fill=fill, outline=COLORS["border"], width=2)
            color = COLORS["text_muted"] if block["type"] == "hole" else COLORS["text_primary"]
            c.create_text(x + w/2, pos_y + bh/2, text=text, fill=color, font=("Inter", 10, "bold"))
            c.create_text(x + w + 8, pos_y + 2, text=f"{block['start']}K", fill=COLORS["text_muted"], font=("JetBrains Mono", 9), anchor="nw")
            pos_y += bh
        c.create_text(x + w + 8, y + h - 10, text=f"{total}K", fill=COLORS["text_muted"], font=("JetBrains Mono", 9), anchor="nw")

    def _draw_mvt_map(self, result):
        stages = result["stages"]
        if result["compaction"] and result["compaction_used"]:
            before = next((s for s in stages if s["label"].startswith("Before Compaction")), stages[-2])
            after = next((s for s in stages if s["label"] == "After Compaction"), stages[-1])
            final = stages[-1]
            self._draw_memory_bar(before["blocks"], 55, 55, 180, 270, "Before Compaction")
            self._draw_memory_bar(after["blocks"], 330, 55, 180, 270, "After Compaction")
            self._draw_memory_bar(final["blocks"], 605, 55, 180, 270, "Final Allocation")
            self.memory_canvas.create_text(275, 180, text="→", fill=COLORS["secondary"], font=("Inter", 28, "bold"))
            self.memory_canvas.create_text(550, 180, text="→", fill=COLORS["secondary"], font=("Inter", 28, "bold"))
        else:
            final = stages[-1]
            self._draw_memory_bar(final["blocks"], 70, 55, 240, 270, "Final Memory Map")
            x = 380
            self.memory_canvas.create_text(x, 55, text="Free Space List", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
            holes = [b for b in final["blocks"] if b["type"] == "hole"]
            if not holes:
                self.memory_canvas.create_text(x, 90, text="No free holes", fill=COLORS["text_muted"], font=("Inter", 11), anchor="w")
            for i, hole in enumerate(holes):
                y = 86 + i * 34
                self.memory_canvas.create_rectangle(x, y, x + 340, y + 26, fill=COLORS["bg_elevated"], outline=COLORS["border"])
                self.memory_canvas.create_text(x + 12, y + 13, text=f"Start: {hole['start']}K", fill=COLORS["text_secondary"], font=("JetBrains Mono", 10), anchor="w")
                self.memory_canvas.create_text(x + 170, y + 13, text=f"Size: {hole['size']}K", fill=COLORS["secondary"], font=("JetBrains Mono", 10), anchor="w")
            y = 235
            self.memory_canvas.create_text(x, y, text="Fragmentation Check", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
            y += 32
            msg = f"Total free: {result['free_total']}K   Largest hole: {result['largest_hole']}K   External fragmentation: {result['external_fragmentation']}K"
            self.memory_canvas.create_text(x, y, text=msg, fill=COLORS["text_secondary"], font=("JetBrains Mono", 10), anchor="w")

    def _draw_paging_map(self, result):
        c = self.memory_canvas
        page_size = result["page_size"]
        pages = result["pages_needed"]
        address = result.get("address_result") if self.paging_view_var.get() == "Address Translation View" else None

        # Logical pages
        lx, ly, bw, bh = 60, 70, 130, 36
        c.create_text(lx, 42, text="Logical Pages", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        for p in range(pages):
            y = ly + p * (bh + 6)
            fill = COLORS["secondary_dark"] if address and p == address["p"] else COLORS["bg_elevated"]
            c.create_rectangle(lx, y, lx + bw, y + bh, fill=fill, outline=COLORS["border"], width=2)
            c.create_text(lx + bw/2, y + bh/2, text=f"Page {p}", fill=COLORS["text_primary"], font=("Inter", 11, "bold"))

        # Page table
        tx = 285
        c.create_text(tx, 42, text="Page Table", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        c.create_rectangle(tx, 70, tx + 210, 100, fill=COLORS["bg_highest"], outline=COLORS["border"])
        c.create_text(tx + 55, 85, text="Page", fill=COLORS["text_secondary"], font=("Inter", 10, "bold"))
        c.create_text(tx + 155, 85, text="Frame", fill=COLORS["text_secondary"], font=("Inter", 10, "bold"))
        for i, (page, frame) in enumerate(result["page_table"].items()):
            y = 100 + i * 30
            fill = COLORS["status_running_bg"] if address and page == address["p"] else COLORS["bg_card"]
            c.create_rectangle(tx, y, tx + 210, y + 30, fill=fill, outline=COLORS["border"])
            c.create_text(tx + 55, y + 15, text=str(page), fill=COLORS["text_primary"], font=("JetBrains Mono", 10))
            c.create_text(tx + 155, y + 15, text=str(frame), fill=COLORS["primary_light"], font=("JetBrains Mono", 10, "bold"))

        # Physical frames
        fx, fy, fw = 610, 40, 170
        c.create_text(fx, 20, text="Physical Frames", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
        total_frames = result["total_frames"]
        frame_h = min(25, 310 / max(1, total_frames))
        for item in result["frames"]:
            frame = item["frame"]
            y = fy + frame * frame_h
            if item["type"] == "os":
                fill = COLORS["bg_highest"]
            elif item["type"] == "page":
                fill = COLORS["secondary_dark"] if address and frame == address["f"] else COLORS["primary"]
            else:
                fill = COLORS["bg_elevated"]
            c.create_rectangle(fx, y, fx + fw, y + frame_h, fill=fill, outline=COLORS["border"])
            c.create_text(fx + 8, y + frame_h/2, text=f"F{frame}", fill=COLORS["text_secondary"], font=("JetBrains Mono", 9), anchor="w")
            c.create_text(fx + fw - 8, y + frame_h/2, text=item["label"], fill=COLORS["text_primary"], font=("JetBrains Mono", 9), anchor="e")

        if address:
            c.create_text(60, 315, text="Address Translation", fill=COLORS["text_primary"], font=("Inter", 14, "bold"), anchor="w")
            formula = f"LA {result['logical_address']}K → p={address['p']}, d={address['d']} → frame={address['f']} → PA={address['pa']}K"
            c.create_rectangle(60, 335, 780, 365, fill=COLORS["status_running_bg"], outline=COLORS["border"])
            c.create_text(70, 350, text=formula, fill=COLORS["secondary"], font=("JetBrains Mono", 11, "bold"), anchor="w")
        else:
            c.create_text(60, 335, text=f"Internal fragmentation: {result['internal_fragmentation']}K", fill=COLORS["secondary"], font=("JetBrains Mono", 11, "bold"), anchor="w")


class PlaceholderPage(ctk.CTkFrame):

    def __init__(self, master, title, icon, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        ctk.CTkLabel(
            self,
            text=icon,
            font=("Inter", 64),
        ).pack(pady=(80, 16))

        ctk.CTkLabel(
            self,
            text=title,
            font=FONTS["headline_md"],
            text_color=COLORS["text_primary"],
        ).pack()

        ctk.CTkLabel(
            self,
            text="This module is coming soon.\nReplace PlaceholderPage with your implementation.",
            font=FONTS["body_md"],
            text_color=COLORS["text_muted"],
            justify="center",
        ).pack(pady=(8, 0))


VM_ALGORITHMS = list(algorithms.REGISTRY.keys())


class VirtualMemoryPage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        self.ref_string = [7, 0, 1, 2, 0, 3]
        self.frame_count = 3
        self.page_faults = 0
        self.sim_steps = []

        self._selected_tile_idx: int | None = None

        self._counting_mode = "LFU"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_parameters_panel()

    def _build_main_area(self):
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.columnconfigure(0, weight=1)
        self._main_scroll = main

        ctk.CTkLabel(
            main,
            text="Virtual Memory Module",
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            main,
            text="Visualize and analyze page replacement algorithms in real-time.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 20))

        self._build_ref_queue_panel(main)

        ctk.CTkFrame(main, fg_color=COLORS["border"], height=1).pack(fill="x", pady=(16, 0))

        self._frames_container = ctk.CTkFrame(
            main,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self._frames_container.pack(fill="both", expand=True, pady=(16, 0))
        self._draw_frames_empty_state()

    def _build_ref_queue_panel(self, parent):
        panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.pack(fill="x")

        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 10))

        ctk.CTkLabel(
            header,
            text="[·]  Reference String Queue",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="✕  Remove All",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            hover_color=COLORS["status_terminated_bg"],
            command=self._remove_all_tiles,
        ).pack(side="right", padx=(0, 6))

        self._done_tile_btn = ctk.CTkButton(
            header,
            text="✓  Done",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color=COLORS["secondary"],
            text_color="#003827",
            hover_color=COLORS["secondary_dark"],
            state="disabled",
            command=self._deselect_tile,
        )
        self._done_tile_btn.pack(side="right", padx=(0, 6))

        self._remove_tile_btn = ctk.CTkButton(
            header,
            text="✕  Remove",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            hover_color=COLORS["status_terminated_bg"],
            state="disabled",
            command=self._remove_selected_tile,
        )
        self._remove_tile_btn.pack(side="right")

        tile_canvas_frame = ctk.CTkFrame(
            panel,
            fg_color=COLORS["bg"],
            corner_radius=10,
        )
        tile_canvas_frame.pack(fill="x", padx=20, pady=(0, 16))

        self._queue_tiles_frame = ctk.CTkScrollableFrame(
            tile_canvas_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=72,
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        self._queue_tiles_frame.pack(fill="x", padx=8, pady=8)

        self._refresh_queue_tiles()

    def _refresh_queue_tiles(self):
        for w in self._queue_tiles_frame.winfo_children():
            w.destroy()

        for idx, page_num in enumerate(self.ref_string):
            is_selected = (idx == self._selected_tile_idx)

            tile_bg     = COLORS["status_running_bg"] if is_selected else COLORS["bg_elevated"]
            tile_border = COLORS["secondary"]          if is_selected else COLORS["border"]
            text_color  = COLORS["secondary"]          if is_selected else COLORS["text_primary"]
            border_w    = 2                             if is_selected else 1

            tile_outer = ctk.CTkFrame(
                self._queue_tiles_frame,
                width=54, height=54,
                fg_color="transparent",
                corner_radius=11,
            )
            tile_outer.pack_propagate(False)
            tile_outer.pack(side="left", padx=(3, 3), pady=4)

            if is_selected:
                stripe = ctk.CTkFrame(
                    tile_outer,
                    width=4,
                    fg_color=COLORS["secondary"],
                    corner_radius=4,
                )
                stripe.pack(side="left", fill="y", padx=(0, 2))

            tile = ctk.CTkFrame(
                tile_outer,
                fg_color=tile_bg,
                corner_radius=10,
                border_width=border_w,
                border_color=tile_border,
            )
            tile.pack(fill="both", expand=True)

            ctk.CTkLabel(
                tile,
                text=str(page_num),
                font=("JetBrains Mono", 16, "bold"),
                text_color=text_color,
            ).place(relx=0.5, rely=0.5, anchor="center")

            for widget in (tile_outer, tile):
                widget.bind("<Button-1>", lambda e, i=idx: self._select_tile(i))
            for child in tile.winfo_children():
                child.bind("<Button-1>", lambda e, i=idx: self._select_tile(i))

    def _select_tile(self, idx: int):
        if self._selected_tile_idx == idx:
            self._selected_tile_idx = None
        else:
            self._selected_tile_idx = idx
        self._refresh_queue_tiles()
        state = "normal" if self._selected_tile_idx is not None else "disabled"
        self._remove_tile_btn.configure(state=state)
        self._done_tile_btn.configure(state=state)

    def _deselect_tile(self):
        self._selected_tile_idx = None
        self._refresh_queue_tiles()
        self._remove_tile_btn.configure(state="disabled")
        self._done_tile_btn.configure(state="disabled")

    def _remove_all_tiles(self):
        self.ref_string.clear()
        self._selected_tile_idx = None
        self._remove_tile_btn.configure(state="disabled")
        self._done_tile_btn.configure(state="disabled")
        self._refresh_queue_tiles()

    def _remove_selected_tile(self):
        idx = self._selected_tile_idx
        if idx is not None and 0 <= idx < len(self.ref_string):
            self.ref_string.pop(idx)
            self._selected_tile_idx = None
            self._remove_tile_btn.configure(state="disabled")
            self._done_tile_btn.configure(state="disabled")
            self._refresh_queue_tiles()

    def _draw_frames_empty_state(self):
        for w in self._frames_container.winfo_children():
            w.destroy()

        placeholder = ctk.CTkFrame(self._frames_container, fg_color="transparent")
        placeholder.pack(expand=True, fill="both", pady=40)

        ctk.CTkLabel(
            placeholder,
            text="▦",
            font=("Inter", 48),
            text_color=COLORS["text_muted"],
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            placeholder,
            text="Memory frames visualization will render here during simulation.\n"
                 "Configure parameters in the control panel to begin.",
            font=FONTS["body_md"],
            text_color=COLORS["text_muted"],
            justify="center",
        ).pack()

    def _draw_simulation_results(self):
        for w in self._frames_container.winfo_children():
            w.destroy()

        if not self.sim_steps:
            self._draw_frames_empty_state()
            return

        title_bar = ctk.CTkFrame(self._frames_container, fg_color="transparent")
        title_bar.pack(fill="x", padx=20, pady=(14, 8))
        ctk.CTkLabel(
            title_bar,
            text="Memory Frames — Step-by-Step",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        legend_frame = ctk.CTkFrame(title_bar, fg_color="transparent")
        legend_frame.pack(side="right")
        for dot, label in ((COLORS["primary_light"], "FAULT"), (COLORS["secondary"], "HIT")):
            ctk.CTkLabel(legend_frame, text="●", font=("Inter", 10), text_color=dot).pack(side="left", padx=(6, 1))
            ctk.CTkLabel(legend_frame, text=label, font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "VM.Treeview.Heading",
            background=COLORS["bg_highest"],
            foreground=COLORS["text_muted"],
            font=("Inter", 10, "bold"),
            relief="flat", borderwidth=0,
        )
        style.map("VM.Treeview.Heading",
                  background=[("active", COLORS["bg_highest"])])
        style.configure(
            "VM.Treeview",
            background=COLORS["bg_panel"],
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_panel"],
            font=("JetBrains Mono", 11),
            rowheight=32, borderwidth=0, relief="flat",
        )
        style.map("VM.Treeview",
                  background=[("selected", COLORS["bg_elevated"])],
                  foreground=[("selected", COLORS["text_primary"])])

        frame_col_ids = [f"f{i}" for i in range(self.frame_count)]
        col_ids = ["page"] + frame_col_ids + ["evicted", "status"]

        tree_wrapper = ctk.CTkFrame(
            self._frames_container,
            fg_color=COLORS["bg_panel"], corner_radius=0,
        )
        tree_wrapper.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        h_scroll = ttk.Scrollbar(tree_wrapper, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")
        v_scroll = ttk.Scrollbar(tree_wrapper, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        tree = ttk.Treeview(
            tree_wrapper, style="VM.Treeview",
            columns=col_ids, show="headings", selectmode="browse",
            xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set,
        )
        tree.pack(side="left", fill="both", expand=True)
        h_scroll.config(command=tree.xview)
        v_scroll.config(command=tree.yview)
        self._tree = tree

        tree.heading("page",    text="Page Ref",  anchor="center")
        tree.column( "page",    width=70, minwidth=60, stretch=False, anchor="center")
        for i in range(self.frame_count):
            tree.heading(f"f{i}",  text=f"Frame {i}", anchor="center")
            tree.column( f"f{i}",  width=66, minwidth=54, stretch=False, anchor="center")
        tree.heading("evicted", text="Evicted",    anchor="center")
        tree.column( "evicted", width=70, minwidth=60, stretch=False, anchor="center")
        tree.heading("status",  text="Status",     anchor="center")
        tree.column( "status",  width=70, minwidth=60, stretch=True,  anchor="center")

        tree.tag_configure("fault_step",
                           background=COLORS["icon_cpu"],
                           foreground=COLORS["primary_light"])
        tree.tag_configure("hit_step",
                           background=COLORS["status_running_bg"],
                           foreground=COLORS["secondary"])

        for step in self.sim_steps:
            page    = step["page"]
            frames  = step["frames"]
            fault   = step["fault"]
            evicted = step["evicted"]

            row = [str(page)]
            for slot in frames:
                row.append(str(slot) if slot is not None else "-")
            row.append(str(evicted) if evicted is not None else "-")
            row.append("FAULT" if fault else "HIT")

            tag = "fault_step" if fault else "hit_step"
            tree.insert("", "end", values=row, tags=(tag,))

    def _build_parameters_panel(self):
        panel = ctk.CTkFrame(
            self,
            width=300,
            fg_color=COLORS["bg_panel"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_propagate(False)

        scroll = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        scroll.pack(fill="both", expand=True)

        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(20, 16))

        ctk.CTkLabel(
            header_row,
            text="≡  Parameters",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Algorithm",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.vm_algo_var = ctk.StringVar(value=VM_ALGORITHMS[0])
        ctk.CTkOptionMenu(
            scroll,
            variable=self.vm_algo_var,
            values=VM_ALGORITHMS,
            font=FONTS["body_md"],
            dropdown_font=FONTS["body_md"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["bg_highest"],
            button_hover_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            text_color=COLORS["text_primary"],
            command=self._on_algo_change,
        ).pack(fill="x", padx=16, pady=(0, 8))

        self._lfu_mfu_frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg_elevated"], corner_radius=10)

        lfu_mfu_inner = ctk.CTkFrame(self._lfu_mfu_frame, fg_color="transparent")
        lfu_mfu_inner.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(
            lfu_mfu_inner,
            text="LFU",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        self._lfu_mfu_switch = ctk.CTkSwitch(
            lfu_mfu_inner,
            text="",
            width=46,
            onvalue="MFU",
            offvalue="LFU",
            fg_color=COLORS["border"],
            progress_color=COLORS["primary"],
            button_color=COLORS["text_primary"],
            button_hover_color=COLORS["primary_light"],
            command=self._on_lfu_mfu_toggle,
        )
        self._lfu_mfu_switch.pack(side="left", padx=8)

        ctk.CTkLabel(
            lfu_mfu_inner,
            text="MFU",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Frames in Memory",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        frames_row = ctk.CTkFrame(scroll, fg_color="transparent")
        frames_row.pack(fill="x", padx=16, pady=(0, 8))
        frames_row.columnconfigure(0, weight=1)
        frames_row.columnconfigure(1, weight=0)

        self.frames_slider = ctk.CTkSlider(
            frames_row,
            from_=1, to=10,
            number_of_steps=9,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["primary"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_light"],
            command=self._on_frames_change,
        )
        self.frames_slider.set(self.frame_count)
        self.frames_slider.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.frames_count_box = ctk.CTkFrame(
            frames_row,
            fg_color=COLORS["bg_elevated"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"],
            width=44, height=32,
        )
        self.frames_count_box.pack_propagate(False)
        self.frames_count_box.grid(row=0, column=1)

        self.frames_val_label = ctk.CTkLabel(
            self.frames_count_box,
            text=str(self.frame_count),
            font=FONTS["metric_val"],
            text_color=COLORS["text_primary"],
        )
        self.frames_val_label.place(relx=0.5, rely=0.5, anchor="center")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Add to Reference String",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        add_row = ctk.CTkFrame(scroll, fg_color="transparent")
        add_row.pack(fill="x", padx=16, pady=(0, 8))
        add_row.columnconfigure(0, weight=1)
        add_row.columnconfigure(1, weight=0)

        self.page_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Page #",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.page_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            add_row,
            text="＋",
            width=36, height=36,
            font=("Inter", 18, "bold"),
            corner_radius=8,
            fg_color=COLORS["bg_elevated"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            hover_color=COLORS["primary"],
            command=self._on_add_page,
        ).grid(row=0, column=1)

        self._divider(scroll)

        faults_box = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["bg"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        faults_box.pack(fill="x", padx=16, pady=(12, 8))

        ctk.CTkLabel(
            faults_box,
            text="PAGE FAULTS",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(pady=(12, 4))

        self.fault_count_label = ctk.CTkLabel(
            faults_box,
            text="0",
            font=("JetBrains Mono", 36, "bold"),
            text_color=COLORS["text_primary"],
        )
        self.fault_count_label.pack(pady=(0, 12))

        self._divider(scroll)

        ctk.CTkButton(
            scroll,
            text="▶  Run Simulation",
            font=FONTS["button"],
            height=52,
            corner_radius=10,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_light"],
            text_color="#ffffff",
            command=self._on_run_simulation,
        ).pack(fill="x", padx=16, pady=16)

        ctk.CTkFrame(scroll, fg_color="transparent", height=20).pack()

    def _on_frames_change(self, value):
        self.frame_count = int(value)
        self.frames_val_label.configure(text=str(self.frame_count))

    def _on_add_page(self):
        raw = self.page_entry.get().strip()
        if raw.isdigit():
            self.ref_string.append(int(raw))
            self._refresh_queue_tiles()
            self.page_entry.delete(0, "end")

    def _on_algo_change(self, algo: str):
        if "Counting" in algo:
            self._lfu_mfu_frame.pack(fill="x", padx=16, pady=(4, 8))
        else:
            self._lfu_mfu_frame.pack_forget()

    def _on_lfu_mfu_toggle(self):
        self._counting_mode = self._lfu_mfu_switch.get()

    def _on_run_simulation(self):
        algo_key = self.vm_algo_var.get()
        algo_module = algorithms.REGISTRY.get(algo_key)
        if algo_module is None:
            return

        if "Counting" in algo_key:
            self.sim_steps, self.page_faults = algo_module.run(
                self.ref_string, self.frame_count, mode=self._counting_mode
            )
        else:
            self.sim_steps, self.page_faults = algo_module.run(
                self.ref_string, self.frame_count
            )

        self.fault_count_label.configure(text=str(self.page_faults))
        self._draw_simulation_results()

    def _divider(self, parent):
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=0, pady=4)


DISK_ALGORITHMS = list(DISK_REGISTRY.keys())


class MassStoragePage(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        self.track_queue   = [98, 183, 37, 122, 14, 124, 65, 67]
        self.head_pos      = 53
        self.visit_order   = []
        self.total_movement = 0

        self._selected_tile_idx: int | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_config_panel()

    def _build_main_area(self):
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.columnconfigure(0, weight=1)
        self._main_scroll = main

        ctk.CTkLabel(
            main,
            text="Mass Storage Management Module",
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            main,
            text="Visualize and analyze disk scheduling algorithms in real-time.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 20))

        self._build_request_queue_panel(main)

        ctk.CTkFrame(main, fg_color=COLORS["border"], height=1).pack(fill="x", pady=(16, 0))

        self._graph_container = ctk.CTkFrame(
            main,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self._graph_container.pack(fill="both", expand=True, pady=(16, 0))
        self._draw_graph_empty_state()

    def _build_request_queue_panel(self, parent):
        panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.pack(fill="x")

        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 10))

        ctk.CTkLabel(
            header,
            text="[·]  Request Queue",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._queue_count_label = ctk.CTkLabel(
            header,
            text=f"Array [{len(self.track_queue)}]",
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
        )
        self._queue_count_label.pack(side="left", padx=10)

        ctk.CTkButton(
            header,
            text="✕  Remove All",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            hover_color=COLORS["status_terminated_bg"],
            command=self._remove_all_tracks,
        ).pack(side="right", padx=(0, 6))

        self._done_track_btn = ctk.CTkButton(
            header,
            text="✓  Done",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color=COLORS["secondary"],
            text_color="#003827",
            hover_color=COLORS["secondary_dark"],
            state="disabled",
            command=self._deselect_track,
        )
        self._done_track_btn.pack(side="right", padx=(0, 6))

        self._remove_track_btn = ctk.CTkButton(
            header,
            text="✕  Remove",
            font=FONTS["body_sm"],
            height=28,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_muted"],
            hover_color=COLORS["status_terminated_bg"],
            state="disabled",
            command=self._remove_selected_track,
        )
        self._remove_track_btn.pack(side="right")

        tile_canvas_frame = ctk.CTkFrame(
            panel,
            fg_color=COLORS["bg"],
            corner_radius=10,
        )
        tile_canvas_frame.pack(fill="x", padx=20, pady=(0, 16))

        self._queue_tiles_frame = ctk.CTkScrollableFrame(
            tile_canvas_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=72,
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        self._queue_tiles_frame.pack(fill="x", padx=8, pady=8)

        self._refresh_queue_tiles()

    def _refresh_queue_tiles(self):
        for w in self._queue_tiles_frame.winfo_children():
            w.destroy()

        for idx, track_num in enumerate(self.track_queue):
            is_selected = (idx == self._selected_tile_idx)

            tile_bg     = COLORS["status_running_bg"] if is_selected else COLORS["bg_elevated"]
            tile_border = COLORS["secondary"]          if is_selected else COLORS["border"]
            text_color  = COLORS["secondary"]          if is_selected else COLORS["text_primary"]
            border_w    = 2                             if is_selected else 1

            tile_outer = ctk.CTkFrame(
                self._queue_tiles_frame,
                width=58, height=54,
                fg_color="transparent",
                corner_radius=11,
            )
            tile_outer.pack_propagate(False)
            tile_outer.pack(side="left", padx=(3, 3), pady=4)

            if is_selected:
                stripe = ctk.CTkFrame(
                    tile_outer,
                    width=4,
                    fg_color=COLORS["secondary"],
                    corner_radius=4,
                )
                stripe.pack(side="left", fill="y", padx=(0, 2))

            tile = ctk.CTkFrame(
                tile_outer,
                fg_color=tile_bg,
                corner_radius=10,
                border_width=border_w,
                border_color=tile_border,
            )
            tile.pack(fill="both", expand=True)

            ctk.CTkLabel(
                tile,
                text=str(track_num),
                font=("JetBrains Mono", 14, "bold"),
                text_color=text_color,
            ).place(relx=0.5, rely=0.5, anchor="center")

            for widget in (tile_outer, tile):
                widget.bind("<Button-1>", lambda e, i=idx: self._select_track(i))
            for child in tile.winfo_children():
                child.bind("<Button-1>", lambda e, i=idx: self._select_track(i))

        if hasattr(self, "_queue_count_label"):
            self._queue_count_label.configure(text=f"Array [{len(self.track_queue)}]")

    def _select_track(self, idx: int):
        self._selected_tile_idx = None if self._selected_tile_idx == idx else idx
        self._refresh_queue_tiles()
        state = "normal" if self._selected_tile_idx is not None else "disabled"
        self._remove_track_btn.configure(state=state)
        self._done_track_btn.configure(state=state)

    def _deselect_track(self):
        self._selected_tile_idx = None
        self._refresh_queue_tiles()
        self._remove_track_btn.configure(state="disabled")
        self._done_track_btn.configure(state="disabled")

    def _remove_selected_track(self):
        idx = self._selected_tile_idx
        if idx is not None and 0 <= idx < len(self.track_queue):
            self.track_queue.pop(idx)
            self._selected_tile_idx = None
            self._remove_track_btn.configure(state="disabled")
            self._done_track_btn.configure(state="disabled")
            self._refresh_queue_tiles()

    def _remove_all_tracks(self):
        self.track_queue.clear()
        self._selected_tile_idx = None
        if hasattr(self, "_remove_track_btn"):
            self._remove_track_btn.configure(state="disabled")
            self._done_track_btn.configure(state="disabled")
        self._refresh_queue_tiles()

    def _draw_graph_empty_state(self):
        for w in self._graph_container.winfo_children():
            w.destroy()

        title_bar = ctk.CTkFrame(self._graph_container, fg_color="transparent")
        title_bar.pack(fill="x", padx=20, pady=(14, 8))
        ctk.CTkLabel(
            title_bar,
            text="≈  Disk Scheduling Graph",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        placeholder = ctk.CTkFrame(self._graph_container, fg_color="transparent")
        placeholder.pack(expand=True, fill="both", pady=40)

        ctk.CTkLabel(
            placeholder,
            text="💿",
            font=("Inter", 48),
            text_color=COLORS["text_muted"],
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            placeholder,
            text="Disk scheduling graph will render here after simulation.\n"
                 "Configure parameters in the panel and click Run Simulation.",
            font=FONTS["body_md"],
            text_color=COLORS["text_muted"],
            justify="center",
        ).pack()

    def _draw_graph(self):
        for w in self._graph_container.winfo_children():
            w.destroy()

        title_bar = ctk.CTkFrame(self._graph_container, fg_color="transparent")
        title_bar.pack(fill="x", padx=20, pady=(14, 8))

        ctk.CTkLabel(
            title_bar,
            text="≈  Disk Scheduling Graph",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        legend_frame = ctk.CTkFrame(title_bar, fg_color="transparent")
        legend_frame.pack(side="right")
        ctk.CTkLabel(
            legend_frame, text="●", font=("Inter", 10),
            text_color=COLORS["primary"]
        ).pack(side="left", padx=(0, 3))
        ctk.CTkLabel(
            legend_frame, text="Head Path", font=FONTS["body_sm"],
            text_color=COLORS["text_muted"]
        ).pack(side="left")

        algo_name = self.disk_algo_var.get()
        is_cscan  = (algo_name == "C-Scan")

        numeric_order = [int(t.rstrip("+")) for t in self.visit_order]
        full_sequence = [self.head_pos] + numeric_order

        bg     = "#111316"
        panel  = "#1e2023"
        accent = "#4a8eff"
        muted  = "#8b90a0"
        txt    = "#e2e2e6"

        fig, ax = plt.subplots(figsize=(7, 4.5))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(panel)

        n = len(full_sequence)

        for i in range(n - 1):
            x0, x1 = full_sequence[i], full_sequence[i + 1]
            y0, y1 = i, i + 1

            is_jump = is_cscan and (x0 - x1) > 50

            color      = "#ff6b6b" if is_jump else accent
            linestyle  = "dashed"  if is_jump else "solid"
            lw         = 1.2       if is_jump else 1.8

            ax.annotate(
                "",
                xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(
                    arrowstyle="->",
                    color=color,
                    lw=lw,
                    linestyle=linestyle,
                    connectionstyle="arc3,rad=0.0",
                ),
            )

        for i, pos in enumerate(full_sequence):
            dot_color = "#44dfab" if i == 0 else accent
            ax.plot(pos, i, "o", color=dot_color, markersize=6, zorder=5)
            ax.text(
                pos, i - 0.35,
                str(pos),
                ha="center", va="bottom",
                fontsize=7.5, color=txt,
                fontfamily="monospace",
            )

        ax.set_ylim(n, -0.8)
        ax.set_yticks(range(n))
        y_labels = ["Head"] + [str(v) for v in self.visit_order]
        ax.set_yticklabels(y_labels, fontsize=8, color=muted)

        ax.set_xlabel("Disk Track", color=muted, fontsize=9)
        ax.tick_params(axis="x", colors=muted, labelsize=8)
        ax.tick_params(axis="y", colors=muted, labelsize=8)

        ax.set_title(
            f"{algo_name}  —  Total Movement: {self.total_movement} tracks",
            color=txt, fontsize=10, pad=10,
        )

        for spine in ax.spines.values():
            spine.set_edgecolor("#414754")
        ax.grid(axis="x", color="#414754", linestyle="--", linewidth=0.5, alpha=0.5)

        fig.tight_layout(pad=1.2)

        canvas_widget = ctk.CTkFrame(
            self._graph_container,
            fg_color=bg,
            corner_radius=10,
        )
        canvas_widget.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        canvas = FigureCanvasTkAgg(fig, master=canvas_widget)
        canvas.draw()
        canvas.get_tk_widget().configure(bg=bg, highlightthickness=0)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)

    def _build_config_panel(self):
        panel = ctk.CTkFrame(
            self,
            width=300,
            fg_color=COLORS["bg_panel"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_propagate(False)

        scroll = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        scroll.pack(fill="both", expand=True)

        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(20, 16))

        ctk.CTkLabel(
            header_row,
            text="≡  Configuration",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Scheduling Algorithm",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.disk_algo_var = ctk.StringVar(value=DISK_ALGORITHMS[0])
        ctk.CTkOptionMenu(
            scroll,
            variable=self.disk_algo_var,
            values=DISK_ALGORITHMS,
            font=FONTS["body_md"],
            dropdown_font=FONTS["body_md"],
            fg_color=COLORS["bg_elevated"],
            button_color=COLORS["bg_highest"],
            button_hover_color=COLORS["primary"],
            dropdown_fg_color=COLORS["bg_elevated"],
            text_color=COLORS["text_primary"],
            command=self._on_algo_change,
        ).pack(fill="x", padx=16, pady=(0, 8))

        self._divider(scroll)

        self._direction_frame = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["bg_elevated"],
            corner_radius=10,
        )

        dir_inner = ctk.CTkFrame(self._direction_frame, fg_color="transparent")
        dir_inner.pack(fill="x", padx=14, pady=10)

        ctk.CTkLabel(
            dir_inner,
            text="Direction",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(0, 6))

        dir_row = ctk.CTkFrame(dir_inner, fg_color="transparent")
        dir_row.pack(fill="x")

        self._dir_down_label = ctk.CTkLabel(
            dir_row,
            text="↓  DOWN",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        )
        self._dir_down_label.pack(side="left")

        self._direction_switch = ctk.CTkSwitch(
            dir_row,
            text="",
            width=46,
            onvalue="up",
            offvalue="down",
            fg_color=COLORS["border"],
            progress_color=COLORS["primary"],
            button_color=COLORS["text_primary"],
            button_hover_color=COLORS["primary_light"],
            command=self._on_direction_change,
        )
        self._direction_switch.select()
        self._direction_switch.pack(side="left", padx=8)

        self._dir_up_label = ctk.CTkLabel(
            dir_row,
            text="↑  UP",
            font=("Inter", 11, "bold"),
            text_color=COLORS["primary_light"],
        )
        self._dir_up_label.pack(side="left")

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Disk Size (tracks)",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.disk_size_entry = ctk.CTkEntry(
            scroll,
            placeholder_text="e.g. 200",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.disk_size_entry.insert(0, "200")
        self.disk_size_entry.pack(fill="x", padx=16, pady=(0, 8))

        self._divider(scroll)

        if DISK_ALGORITHMS[0] in DIRECTION_ALGORITHMS:
            self._direction_frame.pack(fill="x", padx=16, pady=(4, 0))
            self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Current Head Position",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        head_row = ctk.CTkFrame(scroll, fg_color="transparent")
        head_row.pack(fill="x", padx=16, pady=(0, 8))
        head_row.columnconfigure(0, weight=1)
        head_row.columnconfigure(1, weight=0)

        self.head_entry = ctk.CTkEntry(
            head_row,
            placeholder_text="e.g. 53",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.head_entry.insert(0, str(self.head_pos))
        self.head_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            head_row,
            text="↺",
            width=36, height=36,
            font=("Inter", 18),
            corner_radius=8,
            fg_color=COLORS["bg_elevated"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            hover_color=COLORS["primary"],
            command=self._on_reset_head,
        ).grid(row=0, column=1)

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="Add Track Request",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        track_row = ctk.CTkFrame(scroll, fg_color="transparent")
        track_row.pack(fill="x", padx=16, pady=(0, 8))
        track_row.columnconfigure(0, weight=1)
        track_row.columnconfigure(1, weight=0)

        self.track_entry = ctk.CTkEntry(
            track_row,
            placeholder_text="e.g. 150",
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.track_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            track_row,
            text="＋",
            width=36, height=36,
            font=("Inter", 18, "bold"),
            corner_radius=8,
            fg_color=COLORS["bg_elevated"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            hover_color=COLORS["primary"],
            command=self._on_add_track,
        ).grid(row=0, column=1)

        self._divider(scroll)

        movement_box = ctk.CTkFrame(
            scroll,
            fg_color=COLORS["bg"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        movement_box.pack(fill="x", padx=16, pady=(12, 8))

        ctk.CTkLabel(
            movement_box,
            text="TOTAL MOVEMENT",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(pady=(12, 4))

        self.movement_label = ctk.CTkLabel(
            movement_box,
            text="0",
            font=("JetBrains Mono", 36, "bold"),
            text_color=COLORS["text_primary"],
        )
        self.movement_label.pack(pady=(0, 4))

        ctk.CTkLabel(
            movement_box,
            text="tracks",
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
        ).pack(pady=(0, 12))

        self._divider(scroll)

        ctk.CTkLabel(
            scroll,
            text="DISK MOVEMENT",
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.movement_output = ctk.CTkTextbox(
            scroll,
            height=80,
            font=FONTS["data_sm"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
            wrap="word",
            state="disabled",
        )
        self.movement_output.pack(fill="x", padx=16, pady=(0, 8))

        self._divider(scroll)

        ctk.CTkButton(
            scroll,
            text="▶  Run Simulation",
            font=FONTS["button"],
            height=52,
            corner_radius=10,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_light"],
            text_color="#ffffff",
            command=self._on_run_simulation,
        ).pack(fill="x", padx=16, pady=16)

        ctk.CTkFrame(scroll, fg_color="transparent", height=20).pack()

    def _on_reset_head(self):
        self.head_entry.delete(0, "end")
        self.head_entry.insert(0, str(self.head_pos))

    def _on_add_track(self):
        raw = self.track_entry.get().strip()
        if raw.isdigit():
            val = int(raw)
            disk_sz = self._get_disk_size()
            if 0 <= val < disk_sz:
                self.track_queue.append(val)
                self._refresh_queue_tiles()
                self.track_entry.delete(0, "end")

    def _on_algo_change(self, algo: str):
        if algo in DIRECTION_ALGORITHMS:
            self._direction_frame.pack(fill="x", padx=16, pady=(4, 0))
        else:
            self._direction_frame.pack_forget()

    def _on_direction_change(self):
        direction = self._direction_switch.get()
        if direction == "up":
            self._dir_up_label.configure(
                font=("Inter", 11, "bold"), text_color=COLORS["primary_light"]
            )
            self._dir_down_label.configure(
                font=FONTS["body_sm"], text_color=COLORS["text_secondary"]
            )
        else:
            self._dir_down_label.configure(
                font=("Inter", 11, "bold"), text_color=COLORS["primary_light"]
            )
            self._dir_up_label.configure(
                font=FONTS["body_sm"], text_color=COLORS["text_secondary"]
            )

    def _get_disk_size(self) -> int:
        raw = self.disk_size_entry.get().strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        return 200

    def _on_run_simulation(self):
        raw_head = self.head_entry.get().strip()
        if not raw_head.isdigit():
            return
        self.head_pos = int(raw_head)

        if not self.track_queue:
            return

        algo_name = self.disk_algo_var.get()
        algo_fn   = DISK_REGISTRY.get(algo_name)
        if algo_fn is None:
            return

        disk_size = self._get_disk_size()
        direction = self._direction_switch.get()

        self.visit_order, raw_total = algo_fn(
            list(self.track_queue), self.head_pos,
            disk_size=disk_size, direction=direction,
        )

        if isinstance(raw_total, str):
            self.total_movement = int(raw_total.rstrip("+"))
            total_display = raw_total
        else:
            self.total_movement = raw_total
            total_display = str(raw_total)

        self.movement_label.configure(text=total_display)

        order_str = " → ".join([str(self.head_pos)] + self.visit_order)
        self.movement_output.configure(state="normal")
        self.movement_output.delete("1.0", "end")
        self.movement_output.insert("1.0", order_str)
        self.movement_output.configure(state="disabled")

        self._draw_graph()

    def _divider(self, parent):
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=0, pady=4)


class OSSimulatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("OS Algorithm Simulator")
        self.geometry("1280x820")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=COLORS["bg"])

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, navigate_callback=self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self._build_pages()

        self.navigate("Home")

    def _build_pages(self):
        self.pages = {}

        home = HomePage(self.content, navigate_callback=self.navigate)
        home.grid(row=0, column=0, sticky="nsew")
        self.pages["Home"] = home

        cpu = CPUSchedulingPage(self.content)
        cpu.grid(row=0, column=0, sticky="nsew")
        self.pages["CPU Scheduling"] = cpu

        memory = MemoryManagementPage(self.content)
        memory.grid(row=0, column=0, sticky="nsew")
        self.pages["Memory Management"] = memory

        vm = VirtualMemoryPage(self.content)
        vm.grid(row=0, column=0, sticky="nsew")
        self.pages["Virtual Memory"] = vm

        disk = MassStoragePage(self.content)
        disk.grid(row=0, column=0, sticky="nsew")
        self.pages["Disk Management"] = disk

        placeholder_modules = [
            ("Security Management", "Security Management", "🛡"),
        ]
        for page_key, title, icon in placeholder_modules:
            page = PlaceholderPage(self.content, title=title, icon=icon)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[page_key] = page

    def navigate(self, page_key):
        if page_key in self.pages:
            self.pages[page_key].tkraise()
            self.sidebar.set_active(page_key)


if __name__ == "__main__":
    app = OSSimulatorApp()
    app.mainloop()