from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from app.engine.node import Node
from app.engine.graph import WorkflowGraph
from app.engine.executor import WorkflowExecutor
from app.workflows.code_review import (
    extract_functions,
    check_complexity,
    detect_issues,
    suggest_improvements,
    compute_quality,
)

router = APIRouter(prefix="/graph", tags=["Graph"])

# Create executor instance
executor = WorkflowExecutor()

# Define workflow nodes
nodes = {
    "extract": Node("extract", extract_functions),
    "complexity": Node("complexity", check_complexity),
    "issues": Node("issues", detect_issues),
    "suggestions": Node("suggestions", suggest_improvements),
    "quality": Node("quality", compute_quality),
}

# Define edges (includes loop condition)
edges = {
    "extract": "complexity",
    "complexity": "issues",
    "issues": "suggestions",
    "suggestions": "quality",
    "quality": {
        "condition": "state['quality_score'] < state['threshold']",
        "true": "issues",
        "false": None
    }
}

# Create workflow graph
workflow_graph = WorkflowGraph(nodes, edges, start_node="extract")



# Data Model for Run Request

class RunRequest(BaseModel):
    code: str
    threshold: int = 80



# Main Workflow Execution API

@router.post("/run")
async def run_graph(request: RunRequest):
    init_state = {
        "code": request.code,
        "threshold": request.threshold
    }
    result = await executor.run_graph(workflow_graph, init_state)
    return result



# Optional Extra 1: Get State by run_id

@router.get("/state/{run_id}")
async def get_state(run_id: str):
    if run_id not in executor.runs:
        return {"error": "Invalid run_id"}
    return {"run_id": run_id, "state": executor.runs[run_id]}



# Optional Extra 2: Background Execution

@router.post("/run/background")
async def run_graph_background(request: RunRequest, background: BackgroundTasks):

    init_state = {
        "code": request.code,
        "threshold": request.threshold
    }

    async def background_job():
        # Workflow runs in background
        await executor.run_graph(workflow_graph, init_state)

    background.add_task(background_job)

    return {"message": "Workflow started in background"}
