from fastapi import FastAPI
from app.routers import graph as graph_router

app = FastAPI(
    title="AI Workflow Engine",
    description="A minimal workflow/agent engine built for internship assignment",
    version="1.0.0"
)

app.include_router(graph_router.router)
