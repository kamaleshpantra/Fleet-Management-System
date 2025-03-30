import json
import networkx as nx
from typing import List, Dict, Tuple

class NavGraph:
    def __init__(self, json_path: str):
        self.graph = nx.Graph()
        self.load_from_json(json_path)

    def load_from_json(self, json_path: str):
        with open(json_path, 'r') as f:
            data = json.load(f)
        vertices = data.get('vertices', [])
        lanes = data.get('lanes', [])
        for idx, vertex in enumerate(vertices):
            x, y, attrs = vertex[0], vertex[1], vertex[2] if len(vertex) > 2 else {}
            self.graph.add_node(idx, pos=(x, y), **attrs)
        for lane in lanes:
            if len(lane) >= 2:
                self.graph.add_edge(lane[0], lane[1])

    def get_shortest_path(self, start: int, end: int) -> List[int]:
        try:
            return nx.shortest_path(self.graph, start, end)
        except nx.NetworkXNoPath:
            return []

    def get_vertex_position(self, vertex_id: int) -> Tuple[float, float]:
        return self.graph.nodes[vertex_id]['pos']

    def get_vertex_attributes(self, vertex_id: int) -> Dict:
        return {k: v for k, v in self.graph.nodes[vertex_id].items() if k != 'pos'}

    def get_all_vertices(self) -> List[int]:
        return list(self.graph.nodes)

    def get_all_edges(self) -> List[Tuple[int, int]]:
        return list(self.graph.edges)