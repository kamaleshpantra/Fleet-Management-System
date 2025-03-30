import json
import networkx as nx
from typing import List, Dict, Tuple
from src.utils.logger import log

class NavGraph:
    def __init__(self, json_path: str):
        self.graph = nx.Graph()
        self.load_from_json(json_path)

    def load_from_json(self, json_path: str):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            if "levels" in data and "level1" in data["levels"]:
                level_data = data["levels"]["level1"]
                vertices = level_data.get('vertices', [])
                lanes = level_data.get('lanes', [])
            else:
                vertices = data.get('vertices', [])
                lanes = data.get('lanes', [])

            if not vertices:
                log("Error: No vertices found in nav_graph")
                raise ValueError("No vertices in JSON file")

            for idx, vertex in enumerate(vertices):
                if len(vertex) >= 2:
                    x, y = vertex[0], vertex[1]
                    attrs = vertex[2] if len(vertex) > 2 else {}
                    self.graph.add_node(idx, pos=(x, y), **attrs)
                else:
                    log(f"Warning: Invalid vertex format at index {idx}")

            for lane in lanes:
                if len(lane) >= 2:
                    self.graph.add_edge(lane[0], lane[1])
                else:
                    log(f"Warning: Invalid lane format: {lane}")

            log(f"Loaded graph with {len(self.graph.nodes)} vertices and {len(self.graph.edges)} edges")
        except Exception as e:
            log(f"Error loading nav_graph: {str(e)}")
            raise

    def get_shortest_path(self, start: int, end: int) -> List[int]:
        try:
            return nx.shortest_path(self.graph, start, end)
        except nx.NetworkXNoPath:
            return []

    def get_vertex_position(self, vertex_id: int) -> Tuple[float, float]:
        return self.graph.nodes[vertex_id]['pos']

    def get_vertex_attributes(self, vertex_id: int) -> Dict:
        return {k: v for k, v in self.graph.nodes[vertex_id].items() if k != 'pos'}

    @property
    def nodes(self) -> List[int]:
        return list(self.graph.nodes)

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return list(self.graph.edges)