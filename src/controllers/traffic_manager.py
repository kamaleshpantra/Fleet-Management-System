
import logging

class TrafficManager:
    def __init__(self, nav_graph):
        self.nav_graph = nav_graph
        self.reserved_lanes = {}  # Track which lanes are occupied
        self.logger = logging.getLogger(__name__)

    def check_lane_availability(self, lane):
        """
        Checks if a lane is available.
        """
        return lane not in self.reserved_lanes

    def reserve_lane(self, lane):
        """
        Reserves a lane.
        """
        self.reserved_lanes[lane] = True
        self.logger.info(f"Lane {lane} reserved")

    def release_lane(self, lane):
        """
        Releases a reserved lane.
        """
        if lane in self.reserved_lanes:
            del self.reserved_lanes[lane]
            self.logger.info(f"Lane {lane} released")

    def handle_potential_collisions(self, robots):
        """
        Handles potential collisions between robots.
        This is a complex part and requires a strategy.
        A simple strategy is implemented here: robots wait if their next lane is occupied.
        """
        # Create a dictionary to track the next vertex for each robot
        next_vertices = {}
        for robot in robots:
            if robot.status == "moving" and robot.path:
                next_vertices[robot] = robot.path[0]

        # Check for conflicts (multiple robots heading to the same next vertex)
        conflicts = {}
        for robot1, next_vertex1 in next_vertices.items():
            for robot2, next_vertex2 in next_vertices.items():
                if robot1 != robot2 and next_vertex1 == next_vertex2:
                    if next_vertex1 not in conflicts:
                        conflicts[next_vertex1] = [robot1]
                    conflicts[next_vertex1].append(robot2)

        # Handle conflicts (e.g., make robots wait)
        for vertex, conflicting_robots in conflicts.items():
            # A simple strategy: make all conflicting robots wait
            for robot in conflicting_robots:
                robot.wait()
                self.logger.warning(
                    f"Collision avoided: Robot {robot.robot_id} waiting at vertex {robot.current_vertex}"
                )