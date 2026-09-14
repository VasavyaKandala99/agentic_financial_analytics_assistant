# Agentic Financial Analytics Assistant

An agentic financial analytics application that combines SQL-based analytics, retrieval-augmented generation (RAG), tool calling, multi-agent orchestration, persistent session memory, guardrails, and automated evaluation.

This project uses privacy-safe simulated financial transaction data and contains no proprietary or employer data.

## What It Does

The assistant can:

- Analyze monthly transaction KPIs from a SQL-backed dataset
- Compare country-level transaction performance
- Retrieve financial definitions and analytical guidance from a vector-store knowledge base
- Route questions to specialized agents
- Coordinate multiple specialists through a manager-agent architecture
- Preserve conversation context with SQLite-backed sessions
- Use handoffs for specialist routing
- Block out-of-scope requests with input guardrails
- Evaluate responses for correctness, groundedness, and relevance

## Architecture

The project is organized around specialized components:

- **Data Analysis Specialist**  
  Uses SQL-backed tools for monthly KPIs and country-level transaction analysis.

- **Business Knowledge Specialist**  
  Uses RAG and hosted file search to retrieve financial definitions and supporting business knowledge.

- **Financial Analytics Manager**  
  Coordinates the data and knowledge specialists using Agents-as-Tools.

- **Triage / Handoff Agents**  
  Demonstrate decentralized routing between specialists.

- **Guarded Manager**  
  Applies an input guardrail to restrict the assistant to supported financial analytics topics.

- **Evaluator Agent**  
  Scores responses for correctness, groundedness, and relevance.

## Tech Stack

- Python
- SQL / SQLite
- OpenAI API
- OpenAI Agents SDK
- Retrieval-Augmented Generation (RAG)
- Vector Search / File Search
- Function and Tool Calling
- Multi-Agent Orchestration
- SQLiteSession
- Pydantic
- pytest
- pandas

## Project Structure

```text
agentic-financial-analytics-assistant/
├── data/
│   └── sample/
├── notebooks/
│   └── development.ipynb
├── scripts/
│   └── build_sample_database.py
├── src/
│   ├── agents/
│   │   ├── data_agent.py
│   │   ├── guarded_manager_agent.py
│   │   ├── handoff_agents.py
│   │   ├── knowledge_agent.py
│   │   ├── manager_agent.py
│   │   └── session.py
│   ├── evaluation/
│   │   └── evaluator.py
│   ├── guardrails/
│   │   └── input_guardrail.py
│   ├── rag/
│   │   └── knowledge_search.py
│   └── tools/
│       └── analytics_tools.py
├── tests/
│   └── test_smoke.py
├── .env.example
├── .gitignore
├── requirements.txt
└── requirements-dev.txt