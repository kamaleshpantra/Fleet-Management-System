import json

class NavGraph:
    def __init__(self, file_path):
        self.vertices = {}
        self.lanes = []
        self.load_graph(file_path)
        self.adjacency_list = self.build_adjacency_list()

    def load_graph(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        for item in data:
            if isinstance(item, list) and len(item) > 2:  # Vertex
                vertex_id = len(self.vertices)
                self.vertices[vertex_id] = {
                    "coordinates": item[:2],
                    "attributes": item[2]
                }
            elif isinstance(item, list) and len(item) == 2:  # Lane
                self.lanes.append(item)

    def get_vertex_by_name(self, name):
        for vertex_id, vertex in self.vertices.items():
            if vertex["attributes"].get("name") == name:
                return vertex_id
        return None

    def build_adjacency_list(self):
        """
        Builds an adjacency list representation of the graph for pathfinding.
        """
        adjacency_list = {vertex_id: [] for vertex_id in self.vertices}
        for lane in self.lanes:
            adjacency_list[lane[0]].append(lane[1])
            adjacency_list[lane[1]].append(lane[0])  # Assuming bidirectional lanes
        return adjacency_list

    def get_neighbors(self, vertex_id):
        """
        Returns a list of neighboring vertex IDs for a given vertex.
        """
        return self.adjacency_list.get(vertex_id, [])