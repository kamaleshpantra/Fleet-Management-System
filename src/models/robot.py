from enum import Enum
from typing import List, Optional
from src.utils.logger import log

class RobotStatus(Enum):
    IDLE = "Idle"
    MOVING = "Moving"
    WAITING = "Waiting"
    TASK_COMPLETE = "Task Complete"

class Robot:
    def __init__(self, robot_id: int, start_vertex: int):
        self.id = robot_id
        self.current_vertex = start_vertex
        self.destination_vertex: Optional[int] = None
        self.path: List[int] = []
        self.status = RobotStatus.IDLE
        self.color = self.generate_color(robot_id)
        self.progress = 0.0
        self.speed = 0.05

    @staticmethod
    def generate_color(robot_id: int) -> str:
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
        return colors[robot_id % len(colors)]

    def assign_task(self, destination: int, path: List[int]):
        self.destination_vertex = destination
        self.path = path[1:]
        self.status = RobotStatus.MOVING
        self.progress = 0.0
        log(f"Robot {self.id} assigned task to vertex {destination}")

    def update(self, traffic_manager):
        if self.status == RobotStatus.MOVING and self.path:
            next_vertex = self.path[0]
            edge = (self.current_vertex, next_vertex)
            if traffic_manager.request_move(self, edge):
                self.progress += self.speed
                if self.progress >= 1.0:
                    traffic_manager.complete_move(self, edge)
                    self.current_vertex = next_vertex
                    self.path.pop(0)
                    self.progress = 0.0
                    if not self.path:
                        self.status = RobotStatus.TASK_COMPLETE
                        log(f"Robot {self.id} completed task at vertex {self.current_vertex}")
            else:
                self.status = RobotStatus.WAITING
                log(f"Robot {self.id} waiting at vertex {self.current_vertex}")