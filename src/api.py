"""FastAPI service for the agentic financial analytics assistant."""

from fastapi import FastAPI
from pydantic import BaseModel

from agents import Runner
from src.agents.guarded_manager_agent import guarded_manager_agent


app = FastAPI(
    title="Agentic Financial Analytics Assistant",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_assistant(request: QueryRequest):
    result = Runner.run_sync(
        guarded_manager_agent,
        request.question,
    )

    return QueryResponse(
        answer=result.final_output,
    )