import logging
from src.utils.helpers import a_star_pathfinding

class FleetManager:
    def __init__(self, nav_graph, traffic_manager):
        self.nav_graph = nav_graph
        self.traffic_manager = traffic_manager
        self.robots = {}
        self.next_robot_id = 1
        self.logger = logging.getLogger(__name__)

    def spawn_robot(self, start_vertex):
        robot = Robot(self.next_robot_id, start_vertex)
        self.robots[self.next_robot_id] = robot
        self.next_robot_id += 1
        self.logger.info(f"Robot {robot.robot_id} spawned at vertex {start_vertex}")
        return robot

    def assign_task_to_robot(self, robot_id, destination_vertex):
        robot = self.robots.get(robot_id)
        if robot:
            robot.assign_task(destination_vertex)
            self.logger.info(f"Task assigned to Robot {robot.robot_id} to go to {destination_vertex}")
            self.plan_path_for_robot(robot)  # Plan the path immediately
            return True
        return False

    def plan_path_for_robot(self, robot):
        """
        Plans a path for the robot using A*.
        """
        if robot.destination_vertex is not None:
            path = a_star_pathfinding(
                self.nav_graph, robot.current_vertex, robot.destination_vertex
            )
            if path:
                robot.set_path(path[1:])  # Exclude the starting vertex
                robot.status = "moving"
                self.logger.info(f"Robot {robot.robot_id} path: {path}")
            else:
                self.logger.warning(f"No path found for Robot {robot.robot_id}")
                robot.status = "idle"  # Or handle this case appropriately

    def update_robot_statuses(self):
        """
        Updates the status of each robot and moves them along their paths.
        """
        for robot in self.robots.values():
            if robot.status == "moving":
                # Check for lane availability before moving
                next_lane = (robot.current_vertex, robot.next_vertex) if robot.next_vertex is not None else None
                if next_lane is not None and self.traffic_manager.check_lane_availability(next_lane):
                    self.traffic_manager.reserve_lane(next_lane)
                    robot.move_along_path()
                    self.logger.info(f"Robot {robot.robot_id} moved to vertex {robot.current_vertex}")
                    self.traffic_manager.release_lane(
                        (next_lane[0], next_lane[1])
                    )  # Release the lane after moving
                else:
                    robot.wait()
                    self.logger.warning(f"Robot {robot.robot_id} is waiting at vertex {robot.current_vertex}")
            elif robot.status == "planning":
                self.plan_path_for_robot(robot)

    def get_all_robots(self):
        return list(self.robots.values())