import tkinter as tk
from tkinter import ttk, messagebox
from src.models.nav_graph import NavGraph
from src.controllers.fleet_manager import FleetManager

class FleetGUI:
    def __init__(self, master, nav_graph: NavGraph, fleet_manager: FleetManager):
        self.master = master
        self.nav_graph = nav_graph
        self.fleet_manager = fleet_manager
        self.selected_robot = None
        self.scale = 1
        self.offset = 50
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Fleet Management System")
        self.master.geometry("1200x800")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)

        # Canvas
        self.canvas = tk.Canvas(self.master, bg='white')
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Control Panel
        control_panel = tk.Frame(self.master, width=300)
        control_panel.grid(row=0, column=1, sticky="nsew")

        # Robot List
        self.robot_tree = ttk.Treeview(control_panel, columns=('status', 'location'), height=10)
        self.robot_tree.heading('#0', text='Robot ID')
        self.robot_tree.heading('status', text='Status')
        self.robot_tree.heading('location', text='Location')
        self.robot_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Log Display
        self.log_text = tk.Text(control_panel, height=10, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.robot_tree.bind("<<TreeviewSelect>>", self.on_robot_select)

        self.update_gui()
        self.master.after(50, self.update)

    def draw_environment(self):
        self.canvas.delete("all")
        # Auto-scale
        positions = [self.nav_graph.get_vertex_position(v) for v in self.nav_graph.get_all_vertices()]
        min_x, max_x = min(p[0] for p in positions), max(p[0] for p in positions)
        min_y, max_y = min(p[1] for p in positions), max(p[1] for p in positions)
        self.scale = min((800 - 100) / (max_x - min_x), (600 - 100) / (max_y - min_y)) if max_x > min_x else 50

        # Draw lanes
        for u, v in self.nav_graph.edges:
            x1, y1 = self.scale_position(self.nav_graph.get_vertex_position(u))
            x2, y2 = self.scale_position(self.nav_graph.get_vertex_position(v))
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        # Draw vertices
        for v in self.nav_graph.nodes:
            x, y = self.scale_position(self.nav_graph.get_vertex_position(v))
            fill = "orange" if self.nav_graph.get_vertex_attributes(v).get('is_charger', False) else "lightblue"
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=fill, tags=f"vertex_{v}")
            name = self.nav_graph.get_vertex_attributes(v).get('name', str(v))
            self.canvas.create_text(x, y+20, text=name)

        # Draw robots
        positions = self.fleet_manager.get_robot_positions()
        statuses = self.fleet_manager.get_robot_statuses()
        colors = self.fleet_manager.get_robot_colors()
        for robot_id, (x, y) in positions.items():
            x, y = self.scale_position((x, y))
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill=colors[robot_id], tags=f"robot_{robot_id}")
            self.canvas.create_text(x, y-20, text=f"R{robot_id} ({statuses[robot_id]})")

    def scale_position(self, pos):
        return pos[0] * self.scale + self.offset, pos[1] * self.scale + self.offset

    def update_gui(self):
        self.draw_environment()
        self.robot_tree.delete(*self.robot_tree.get_children())
        for robot_id, status in self.fleet_manager.get_robot_statuses().items():
            location = self.nav_graph.get_vertex_attributes(self.fleet_manager.robots[robot_id].current_vertex).get('name', str(robot_id))
            self.robot_tree.insert('', 'end', text=f"R{robot_id}", values=(status, location))
        try:
            with open('logs/fleet_logs.txt', 'r') as f:
                self.log_text.config(state='normal')
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, ''.join(f.readlines()[-20:]))
                self.log_text.config(state='disabled')
        except FileNotFoundError:
            pass

    def on_canvas_click(self, event):
        clicked_vertex = None
        for v in self.nav_graph.nodes:
            x, y = self.scale_position(self.nav_graph.get_vertex_position(v))
            if ((event.x - x)**2 + (event.y - y)**2)**0.5 < 10:
                clicked_vertex = v
                break
        if clicked_vertex is not None:
            if self.selected_robot is None:
                try:
                    self.fleet_manager.spawn_robot(clicked_vertex)
                except RuntimeError as e:
                    messagebox.showerror("Error", str(e))
            else:
                if not self.fleet_manager.assign_task(self.selected_robot, clicked_vertex):
                    messagebox.showerror("Error", "No path to destination")
                self.selected_robot = None
            self.update_gui()

        for robot_id, (x, y) in self.fleet_manager.get_robot_positions().items():
            x, y = self.scale_position((x, y))
            if ((event.x - x)**2 + (event.y - y)**2)**0.5 < 10:
                self.selected_robot = robot_id
                break

    def on_robot_select(self, event):
        selected = self.robot_tree.selection()
        if selected:
            self.selected_robot = int(self.robot_tree.item(selected[0], 'text')[1:])
            self.update_gui()

    def update(self):
        self.fleet_manager.update()
        self.update_gui()
        self.master.after(50, self.update)