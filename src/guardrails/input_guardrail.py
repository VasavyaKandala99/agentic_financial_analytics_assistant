"""Input guardrail for the financial analytics assistant."""

from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from agents.decorators import input_guardrail


class ScopeCheck(BaseModel):
    is_in_scope: bool
    reasoning: str


scope_guardrail_agent = Agent(
    name="Scope Guardrail",
    instructions=(
        "Determine whether the user's request is within the scope of a "
        "financial analytics assistant. "
        "In-scope topics include transaction analytics, KPIs, country performance, "
        "financial analytics concepts, liquidity, and related business definitions. "
        "General unrelated requests should be marked out of scope."
    ),
    output_type=ScopeCheck,
)


@input_guardrail
async def financial_scope_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        scope_guardrail_agent,
        input,
        context=ctx.context,
    )

    scope_result = result.final_output

    return GuardrailFunctionOutput(
        output_info=scope_result,
        tripwire_triggered=not scope_result.is_in_scope,
    )