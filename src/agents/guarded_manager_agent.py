"""Guarded version of the financial analytics manager."""

from src.agents.manager_agent import manager_agent
from src.guardrails.input_guardrail import financial_scope_guardrail


guarded_manager_agent = manager_agent.clone(
    name="Guarded Financial Analytics Manager",
    input_guardrails=[financial_scope_guardrail],
)