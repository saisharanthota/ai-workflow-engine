class WorkflowGraph:
    def __init__(self, nodes: dict, edges: dict, start_node: str):
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node
