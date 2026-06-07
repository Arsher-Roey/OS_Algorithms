import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

# Algorithm modules (modular — one file per algorithm in algorithms/)
import algorithms  # noqa: E402  (algorithms/__init__.py provides REGISTRY)


# =============================================================================
# [COLORS] - Design System Color Palette ("Systemic Precision")
# Change any hex value here to update that color everywhere in the app.
# =============================================================================
COLORS = {
    # Backgrounds (layered from darkest to brightest)
    "bg":               "#111316",   # Main app background (deepest layer)
    "bg_panel":         "#1e2023",   # Panel/card background
    "bg_card":          "#1a1c1f",   # Slightly lighter card surface
    "bg_elevated":      "#282a2d",   # Elevated elements (rows, inputs)
    "bg_highest":       "#333538",   # Highest surface (e.g. active nav item)

    # Sidebar
    "sidebar_bg":       "#111316",   # Sidebar background color
    "sidebar_active":   "#1e2023",   # Active nav item background
    "sidebar_border":   "#4a8eff",   # Blue left-border on active nav item

    # Text colors
    "text_primary":     "#e2e2e6",   # Main readable text (white-ish)
    "text_secondary":   "#c1c6d7",   # Subdued/label text
    "text_muted":       "#8b90a0",   # Hint/placeholder text
    "text_accent":      "#adc7ff",   # Light-blue accented text

    # Brand / Interactive
    "primary":          "#4a8eff",   # Electric blue (primary action color)
    "primary_light":    "#adc7ff",   # Lighter blue (headings, links)
    "secondary":        "#44dfab",   # Teal (secondary actions, "Start Simulation")
    "secondary_dark":   "#00bf8e",   # Darker teal

    # Borders / Dividers
    "border":           "#414754",   # Standard border/outline
    "border_focus":     "#4a8eff",   # Focus border (glows electric blue)

    # Status chip colors — change these to adjust process state badges
    "status_running_bg":     "#003827",   # Running chip background
    "status_running_fg":     "#44dfab",   # Running chip text
    "status_waiting_bg":     "#1e2a3a",   # Waiting chip background
    "status_waiting_fg":     "#adc7ff",   # Waiting chip text
    "status_terminated_bg":  "#2a1a1a",   # Terminated chip background
    "status_terminated_fg":  "#ffb4ab",   # Terminated chip text
    "status_ready_bg":       "#2a2a1a",   # Ready chip background
    "status_ready_fg":       "#e2e2e6",   # Ready chip text

    # Module card icon backgrounds
    "icon_cpu":     "#1a2a3a",   # CPU card icon bg
    "icon_mem":     "#1a2d2a",   # Memory card icon bg
    "icon_virt":    "#2d1a10",   # Virtual Memory icon bg
    "icon_disk":    "#1a2040",   # Disk Management icon bg
    "icon_sec":     "#2d1a1a",   # Security icon bg
}


# =============================================================================
# [FONTS] - Typography Definitions
# Change font sizes and weights here to apply globally.
# Font families: "Inter" for UI text, "JetBrains Mono" for data/tables.
# If these fonts aren't installed, CustomTkinter falls back to system fonts.
# =============================================================================
FONTS = {
    "headline_lg": ("Inter", 28, "bold"),       # Page titles (e.g. "Hi, what do you want to do?")
    "headline_md": ("Inter", 20, "bold"),       # Section headers
    "headline_sm": ("Inter", 15, "bold"),       # Card titles / nav labels
    "body_md":     ("Inter", 13, "normal"),     # Descriptions, body copy
    "body_sm":     ("Inter", 11, "normal"),     # Captions, small labels
    "label_caps":  ("Inter", 10, "bold"),       # ALL-CAPS section labels (e.g. "ALGORITHM")
    "data_md":     ("JetBrains Mono", 12, "normal"),  # Table cell data
    "data_sm":     ("JetBrains Mono", 11, "normal"),  # Smaller table data
    "nav":         ("Inter", 13, "normal"),     # Sidebar nav item text
    "button":      ("Inter", 13, "bold"),       # Button labels
    "metric_val":  ("JetBrains Mono", 13, "bold"),    # Metric values (e.g. "4.2 ms")
}


# =============================================================================
# [ABOUT US] - About Us card content
# Change the text here to update the About Us section in the sidebar.
# =============================================================================
ABOUT_US_TEXT = (
    "The OS Simulator project is an educational platform designed to "
    "visualize complex kernel operations. Developed for students and "
    "enthusiasts to explore low-level system logic through interactive, "
    "real-time algorithmic execution."
)


