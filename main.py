import os
import tkinter as tk
from src.utils.logger import setup_logger
from src.models.nav_graph import NavGraph
from src.controllers.fleet_manager import FleetManager
from src.gui.fleet_gui import FleetGUI

def main():
    os.makedirs('logs', exist_ok=True)
    setup_logger()
    nav_graph = NavGraph("data/nav_graph_1.json")
    fleet_manager = FleetManager(nav_graph)
    root = tk.Tk()
    app = FleetGUI(root, nav_graph, fleet_manager)
    root.mainloop()

if __name__ == "__main__":
    main()