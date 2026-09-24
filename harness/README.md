# Starter harness (optional)

A minimal, working starting point. Use it if you want Dawn genuinely reasoning over the data
behind your prototype. Faking the agent and spending your hours on the interface is an equally
valid choice for this exercise — just tell us which you did.

- `load_data.py` — tidy loaders for every CSV in `../data`. `load_all()` returns a dict of
  DataFrames; `load_table("fact_forecast")` loads one.
- `agent.py` — a tiny agent built on the Anthropic Python SDK's tool runner (a managed agent
  loop). It has two tools (`describe_dataset`, `query_demand_data`) and answers questions about
  the data. Extend it if it serves your design — add tools, or wire it to whatever
  surface you build.

## Run it

```bash
uv sync                       # install dependencies
# paste the API key we provided into .env  (copy .env.example to .env first)
cp .env.example .env

uv run python harness/load_data.py                    # sanity-check the data loads
uv run python harness/agent.py "what's launching or being discontinued this year?"
```

## Notes

- **We provide the API key.** You will (or should have already!) receive one with this assignment — paste it into
  `.env`. Don't use your own and absolutely DO NOT expose it to the open internet! If you didn't get a key, tell us.
- **Use whatever tools you prefer.** This starter uses the Anthropic SDK's tool runner for
  convenience. Claude Code, Cursor, v0, plain HTML — all fine. We care about what you build,
  not the stack.
- Python 3.12+ and [`uv`](https://docs.astral.sh/uv/) are assumed.