# =============================================================================
# [SIDEBAR] - Left Navigation Panel
# Handles the fixed sidebar with navigation items and About Us card.
# =============================================================================
class Sidebar(ctk.CTkFrame):
    """
    The persistent left sidebar that holds:
      - App logo + branding
      - Navigation buttons (Home, CPU Scheduling, etc.)
      - About Us card at the bottom

    To add a new nav item:
      1. Add an entry to self.nav_items list: ("Label", callback_function)
      2. The button will be created automatically in _build_nav()
    """

    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(
            master,
            width=240,                          # [CHANGE] Sidebar width in pixels
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs
        )
        self.grid_propagate(False)              # Keep fixed width
        self.navigate_callback = navigate_callback
        self.active_page = "Home"
        self.nav_buttons = {}

        self._build_logo()
        self._build_nav()
        self._build_about_us()

    # ─── Logo / Branding ────────────────────────────────────────────────────
    def _build_logo(self):
        """Top logo area. Change the icon character or title/subtitle text here."""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(20, 24))

        # Icon square — change the Unicode character or background color here
        icon_box = ctk.CTkFrame(
            logo_frame,
            width=40, height=40,
            fg_color=COLORS["primary"],          # [CHANGE] Icon box background
            corner_radius=10,
        )
        icon_box.pack_propagate(False)
        icon_box.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            icon_box,
            text="⚙",                            # [CHANGE] Logo icon character
            font=("Inter", 18, "bold"),
            text_color="#ffffff",
        ).place(relx=0.5, rely=0.5, anchor="center")

        # App title and subtitle
        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.pack(side="left")

        ctk.CTkLabel(
            text_frame,
            text="OS Simulator",                 # [CHANGE] App name
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Management Console",           # [CHANGE] App subtitle
            font=FONTS["body_sm"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w")

    # ─── Navigation Items ────────────────────────────────────────────────────
    def _build_nav(self):
        """
        Builds the navigation button list.
        Each tuple is: (display_label, page_key, icon_character)
        To add/remove pages, edit the self.nav_items list below.
        """
        nav_container = ctk.CTkFrame(self, fg_color="transparent")
        nav_container.pack(fill="x", pady=(0, 8))

        # [CHANGE] Navigation items: (Label, Page Key, Icon)
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
        """Creates a single nav button with active-state styling."""
        btn = ctk.CTkButton(
            parent,
            text=f"  {icon}  {label}",
            font=FONTS["nav"],
            anchor="w",
            height=42,                           # [CHANGE] Nav button height
            corner_radius=8,
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["bg_elevated"],
            command=lambda pk=page_key: self.navigate_callback(pk),
        )
        btn.pack(fill="x", padx=12, pady=2)
        return btn

    def set_active(self, page_key):
        """Highlights the active nav item with a blue accent border effect."""
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

    # ─── About Us Card ───────────────────────────────────────────────────────
    def _build_about_us(self):
        """
        About Us panel pinned to the bottom of the sidebar.
        Change ABOUT_US_TEXT at the top of the file to update the content.
        """
        # Push the card to the bottom
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_elevated"],
            corner_radius=12,                    # [CHANGE] Card corner radius
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
            wraplength=190,                      # [CHANGE] Adjust if sidebar width changes
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 14))


