from typing import Dict
from src.models.robot import Robot, RobotStatus
from src.models.nav_graph import NavGraph
from src.controllers.traffic_manager import TrafficManager
from src.utils.logger import log

class FleetManager:
    def __init__(self, nav_graph: NavGraph):
        self.robots: Dict[int, Robot] = {}
        self.nav_graph = nav_graph
        self.traffic_manager = TrafficManager()
        self.next_robot_id = 0

    def spawn_robot(self, vertex: int) -> int:
        if vertex not in self.nav_graph.nodes:
            raise ValueError(f"Invalid vertex {vertex}")
        if any(r.current_vertex == vertex for r in self.robots.values()):
            raise RuntimeError(f"Vertex {vertex} is occupied")
        robot_id = self.next_robot_id
        self.robots[robot_id] = Robot(robot_id, vertex)
        self.next_robot_id += 1
        log(f"Robot {robot_id} spawned at vertex {vertex}")
        return robot_id

    def assign_task(self, robot_id: int, destination: int) -> bool:
        if robot_id not in self.robots:
            return False
        robot = self.robots[robot_id]
        path = self.nav_graph.get_shortest_path(robot.current_vertex, destination)
        if not path:
            log(f"Robot {robot_id}: No path to vertex {destination}")
            return False
        robot.assign_task(destination, path)
        log(f"Robot {robot_id} assigned task to {destination} with path {path}")
        return True

    def update(self):
        for robot in self.robots.values():
            robot.update(self.traffic_manager)

    def get_robot_positions(self) -> Dict[int, tuple]:
        positions = {}
        for robot in self.robots.values():
            if robot.status == RobotStatus.MOVING and robot.path:
                start_pos = self.nav_graph.get_vertex_position(robot.current_vertex)
                next_pos = self.nav_graph.get_vertex_position(robot.path[0])
                x = start_pos[0] + (next_pos[0] - start_pos[0]) * robot.progress
                y = start_pos[1] + (next_pos[1] - start_pos[1]) * robot.progress
                positions[robot.id] = (x, y)
            else:
                positions[robot.id] = self.nav_graph.get_vertex_position(robot.current_vertex)
        return positions

    def get_robot_statuses(self) -> Dict[int, str]:
        return {r.id: r.status.value for r in self.robots.values()}

    def get_robot_colors(self) -> Dict[int, str]:
        return {r.id: r.color for r in self.robots.values()}