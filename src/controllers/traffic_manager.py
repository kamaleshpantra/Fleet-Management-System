from typing import Dict, Set, Tuple
from src.models.robot import Robot

class TrafficManager:
    def __init__(self):
        self.occupied_edges: Dict[Tuple[int, int], Robot] = {}
        self.waiting_queues: Dict[Tuple[int, int], Set[Robot]] = {}

    def request_move(self, robot: Robot, edge: Tuple[int, int]) -> bool:
        if edge in self.occupied_edges or edge[1] in {r.current_vertex for r in self.occupied_edges.values()}:
            if edge not in self.waiting_queues:
                self.waiting_queues[edge] = set()
            self.waiting_queues[edge].add(robot)
            return False
        self.occupied_edges[edge] = robot
        return True

    def complete_move(self, robot: Robot, edge: Tuple[int, int]):
        if edge in self.occupied_edges:
            del self.occupied_edges[edge]
        if edge in self.waiting_queues and self.waiting_queues[edge]:
            next_robot = self.waiting_queues[edge].pop()
            if self.request_move(next_robot, edge):
                next_robot.status = RobotStatus.MOVING
                from src.utils.logger import log
                log(f"Robot {next_robot.id} resumed from queue")