# =============================================================================
# [HOME PAGE] - Dashboard / Landing Screen
# Shows module cards that let the user navigate to each simulator.
# =============================================================================
class HomePage(ctk.CTkFrame):
    """
    Home page layout with greeting header and module selection cards.

    To add/remove module cards, edit the self.modules list in _build_cards().
    """

    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)
        self.navigate_callback = navigate_callback
        self._build_header()
        self._build_cards()

    # ─── Header ─────────────────────────────────────────────────────────────
    def _build_header(self):
        """Page title and subtitle. Change text here."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(32, 24))   # [CHANGE] Top padding

        ctk.CTkLabel(
            header,
            text="Hi, what do you want to do?",          # [CHANGE] Page title
            font=FONTS["headline_lg"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Select a module to start the simulation and observe real-time algorithmic execution.",
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(4, 0))

    # ─── Module Cards ────────────────────────────────────────────────────────
    def _build_cards(self):
        """
        Grid of module cards. Each card has an icon, title, description, and link.
        
        Module data format: (title, description, icon_char, icon_bg_color, page_key, badge_text or None)
        - badge_text: Optional badge shown in top-right of card (e.g. "SYSTEM_CORE_V1")
        - page_key: Must match a key in the app's page registry
        """
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # [CHANGE] Module definitions — edit here to update cards
        self.modules = [
            (
                "CPU Scheduling",
                "Dive deep into the heart of the operating system. Simulate First-Come-First-Served, "
                "Round Robin, and Shortest Job First algorithms. Visualize process states, burst times, "
                "and monitor context switching overhead in real-time.",
                "🖥",
                COLORS["icon_cpu"],
                "CPU Scheduling",
                "SYSTEM_CORE_V1",       # Badge text (None = no badge)
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

        # Row 0: large featured card + memory card (side by side)
        row0 = ctk.CTkFrame(scroll, fg_color="transparent")
        row0.pack(fill="x", pady=(0, 16))
        row0.columnconfigure(0, weight=3)    # [CHANGE] Featured card weight
        row0.columnconfigure(1, weight=2)    # [CHANGE] Side card weight

        self._make_card(row0, self.modules[0], large=True).grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self._make_card(row0, self.modules[1], large=True).grid(row=0, column=1, sticky="nsew")

        # Row 1: three equal cards
        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 16))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)
        row1.columnconfigure(2, weight=1)

        for i, module in enumerate(self.modules[2:]):
            self._make_card(row1, module).grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 12, 0))

    def _make_card(self, parent, module_data, large=False):
        """
        Builds a single module card.
        large=True makes it taller with more padding (used for top row).
        """
        title, desc, icon, icon_bg, page_key, badge = module_data

        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,                    # [CHANGE] Card corner radius
            border_width=1,
            border_color=COLORS["border"],
        )

        inner_pad = 20 if large else 16          # [CHANGE] Inner card padding

        # Badge (optional top-right label, e.g. "SYSTEM_CORE_V1")
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
                text=badge,                      # [CHANGE] Badge text
                font=FONTS["body_sm"],
                text_color=COLORS["text_muted"],
            ).pack(padx=10, pady=4)

        # Card title
        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=inner_pad, pady=(16, 0))

        # Card description
        ctk.CTkLabel(
            card,
            text=desc,
            font=FONTS["body_md"],
            text_color=COLORS["text_secondary"],
            wraplength=320 if large else 240,    # [CHANGE] Adjust to prevent overflow
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=inner_pad, pady=(6, 0))

        # "Start Simulation →" link button
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


# =============================================================================
# [CPU PAGE] - CPU Scheduling Simulator
# Left/center area is the process queue table; right panel has controls.
# =============================================================================
class CPUSchedulingPage(ctk.CTkFrame):
    """
    CPU Scheduling page with:
      - Progress bar at the top (simulation progress)
      - [PROCESS TABLE] scrollable table
      - [CONTROLS] right-side panel with algorithm selector, sliders, inputs
      - [METRICS] bottom metrics strip
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        # Track process list: list of dicts with keys: pid, arrival, burst, priority, status
        self.processes = [
            {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2, "status": "Waiting"},
            {"pid": "P2", "arrival": 1, "burst": 5, "priority": 1, "status": "Terminated"},
            {"pid": "P3", "arrival": 2, "burst": 4, "priority": 3, "status": "Running"},
            {"pid": "P4", "arrival": 6, "burst": 2, "priority": 4, "status": "Ready"},
        ]

        # Main 2-column layout: content area + controls panel
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)   # Controls panel has fixed width
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_controls_panel()

    # ─── Left/Center Content Area ────────────────────────────────────────────
    def _build_main_area(self):
        """Builds the main content column: header, progress bar, and process table."""
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.rowconfigure(2, weight=1)
        main.columnconfigure(0, weight=1)

        # ── Page Title ──────────────────────────────────────────────────────
        ctk.CTkLabel(
            main,
            text="CPU Scheduling Module",         # [CHANGE] Module title
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

        # ── Simulation Progress Bar ─────────────────────────────────────────
        # [CHANGE] Update self.progress_var.set(value) to animate this bar
        self.progress_var = ctk.DoubleVar(value=0.0)
        progress_bar = ctk.CTkProgressBar(
            main,
            variable=self.progress_var,
            height=8,                            # [CHANGE] Bar thickness
            corner_radius=4,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["primary"],
        )
        progress_bar.grid(row=2, column=0, sticky="ew", pady=(0, 16))

        # ── Process Queue Table ─────────────────────────────────────────────
        self._build_process_table(main, row=3)

    # ─── [PROCESS TABLE] ─────────────────────────────────────────────────────
    def _build_process_table(self, parent, row):
        """
        Scrollable process queue table.
        Headers: PID, Arrival Time, Burst Time, Priority, Status, Remove
        To add a column, add to COLUMNS and extend _add_process_row().
        """
        table_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        table_frame.grid(row=row, column=0, sticky="nsew")
        parent.rowconfigure(row, weight=1)

        # ── Table header row ────────────────────────────────────────────────
        header_bar = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_bar.pack(fill="x", padx=20, pady=(16, 0))

        ctk.CTkLabel(
            header_bar,
            text="Process Queue",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # "+ Add Process" button in the table header
        add_btn = ctk.CTkButton(
            header_bar,
            text="⊕  Add Process",              # [CHANGE] Button text
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

        # ── Column headers ──────────────────────────────────────────────────
        # [CHANGE] COLUMNS: list of (label, weight) — weight controls column width
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
                font=FONTS["body_sm"],           # [CHANGE] Header font
                text_color=COLORS["text_muted"],
                anchor="w" if i == 0 else "center",
            ).grid(row=0, column=i, sticky="ew")

        # Divider line
        divider = ctk.CTkFrame(table_frame, fg_color=COLORS["border"], height=1)
        divider.pack(fill="x", padx=20, pady=(0, 4))

        # ── Scrollable rows container ───────────────────────────────────────
        self.table_scroll = ctk.CTkScrollableFrame(
            table_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        self.table_scroll.pack(fill="both", expand=True, padx=4, pady=(0, 12))
        self.table_scroll.columnconfigure(list(range(len(COLUMNS))), weight=1)

        # Store column count for row builder
        self._col_count = len(COLUMNS)
        self._col_weights = [w for _, w in COLUMNS]

        # Populate initial rows from self.processes
        self._refresh_table()

    def _refresh_table(self):
        """Clears and redraws all process rows. Call this after adding/removing a process."""
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        for i, proc in enumerate(self.processes):
            self._add_process_row(i, proc)

    def _add_process_row(self, row_index, proc):
        """
        Renders a single process row.
        proc keys: pid, arrival, burst, priority, status
        Status colors are controlled by COLORS["status_*"] at the top.
        """
        # Alternating row background colors for readability
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

        # Column 0: PID (electric-blue, monospace)
        ctk.CTkLabel(
            row_frame,
            text=proc["pid"],
            font=FONTS["data_md"],
            text_color=COLORS["primary_light"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(12, 0))

        # Columns 1–3: Arrival, Burst, Priority (monospace data)
        for col_idx, key in enumerate(["arrival", "burst", "priority"], start=1):
            ctk.CTkLabel(
                row_frame,
                text=str(proc[key]),
                font=FONTS["data_md"],
                text_color=COLORS["text_primary"],
                anchor="center",
            ).grid(row=0, column=col_idx, sticky="ew")

        # Column 4: Status chip (pill badge)
        status = proc["status"]
        # [CHANGE] Status chip colors — map status string to color pair
        chip_colors = {
            "Running":    (COLORS["status_running_bg"],    COLORS["status_running_fg"]),
            "Waiting":    (COLORS["status_waiting_bg"],    COLORS["status_waiting_fg"]),
            "Terminated": (COLORS["status_terminated_bg"], COLORS["status_terminated_fg"]),
            "Ready":      (COLORS["status_ready_bg"],      COLORS["status_ready_fg"]),
        }
        chip_bg, chip_fg = chip_colors.get(status, (COLORS["bg_elevated"], COLORS["text_primary"]))

        # Running badge gets a green dot prefix
        status_text = f"● {status}" if status == "Running" else status

        chip_wrapper = ctk.CTkFrame(row_frame, fg_color="transparent")
        chip_wrapper.grid(row=0, column=4, sticky="ew")

        chip = ctk.CTkFrame(
            chip_wrapper,
            fg_color=chip_bg,
            corner_radius=99,                    # [CHANGE] Pill radius (99 = fully rounded)
        )
        chip.pack(anchor="center")
        ctk.CTkLabel(
            chip,
            text=status_text,
            font=FONTS["body_sm"],
            text_color=chip_fg,
        ).pack(padx=10, pady=3)

        # Column 5: Remove (trash icon) button
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
        """Removes a process from self.processes by PID and refreshes the table."""
        self.processes = [p for p in self.processes if p["pid"] != pid]
        self._refresh_table()

    def _on_add_process(self):
        """
        Called when '+ Add Process' is clicked.
        Reads values from the right-panel inputs and adds a new process.
        """
        name = self.proc_name_entry.get().strip()
        burst = self.burst_entry.get().strip()
        arrival = self.arrival_entry.get().strip()

        # Basic validation — customize error handling here
        if not name or not burst.isdigit() or not arrival.isdigit():
            return  # [CHANGE] Add error feedback (e.g., shake animation or label)

        new_proc = {
            "pid":      name,
            "arrival":  int(arrival),
            "burst":    int(burst),
            "priority": 1,                       # [CHANGE] Default priority for new processes
            "status":   "Ready",
        }
        self.processes.append(new_proc)
        self._refresh_table()

        # Clear inputs after adding
        self.proc_name_entry.delete(0, "end")
        self.burst_entry.delete(0, "end")
        self.arrival_entry.delete(0, "end")

    # ─── [CONTROLS] Right Panel ───────────────────────────────────────────────
    def _build_controls_panel(self):
        """
        Right-side controls panel containing:
          - Algorithm dropdown
          - Time Quantum slider
          - Process Configuration form (name, burst, arrival, add button)
          - Run Simulation button
          - [METRICS] section
        """
        panel = ctk.CTkFrame(
            self,
            width=290,                           # [CHANGE] Controls panel width
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

        # ── Panel Header ────────────────────────────────────────────────────
        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(20, 16))

        ctk.CTkLabel(
            header_row,
            text="≡  Controls",                 # [CHANGE] Panel title
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._divider(scroll)

        # ── Algorithm Selector ──────────────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="ALGORITHM",                   # [CHANGE] Section label
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        # [CHANGE] Algorithm options list
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

        # ── Time Quantum Slider ─────────────────────────────────────────────
        tq_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tq_row.pack(fill="x", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            tq_row,
            text="TIME QUANTUM (MS)",           # [CHANGE] Slider label
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
            from_=1, to=10,                     # [CHANGE] Slider min/max
            number_of_steps=9,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["primary"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_light"],
            command=self._on_tq_change,
        )
        self.tq_slider.set(2)                   # [CHANGE] Default time quantum
        self.tq_slider.pack(fill="x", padx=16, pady=(6, 0))

        # Slider tick labels (min / mid / max)
        tick_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tick_row.pack(fill="x", padx=16)
        ctk.CTkLabel(tick_row, text="1", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkLabel(tick_row, text="5", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left", expand=True)
        ctk.CTkLabel(tick_row, text="10", font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="right")

        self._divider(scroll)

        # ── Process Configuration Form ──────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="PROCESS CONFIGURATION",       # [CHANGE] Section label
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 8))

        # Process Name input
        ctk.CTkLabel(scroll, text="Process Name", font=FONTS["body_sm"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=16)
        self.proc_name_entry = ctk.CTkEntry(
            scroll,
            placeholder_text="e.g. P5",        # [CHANGE] Placeholder text
            font=FONTS["data_md"],
            fg_color=COLORS["bg_elevated"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_primary"],
        )
        self.proc_name_entry.pack(fill="x", padx=16, pady=(4, 10))

        # Burst Time + Arrival Time (side by side)
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

        # Add to Queue button (teal)
        ctk.CTkButton(
            scroll,
            text="＋  Add to Queue",            # [CHANGE] Button text
            font=FONTS["button"],
            height=44,
            corner_radius=8,
            fg_color=COLORS["secondary"],        # [CHANGE] Button color
            text_color="#003827",
            hover_color=COLORS["secondary_dark"],
            command=self._on_add_process,
        ).pack(fill="x", padx=16, pady=(0, 16))

        self._divider(scroll)

        # ── Run Simulation Button ───────────────────────────────────────────
        ctk.CTkButton(
            scroll,
            text="▶  Run Simulation",           # [CHANGE] Button text
            font=FONTS["button"],
            height=52,
            corner_radius=10,
            fg_color=COLORS["primary"],          # [CHANGE] Button color
            hover_color=COLORS["primary_light"],
            text_color="#ffffff",
            command=self._on_run_simulation,
        ).pack(fill="x", padx=16, pady=16)

        self._divider(scroll)

        # ── [METRICS] Section ───────────────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="METRICS",                     # [CHANGE] Section label
            font=FONTS["label_caps"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=16, pady=(12, 8))

        # [CHANGE] Metrics data: (label, value, color)
        self.metrics_data = {
            "avg_wait":    ("Avg Waiting Time",  "4.2 ms",  COLORS["text_primary"]),
            "avg_turn":    ("Avg Turnaround",    "8.5 ms",  COLORS["text_primary"]),
            "cpu_util":    ("CPU Utilization",   "92%",     COLORS["secondary"]),
        }

        self.metric_labels = {}
        for key, (label, value, color) in self.metrics_data.items():
            self._make_metric_row(scroll, key, label, value, color)

        # Bottom padding
        ctk.CTkFrame(scroll, fg_color="transparent", height=20).pack()

    def _make_metric_row(self, parent, key, label, value, color):
        """
        Creates a single metric display row.
        Call self.update_metric(key, new_value) to update it dynamically.
        """
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
        """
        Call this to update a metric value dynamically after simulation runs.
        Example: self.update_metric("cpu_util", "87%")
        """
        if key in self.metric_labels:
            self.metric_labels[key].configure(text=new_value)

    # ─── Helpers ─────────────────────────────────────────────────────────────
    def _divider(self, parent):
        """Thin horizontal divider line."""
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=0, pady=4)

    def _on_tq_change(self, value):
        """Called when the Time Quantum slider moves. Updates the value label."""
        self.tq_value_label.configure(text=str(int(value)))

    def _on_run_simulation(self):
        """
        Called when 'Run Simulation' is clicked.
        [CHANGE] Add your scheduling algorithm logic here.
        After computation, call self.update_metric(key, value) for each metric.
        Also update self.progress_var.set(0.0 to 1.0) to animate the progress bar.
        """
        algo = self.algo_var.get()
        tq = int(self.tq_slider.get())
        print(f"[Simulation] Algorithm: {algo}, Time Quantum: {tq}ms")
        print(f"[Simulation] Processes: {self.processes}")

        # Placeholder: set progress bar to 100% on run
        self.progress_var.set(1.0)

        # Placeholder: update metrics (replace with real calculations)
        self.update_metric("avg_wait", "4.2 ms")
        self.update_metric("avg_turn", "8.5 ms")
        self.update_metric("cpu_util", "92%")


# =============================================================================
# [PLACEHOLDER PAGES] - Stub pages for modules not yet implemented
# Replace each PlaceholderPage with a real module class when ready.
# =============================================================================
class PlaceholderPage(ctk.CTkFrame):
    """
    Generic placeholder page for unimplemented modules.
    Replace this with a real page class (like CPUSchedulingPage) when ready.
    """

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


# =============================================================================
# [VIRTUAL MEMORY PAGE] - Virtual Memory / Page Replacement Simulator
#
# Layout mirrors the inspo design:
#   • Center: page title/subtitle, Reference String Queue panel, memory frames
#   • Right:  Parameters panel (algorithm, frames slider, add page, page faults,
#             run button)
#
# Algorithm logic lives in algorithms/<name>.py  (one module per algorithm).
# To add a new algorithm: create the module and register it in algorithms/__init__.py.
# The dropdown is auto-populated from the registry keys.
# =============================================================================

# Build the ordered algorithm list from the registry (preserves insertion order)
VM_ALGORITHMS = list(algorithms.REGISTRY.keys())


class VirtualMemoryPage(ctk.CTkFrame):
    """
    Virtual Memory module page.

    Key state:
      self.ref_string  – list[int] of page numbers in the reference queue
      self.frame_count – number of physical memory frames (from slider)
      self.page_faults – int count of faults after last simulation run
      self.sim_steps   – list[list[int|None]] of frame snapshots per step
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], corner_radius=0, **kwargs)

        # Starting reference string (matches inspo screenshot)
        self.ref_string = [7, 0, 1, 2, 0, 3]
        self.frame_count = 3
        self.page_faults = 0
        self.sim_steps = []   # list of step dicts from algorithm modules

        # Selection state for queue tiles
        self._selected_tile_idx: int | None = None

        # LFU / MFU mode for Counting-Based algorithm (default: LFU)
        self._counting_mode = "LFU"

        # 2-column layout: main content + right parameters panel
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)  # fixed-width right panel
        self.rowconfigure(0, weight=1)

        self._build_main_area()
        self._build_parameters_panel()

    # =========================================================================
    # CENTER CONTENT AREA
    # =========================================================================
    def _build_main_area(self):
        """Builds the scrollable center column with title, queue, and frames."""
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary"],
        )
        main.grid(row=0, column=0, sticky="nsew", padx=(32, 16), pady=24)
        main.columnconfigure(0, weight=1)
        self._main_scroll = main

        # ── Page Title ───────────────────────────────────────────────────────
        ctk.CTkLabel(
            main,
            text="Virtual Memory Module",            # [CHANGE] Page title
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

        # ── Reference String Queue Panel ─────────────────────────────────────
        self._build_ref_queue_panel(main)

        # Thin divider between queue and frames area
        ctk.CTkFrame(main, fg_color=COLORS["border"], height=1).pack(fill="x", pady=(16, 0))

        # ── Memory Frames Visualization Area ─────────────────────────────────
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
        """
        The [·] Reference String Queue card.
        Click any tile to select it (green border). Click the Remove button
        to delete the selected tile from the queue.
        """
        panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_panel"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        panel.pack(fill="x")

        # ── Panel header ─────────────────────────────────────────────────────
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 10))

        ctk.CTkLabel(
            header,
            text="[·]  Reference String Queue",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # Remove Selected button — stays disabled until a tile is selected
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

        # ── Scrollable tile row ───────────────────────────────────────────────
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
        """Redraws all page-number tiles. Selected tile shows a green border."""
        for w in self._queue_tiles_frame.winfo_children():
            w.destroy()

        for idx, page_num in enumerate(self.ref_string):
            is_selected = (idx == self._selected_tile_idx)

            # Selected tile: green border + tinted bg; normal tile: default border
            tile_bg     = COLORS["status_running_bg"] if is_selected else COLORS["bg_elevated"]
            tile_border = COLORS["secondary"]          if is_selected else COLORS["border"]
            text_color  = COLORS["secondary"]          if is_selected else COLORS["text_primary"]
            border_w    = 2                             if is_selected else 1

            # Outer wrapper gives us the green left-side accent when selected
            tile_outer = ctk.CTkFrame(
                self._queue_tiles_frame,
                width=54, height=54,
                fg_color="transparent",
                corner_radius=11,
            )
            tile_outer.pack_propagate(False)
            tile_outer.pack(side="left", padx=(3, 3), pady=4)

            # Green left stripe for the selected tile
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

            # Bind click to select/deselect this tile
            for widget in (tile_outer, tile):
                widget.bind("<Button-1>", lambda e, i=idx: self._select_tile(i))
            for child in tile.winfo_children():
                child.bind("<Button-1>", lambda e, i=idx: self._select_tile(i))

    def _select_tile(self, idx: int):
        """Selects a tile (or deselects if the same tile is clicked again)."""
        if self._selected_tile_idx == idx:
            self._selected_tile_idx = None           # toggle off
        else:
            self._selected_tile_idx = idx
        self._refresh_queue_tiles()
        # Enable/disable the Remove button
        state = "normal" if self._selected_tile_idx is not None else "disabled"
        self._remove_tile_btn.configure(state=state)

    def _remove_selected_tile(self):
        """Removes the currently selected tile from the reference string."""
        idx = self._selected_tile_idx
        if idx is not None and 0 <= idx < len(self.ref_string):
            self.ref_string.pop(idx)
            self._selected_tile_idx = None
            self._remove_tile_btn.configure(state="disabled")
            self._refresh_queue_tiles()

    def _draw_frames_empty_state(self):
        """Shows the 'no simulation yet' empty state inside the frames area."""
        for w in self._frames_container.winfo_children():
            w.destroy()

        placeholder = ctk.CTkFrame(self._frames_container, fg_color="transparent")
        placeholder.pack(expand=True, fill="both", pady=40)

        ctk.CTkLabel(
            placeholder,
            text="▦",                             # grid-like icon
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
        """
        Renders simulation results as a ttk.Treeview.

        Orientation: ROWS = steps (one per page reference),
                     COLUMNS = fixed: Page | Frame0 | Frame1 | … | Evicted | Status

        This allows natural per-row coloring:
          • FAULT rows  — electric-blue accent (primary_light)
          • HIT   rows  — green accent (secondary)
        """
        for w in self._frames_container.winfo_children():
            w.destroy()

        if not self.sim_steps:
            self._draw_frames_empty_state()
            return

        # ── Section title ────────────────────────────────────────────────────────
        title_bar = ctk.CTkFrame(self._frames_container, fg_color="transparent")
        title_bar.pack(fill="x", padx=20, pady=(14, 8))
        ctk.CTkLabel(
            title_bar,
            text="Memory Frames — Step-by-Step",
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # Legend
        legend_frame = ctk.CTkFrame(title_bar, fg_color="transparent")
        legend_frame.pack(side="right")
        for dot, label in ((COLORS["primary_light"], "FAULT"), (COLORS["secondary"], "HIT")):
            ctk.CTkLabel(legend_frame, text="●", font=("Inter", 10), text_color=dot).pack(side="left", padx=(6, 1))
            ctk.CTkLabel(legend_frame, text=label, font=FONTS["body_sm"], text_color=COLORS["text_muted"]).pack(side="left")

        # ── ttk style ─────────────────────────────────────────────────────────────
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

        # ── Build column definitions ───────────────────────────────────────────────────
        # Columns: Page | Frame0 … FrameN | Evicted | Status
        frame_col_ids = [f"f{i}" for i in range(self.frame_count)]
        col_ids = ["page"] + frame_col_ids + ["evicted", "status"]

        # ── Wrapper + Treeview + scrollbars ─────────────────────────────────────────
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
        self._tree = tree  # keep ref to prevent GC

        # ── Column headings ────────────────────────────────────────────────────────────
        tree.heading("page",    text="Page Ref",  anchor="center")
        tree.column( "page",    width=70, minwidth=60, stretch=False, anchor="center")
        for i in range(self.frame_count):
            tree.heading(f"f{i}",  text=f"Frame {i}", anchor="center")
            tree.column( f"f{i}",  width=66, minwidth=54, stretch=False, anchor="center")
        tree.heading("evicted", text="Evicted",    anchor="center")
        tree.column( "evicted", width=70, minwidth=60, stretch=False, anchor="center")
        tree.heading("status",  text="Status",     anchor="center")
        tree.column( "status",  width=70, minwidth=60, stretch=True,  anchor="center")

        # ── Row tags ──────────────────────────────────────────────────────────────────
        tree.tag_configure("fault_step",
                           background=COLORS["icon_cpu"],
                           foreground=COLORS["primary_light"])
        tree.tag_configure("hit_step",
                           background=COLORS["status_running_bg"],
                           foreground=COLORS["secondary"])

        # ── Populate rows (one per reference step) ───────────────────────────────────
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

    # =========================================================================
    # RIGHT PARAMETERS PANEL
    # =========================================================================
    def _build_parameters_panel(self):
        """
        Right-side Parameters panel matching the inspo:
          ≡ Parameters
          ─────────────
          Algorithm (dropdown)
          Frames in Memory (slider + number box)
          Add to Reference String (entry + + button)
          PAGE FAULTS counter
          ▶ Run Simulation
        """
        panel = ctk.CTkFrame(
            self,
            width=300,                           # [CHANGE] Right panel width
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

        # ── Panel Header ─────────────────────────────────────────────────────
        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(20, 16))

        ctk.CTkLabel(
            header_row,
            text="≡  Parameters",                # matches inspo icon + label
            font=FONTS["headline_sm"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self._divider(scroll)

        # ── Algorithm Dropdown ───────────────────────────────────────────────
        ctk.CTkLabel(
            scroll,
            text="Algorithm",
            font=FONTS["body_sm"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.vm_algo_var = ctk.StringVar(value=VM_ALGORITHMS[0])  # default: FIFO
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

        # ── LFU / MFU Toggle (only shown for Counting-Based) ────────────────────
        self._lfu_mfu_frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg_elevated"], corner_radius=10)
        # Packed/un-packed dynamically by _on_algo_change; hidden by default

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
            text="",                            # no text; labels are manual
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

        # ── Frames in Memory Slider + Input ──────────────────────────────────
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

        # Numeric display box (like inspo, shows current frame count)
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

        # ── Add to Reference String ──────────────────────────────────────────
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

        # ── Page Faults Counter Box ───────────────────────────────────────────
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

        # ── Run Simulation Button ─────────────────────────────────────────────
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

        # Bottom padding
        ctk.CTkFrame(scroll, fg_color="transparent", height=20).pack()

    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    def _on_frames_change(self, value):
        """Updates frame_count and the numeric display box when slider moves."""
        self.frame_count = int(value)
        self.frames_val_label.configure(text=str(self.frame_count))

    def _on_add_page(self):
        """Adds a page number to the reference string from the entry widget."""
        raw = self.page_entry.get().strip()
        if raw.isdigit():
            self.ref_string.append(int(raw))
            self._refresh_queue_tiles()
            self.page_entry.delete(0, "end")

    def _on_algo_change(self, algo: str):
        """
        Called when the algorithm dropdown changes.
        Shows the LFU/MFU toggle only for Counting-Based.
        """
        if "Counting" in algo:
            self._lfu_mfu_frame.pack(fill="x", padx=16, pady=(4, 8))
        else:
            self._lfu_mfu_frame.pack_forget()

    def _on_lfu_mfu_toggle(self):
        """Reads the switch value (LFU / MFU) into self._counting_mode."""
        self._counting_mode = self._lfu_mfu_switch.get()

    def _on_run_simulation(self):
        """
        Dispatches to the selected algorithm module via the registry, then
        re-renders the Treeview visualization.
        For Counting-Based, passes the current LFU/MFU mode.
        """
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

    # =========================================================================
    # HELPERS
    # =========================================================================
    def _divider(self, parent):
        """Thin horizontal divider line."""
        ctk.CTkFrame(parent, fg_color=COLORS["border"], height=1).pack(fill="x", padx=0, pady=4)


# =============================================================================
# [MAIN APP] - Application Window & Page Router
# Controls window setup, page registry, and navigation.
# =============================================================================
class OSSimulatorApp(ctk.CTk):
    """
    Root application window.
    
    HOW NAVIGATION WORKS:
      - self.pages is a dict mapping page_key → frame widget
      - navigate(page_key) hides all frames and shows the requested one
      - The sidebar calls navigate() when a nav button is clicked
      - Home page cards also call navigate() via the navigate_callback

    To add a new page:
      1. Create a new class (like CPUSchedulingPage)
      2. Instantiate it in _build_pages() and add to self.pages dict
      3. Add a nav item in Sidebar._build_nav()
    """

    def __init__(self):
        super().__init__()

        # ── Window settings ─────────────────────────────────────────────────
        self.title("OS Algorithm Simulator")    # [CHANGE] Window title bar text
        self.geometry("1280x820")               # [CHANGE] Default window size
        self.minsize(900, 600)                  # [CHANGE] Minimum window size
        ctk.set_appearance_mode("dark")         # "dark" or "light"
        ctk.set_default_color_theme("blue")     # CustomTkinter base theme

        # Background color
        self.configure(fg_color=COLORS["bg"])

        # ── Layout: sidebar (left) + content area (right) ───────────────────
        self.grid_columnconfigure(0, weight=0)  # Sidebar: fixed
        self.grid_columnconfigure(1, weight=1)  # Content: expands
        self.grid_rowconfigure(0, weight=1)

        # ── Build sidebar ────────────────────────────────────────────────────
        self.sidebar = Sidebar(self, navigate_callback=self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # ── Build content area ───────────────────────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # ── Register all pages ───────────────────────────────────────────────
        self._build_pages()

        # ── Start on Home page ───────────────────────────────────────────────
        self.navigate("Home")

    def _build_pages(self):
        """
        Instantiates all page frames and stores them in self.pages.
        All pages share the same grid cell (row=0, col=0) and are
        shown/hidden via tkraise().
        """
        self.pages = {}

        # Home page
        home = HomePage(self.content, navigate_callback=self.navigate)
        home.grid(row=0, column=0, sticky="nsew")
        self.pages["Home"] = home

        # CPU Scheduling page
        cpu = CPUSchedulingPage(self.content)
        cpu.grid(row=0, column=0, sticky="nsew")
        self.pages["CPU Scheduling"] = cpu

        # Virtual Memory page — full implementation
        vm = VirtualMemoryPage(self.content)
        vm.grid(row=0, column=0, sticky="nsew")
        self.pages["Virtual Memory"] = vm

        # [CHANGE] Add real page classes below when modules are implemented.
        # For now they show a placeholder screen.
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
        """
        Switches the visible page.
        Also updates the sidebar active state.
        """
        if page_key in self.pages:
            self.pages[page_key].tkraise()
            self.sidebar.set_active(page_key)


# =============================================================================
#  Entry Point
# =============================================================================
if __name__ == "__main__":
    app = OSSimulatorApp()
    app.mainloop()
