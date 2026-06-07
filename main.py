import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

import algorithms

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
            {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2, "status": "Waiting"},
            {"pid": "P2", "arrival": 1, "burst": 5, "priority": 1, "status": "Terminated"},
            {"pid": "P3", "arrival": 2, "burst": 4, "priority": 3, "status": "Running"},
            {"pid": "P4", "arrival": 6, "burst": 2, "priority": 4, "status": "Ready"},
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

        self._build_process_table(main, row=3)

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
            ("Status",       2),
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

        status = proc["status"]
        chip_colors = {
            "Running":    (COLORS["status_running_bg"],    COLORS["status_running_fg"]),
            "Waiting":    (COLORS["status_waiting_bg"],    COLORS["status_waiting_fg"]),
            "Terminated": (COLORS["status_terminated_bg"], COLORS["status_terminated_fg"]),
            "Ready":      (COLORS["status_ready_bg"],      COLORS["status_ready_fg"]),
        }
        chip_bg, chip_fg = chip_colors.get(status, (COLORS["bg_elevated"], COLORS["text_primary"]))

        status_text = f"● {status}" if status == "Running" else status

        chip_wrapper = ctk.CTkFrame(row_frame, fg_color="transparent")
        chip_wrapper.grid(row=0, column=4, sticky="ew")

        chip = ctk.CTkFrame(
            chip_wrapper,
            fg_color=chip_bg,
            corner_radius=99,
        )
        chip.pack(anchor="center")
        ctk.CTkLabel(
            chip,
            text=status_text,
            font=FONTS["body_sm"],
            text_color=chip_fg,
        ).pack(padx=10, pady=3)

        ctk.CTkButton(
            row_frame,
            text="🗑",
            width=28, height=28,
            font=("Inter", 14),
            fg_color="transparent",
            text_color=COLORS["text_muted"],
            hover_color=COLORS["bg_elevated"],
            command=lambda pid=proc["pid"]: self._remove_process(pid),
        ).grid(row=0, column=5, sticky="ew")

    def _remove_process(self, pid):
        self.processes = [p for p in self.processes if p["pid"] != pid]
        self._refresh_table()

    def _on_add_process(self):
        name = self.proc_name_entry.get().strip()
        burst = self.burst_entry.get().strip()
        arrival = self.arrival_entry.get().strip()

        if not name or not burst.isdigit() or not arrival.isdigit():
            return

        new_proc = {
            "pid":      name,
            "arrival":  int(arrival),
            "burst":    int(burst),
            "priority": 1,
            "status":   "Ready",
        }
        self.processes.append(new_proc)
        self._refresh_table()

        self.proc_name_entry.delete(0, "end")
        self.burst_entry.delete(0, "end")
        self.arrival_entry.delete(0, "end")

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
            "Priority Scheduling",
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

        ctk.CTkLabel(bt_at_row, text="Burst Time", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(bt_at_row, text="Arrival Time", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).grid(row=0, column=1, sticky="w", padx=(8, 0))

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

        self.progress_var.set(1.0)

        self.update_metric("avg_wait", "4.2 ms")
        self.update_metric("avg_turn", "8.5 ms")
        self.update_metric("cpu_util", "92%")

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

    def _remove_selected_tile(self):
        idx = self._selected_tile_idx
        if idx is not None and 0 <= idx < len(self.ref_string):
            self.ref_string.pop(idx)
            self._selected_tile_idx = None
            self._remove_tile_btn.configure(state="disabled")
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

        vm = VirtualMemoryPage(self.content)
        vm.grid(row=0, column=0, sticky="nsew")
        self.pages["Virtual Memory"] = vm

        placeholder_modules = [
            ("Memory Management",   "Memory Management",   "🗂"),
            ("Disk Management",     "Disk Management",     "💾"),
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
