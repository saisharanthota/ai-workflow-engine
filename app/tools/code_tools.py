tool_registry = {}

def register_tool(name: str, func):
    tool_registry[name] = func
