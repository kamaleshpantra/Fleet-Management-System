import tkinter as tk
from tkinter import messagebox
import logging

class FleetGUI:
    def __init__(self, fleet_manager, traffic_manager, nav_graph):
        self.fleet_manager = fleet_manager
        self.traffic_manager = traffic_manager
        self.nav_graph = nav_graph
        self.window = tk.Tk()
        self.window.title("Fleet Management System")  # Set window title
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.robot_circles = {}  # Store GUI representations of robots
        self.selected_robot = None
        self.logger = logging.getLogger(__name__)

        self.draw_environment()
        self.setup_event_handlers()
        self.update_robots()  # Start updating robot positions

    def draw_environment(self):
        """
        Draws the vertices and lanes on the canvas.
        """
        self.canvas.delete("all")  # Clear the canvas
        for vertex_id, vertex in self.nav_graph.vertices.items():
            x, y = vertex["coordinates"]
            self.draw_vertex(x, y, vertex_id, vertex.get("attributes", {}).get("name"))

        for lane in self.nav_graph.lanes:
            start_vertex = self.nav_graph.vertices[lane[0]]
            end_vertex = self.nav_graph.vertices[lane[1]]
            start_x, start_y = start_vertex["coordinates"]
            end_x, end_y = end_vertex["coordinates"]
            self.draw_lane(start_x, start_y, end_x, end_y)

        # Draw robots after drawing the environment
        for robot in self.fleet_manager.get_all_robots():
            self.draw_robot(robot)

    def draw_vertex(self, x, y, vertex_id, name=None):
        """
        Draws a vertex on the canvas.
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", tags=("vertex", f"vertex_{vertex_id}"))
        if name:
            self.canvas.create_text(x, y - 10, text=name, tags=("vertex_label", f"vertex_label_{vertex_id}"))
        else:
            self.canvas.create_text(x, y - 10, text=str(vertex_id), tags=("vertex_label", f"vertex_label_{vertex_id}"))

    def draw_lane(self, start_x, start_y, end_x, end_y):
        """
        Draws a lane on the canvas.
        """
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="black", tags="lane")

    def draw_robot(self, robot):
        """
        Draws a robot on the canvas.
        """
        x, y = self.nav_graph.vertices[robot.current_vertex]["coordinates"]
        color = "red" if robot.status != "complete" else "green"  # Change color based on status
        if robot.robot_id not in self.robot_circles:
            circle = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, tags=("robot", f"robot_{robot.robot_id}"))
            self.robot_circles[robot.robot_id] = circle
            self.canvas.create_text(x, y - 10, text=str(robot.robot_id), tags=("robot_label", f"robot_label_{robot.robot_id}"))
        else:
            self.canvas.coords(self.robot_circles[robot.robot_id], x - 3, y - 3, x + 3, y + 3)
            self.canvas.itemconfig(self.robot_circles[robot.robot_id], fill=color)

    def setup_event_handlers(self):
        """
        Sets up event handlers for mouse clicks.
        """
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        """
        Handles mouse clicks on the canvas.
        """
        x, y = event.x, event.y
        clicked_vertex = self.find_clicked_vertex(x, y)
        if clicked_vertex is not None:
            self.handle_vertex_click(clicked_vertex)
        else:
            clicked_robot = self.find_clicked_robot(x, y)
            if clicked_robot is not None:
                self.handle_robot_click(clicked_robot)

    def find_clicked_vertex(self, x, y):
        """
        Finds the clicked vertex.
        """
        for vertex_id, vertex in self.nav_graph.vertices.items():
            vx, vy = vertex["coordinates"]
            if vx - 5 <= x <= vx + 5 and vy - 5 <= y <= vy + 5:
                return vertex_id
        return None

    def find_clicked_robot(self, x, y):
        """
        Finds the clicked robot.
        """
        for robot in self.fleet_manager.get_all_robots():
            rx, ry = self.nav_graph.vertices[robot.current_vertex]["coordinates"]
            if rx - 3 <= x <= rx + 3 and ry - 3 <= y <= ry + 3:
                return robot
        return None

    def handle_vertex_click(self, vertex_id):
        """
        Handles clicks on vertices.
        """
        if self.selected_robot is None:
            self.spawn_robot(vertex_id)
        else:
            self.assign_task(self.selected_robot, vertex_id)
            self.selected_robot = None  # Deselect the robot after assigning a task

    def handle_robot_click(self, robot):
        """
        Handles clicks on robots.
        """
        self.selected_robot = robot

    def spawn_robot(self, vertex_id):
        """
        Spawns a robot at the given vertex.
        """
        robot = self.fleet_manager.spawn_robot(vertex_id)
        self.draw_robot(robot)
        self.logger.info(f"Robot spawned at vertex {vertex_id}")

    def assign_task(self, robot, destination_vertex):
        """
        Assigns a task to the selected robot.
        """
        if self.fleet_manager.assign_task_to_robot(robot.robot_id, destination_vertex):
            self.logger.info(f"Task assigned to robot {robot.robot_id} to go to {destination_vertex}")
        else:
            messagebox.showerror("Error", "Could not assign task to robot.")

    def update_robots(self):
        """
        Updates the positions of the robots on the canvas.
        """
        self.fleet_manager.update_robot_statuses()
        for robot in self.fleet_manager.get_all_robots():
            self.draw_robot(robot)
        self.window.after(100, self.update_robots)  # Update every 100 milliseconds

    def run(self):
        """
        Runs the GUI main loop.
        """
        self.window.mainloop()