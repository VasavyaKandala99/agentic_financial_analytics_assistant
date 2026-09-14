"""LLM-based evaluator for financial analytics responses."""

from pydantic import BaseModel, Field

from agents import Agent, Runner


class EvaluationResult(BaseModel):
    correctness: int = Field(ge=1, le=5)
    groundedness: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    reasoning: str


evaluation_agent = Agent(
    name="Financial Analytics Evaluator",
    instructions=(
        "Evaluate the assistant response against the user question and expected facts. "
        "Score correctness, groundedness, and relevance from 1 to 5. "
        "Correctness measures whether the answer matches the expected facts. "
        "Groundedness measures whether claims are supported by the supplied evidence "
        "and do not introduce unsupported numbers, definitions, or causal claims. "
        "Relevance measures whether the response directly answers the user's question. "
        "Be strict but fair and briefly explain the scores."
    ),
    output_type=EvaluationResult,
)


def evaluate_response(
    question: str,
    assistant_response: str,
    expected_facts: str,
) -> EvaluationResult:
    """Evaluate one assistant response."""

    prompt = f"""
User question:
{question}

Expected facts / evidence:
{expected_facts}

Assistant response:
{assistant_response}
"""

    result = Runner.run_sync(
        evaluation_agent,
        prompt,
    )

    return result.final_output