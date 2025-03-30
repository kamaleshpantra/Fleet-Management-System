class Robot:
    def __init__(self, robot_id, start_vertex):
        self.robot_id = robot_id
        self.current_vertex = start_vertex
        self.destination_vertex = None
        self.path = []
        self.status = "idle"  # idle, moving, waiting, charging, complete
        self.next_vertex = None  # Track the next vertex the robot is moving towards

    def assign_task(self, destination_vertex):
        self.destination_vertex = destination_vertex
        self.status = "planning"

    def move_along_path(self):
        if self.path:
            self.next_vertex = self.path.pop(0)
            self.status = "moving"
            self.current_vertex = self.next_vertex  # Update current_vertex here
        else:
            self.status = "complete"
            self.next_vertex = None  # Reset next_vertex when path is complete

    def wait(self):
        self.status = "waiting"

    def set_path(self, path):
        self.path = path

    # Add methods for collision avoidance, charging, etc.