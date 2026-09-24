"""A minimal *working* starter agent over the Northwind Outdoor dataset.

This is intentionally small — it's the thing you EXTEND, not a finished product. It uses the
Anthropic Python SDK's tool runner (a managed agent loop): you define typed tools, and the SDK
handles calling the model, executing your tools, and looping until the model is done.

You are encouraged to take this further with whatever lightweight agent framework you prefer —
the Anthropic Agent SDK / Managed Agents, the OpenAI Agents SDK, etc. The point of the take-home
is what you build on top of this, not this file.

Run:
    uv sync
    # paste the API key we provided into .env  (see .env.example)
    uv run python harness/agent.py "which products are on promotion in the next quarter?"
"""
from __future__ import annotations

import os
import sys

import anthropic
import pandas as pd
from anthropic import beta_tool

from load_data import TABLES, load_table

MODEL = "claude-opus-4-8"


def _load_dotenv() -> None:
    """Tiny .env reader so you don't need an extra dependency."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


@beta_tool
def describe_dataset() -> str:
    """List every available table and its columns so you know what you can query."""
    lines = []
    for name in TABLES:
        df = load_table(name)
        lines.append(f"{name} ({len(df):,} rows): {', '.join(df.columns)}")
    return "\n".join(lines)


@beta_tool
def query_demand_data(table: str, query: str = "", columns: str = "", limit: int = 25) -> str:
    """Query one table of the demand-planning dataset and return matching rows as CSV.

    Args:
        table: Table name (e.g. "fact_forecast", "dim_product", "fact_promo").
        query: Optional pandas .query() expression, e.g. "lifecycle_stage == 'EOL'"
            or "week >= '2026-06-01'". Leave empty for no filter.
        columns: Optional comma-separated columns to return. Leave empty for all columns.
        limit: Max rows to return (default 25).
    """
    if table not in TABLES:
        return f"Unknown table '{table}'. Available: {', '.join(TABLES)}"
    df = load_table(table)
    if query:
        try:
            df = df.query(query)
        except Exception as exc:  # surface the error back to the model so it can retry
            return f"Query error: {exc}"
    if columns:
        cols = [c.strip() for c in columns.split(",") if c.strip() in df.columns]
        if cols:
            df = df[cols]
    return df.head(limit).to_csv(index=False)


SYSTEM = (
    "You are Dawn, Daybreak's demand-planning agent, working over the Northwind Outdoor dataset. "
    "Use the tools to inspect and query the data before answering. Be concrete and cite the "
    "numbers you find."
)


def run(prompt: str) -> None:
    _load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Paste the key we provided into .env (see .env.example).")

    client = anthropic.Anthropic()
    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=SYSTEM,
        tools=[describe_dataset, query_demand_data],
        messages=[{"role": "user", "content": prompt}],
    )
    for message in runner:
        for block in message.content:
            if block.type == "text":
                print(block.text)


if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]) or "Give me a 3-bullet orientation to this dataset."
    run(user_prompt)
