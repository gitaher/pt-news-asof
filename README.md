# PersonalTrader News As Of

Select available, recent, ticker-relevant news and remove syndication duplicates at a fixed decision timestamp.

Supports timestamped news ingestion and prevents future-news leakage; does not extract EDGAR fields or judge sentiment.

## Tools

- `compute`: typed `TaskInput` to `TaskOutput`. No network, no model, no file writes.
- `screen-news`: agent task; call `compute` with the input and submit its typed result.
  The agent is permitted to choose its tool call, while arithmetic stays in code.
  No reference tool is needed: the verifier independently recomputes from immutable task arguments.

`contract.py` defines all fields. `tests/fixture.json` is a hand-computed example input and expected output.
The executable specification is in `verifier/checks.py`; the tool uses a separate implementation in
`src/plugin/logic.py`. Numeric tolerance is 1e-9 absolute/relative; all other values and order are exact.
Cutoffs are inclusive. UTC timestamps must be YYYY-MM-DDTHH:MM:SSZ. Invalid inputs raise errors.

## Layout

`src/plugin/`: MCP runtime and tools. `verifier/`: pure deterministic checks.
`tests/`: positive, negative and boundary tests plus a synthetic fixture.
`ui/`: schema renderer. `product/`: marketplace description.
Reports and execution evidence are deliberately kept outside this repository.

## Develop and run

Requires Git, uv, Python >=3.12. Dependencies are pinned in `uv.lock`.
The lock graph originates from the official arxiv-source reference, whose dependencies match this
plugin; only this project's name/version were changed. Validate it before publishing.

```bash
uv lock --check
uv sync --frozen --extra dev
uv run pytest
uv run ruff check .
```

Offline core verification (no dependencies, Python >=3.12):

```bash
python3 -m unittest discover -s tests -v
```

The contract round-trip test is skipped if slimconfig is unavailable; this is not full harness validation.
For full checks, install nanoagent separately and run `nanoagent plugin inspect <absolute-plugin-path>`.
Use `nanoagent plugin agent` with a `PluginOpenRouterAgentConfig` and an arguments JSON containing
the `input` object from `tests/fixture.json`; save the resulting verdict and trajectory outside this repo.
The platform selects its model; the plugin never selects or calls one itself.

Task limitations: Canonical syndication IDs and ticker tags are supplied, not inferred. No claim is made about factual reliability or sentiment understanding. Availability must reflect ingestion time.

Status remains `in-development` until frozen dependency setup, harness checks and a real agent run pass.
This repository contains synthetic test data, not Alpaca/SEC/live news observations or a completed trading study.
