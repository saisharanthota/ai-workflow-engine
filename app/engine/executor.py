import uuid
import asyncio
import datetime

class WorkflowExecutor:
    def __init__(self):
        # Stores final states of all runs
        self.runs = {}

    async def run_graph(self, graph, init_state):
        run_id = str(uuid.uuid4())
        log = []
        state = init_state.copy()

        current = graph.start_node

        while current:
            node = graph.nodes[current]

            # Timestamped log entry (Optional Extra)
            timestamp = datetime.datetime.now().isoformat()
            log.append(f"[{timestamp}] Running node: {current}")

            # Run the node
            state = await node.run(state)

            # Determine the next node
            next_node = graph.edges.get(current)

            # Conditional branching (loop until quality >= threshold)
            if isinstance(next_node, dict):
                cond = next_node["condition"]
                
                # FIX: pass state explicitly into eval
                result = eval(cond, {"state": state})
                
                current = next_node["true"] if result else next_node["false"]
                continue

            # Normal flow to next node
            current = next_node

        # Save final state for /graph/state/{run_id} (Optional Extra)
        self.runs[run_id] = state

        return {
            "run_id": run_id,
            "final_state": state,
            "log": log
        }
