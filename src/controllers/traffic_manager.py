from typing import Dict, Set, Tuple
from src.models.robot import Robot, RobotStatus
from src.utils.logger import log

class TrafficManager:
    def __init__(self):
        self.occupied_edges: Dict[Tuple[int, int], Robot] = {}
        self.occupied_vertices: Set[int] = set()
        self.waiting_queues: Dict[Tuple[int, int], Set[Robot]] = {}

    def request_move(self, robot: Robot, edge: Tuple[int, int]) -> bool:
        # Check if edge or destination vertex is occupied
        if (edge in self.occupied_edges or 
            edge[1] in self.occupied_vertices or 
            any(r.current_vertex == edge[1] for r in self.occupied_edges.values())):
            if edge not in self.waiting_queues:
                self.waiting_queues[edge] = set()
            self.waiting_queues[edge].add(robot)
            robot.status = RobotStatus.WAITING
            log(f"Robot {robot.id} waiting for edge {edge}")
            return False
        
        # Reserve the edge and destination vertex
        self.occupied_edges[edge] = robot
        self.occupied_vertices.add(edge[1])
        log(f"Robot {robot.id} moving on edge {edge}")
        return True

    def complete_move(self, robot: Robot, edge: Tuple[int, int]):
        if edge in self.occupied_edges:
            del self.occupied_edges[edge]
            self.occupied_vertices.remove(edge[1])
            log(f"Robot {robot.id} completed move on edge {edge}")
        
        # Check waiting queue
        if edge in self.waiting_queues and self.waiting_queues[edge]:
            next_robot = self.waiting_queues[edge].pop()
            if self.request_move(next_robot, edge):
                next_robot.status = RobotStatus.MOVING
                log(f"Robot {next_robot.id} resumed from queue on edge {edge}")