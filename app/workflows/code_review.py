import re
import asyncio

# Extract function names using regex
async def extract_functions(state):
    code = state["code"]
    funcs = re.findall(r"def (.*?):", code)
    state["functions"] = funcs
    return state

# Simple complexity measure
async def check_complexity(state):
    state["complexity_score"] = len(state.get("functions", [])) * 2
    return state

# Identify TODO issues
async def detect_issues(state):
    code = state["code"]
    state["issues"] = code.count("TODO")
    return state

# Suggest improvements
async def suggest_improvements(state):
    if state["issues"] > 0:
        state["suggestions"] = ["Remove TODO comments", "Follow clean code style"]
    else:
        state["suggestions"] = ["Everything looks good"]
    return state

# Compute quality score
async def compute_quality(state):
    state["quality_score"] = max(0, 100 - state["issues"] * 10)
    return state
