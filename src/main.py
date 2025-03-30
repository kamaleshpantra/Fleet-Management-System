import logging
import os
from src.models.nav_graph import NavGraph
from src.controllers.fleet_manager import FleetManager
from src.controllers.traffic_manager import TrafficManager
from src.gui.fleet_gui import FleetGUI

if __name__ == "__main__":
    # Set up logging
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename=os.path.join(log_dir, "fleet_logs.txt"),
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        nav_graph = NavGraph("data/nav_graph.json")
        traffic_manager = TrafficManager(nav_graph)
        fleet_manager = FleetManager(nav_graph, traffic_manager)
        gui = FleetGUI(fleet_manager, traffic_manager, nav_graph)
        gui.run()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)