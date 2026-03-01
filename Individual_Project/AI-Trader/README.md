# FTEC5660 — AI-Trader Reproducibility Study

**Student:** Wu Sitong (1155253147)
**Course:** FTEC5660 — Agentic AI for Business and FinTech
**Original Paper:** [AI-Trader: Benchmarking Autonomous Agents in Real-Time Financial Markets](https://arxiv.org/abs/2512.10971) (Fan et al., 2025)
**Original Repo:** [HKUDS/AI-Trader](https://github.com/HKUDS/AI-Trader)

## Overview

This repository reproduces the AI-Trader cryptocurrency trading experiment using Claude-3.7-Sonnet and implements one modification (risk-controlled prompt) with an additional control experiment (model upgrade to Claude-Sonnet-4.6).

### Experiments

| Experiment | Config File | Description |
|------------|-------------|-------------|
| **Reproduction** | `configs/default_crypto_config.json` | Claude-3.7-Sonnet, original prompt |
| **Control Group** | `configs/modified_crypto_config.json` | Claude-Sonnet-4.6, original prompt |
| **Modification** | `configs/risk_prompt_crypto_config.json` | Claude-3.7-Sonnet, risk-controlled prompt |

## Setup

### Prerequisites

- Python 3.10+
- Conda (recommended)
- API keys: Anthropic-compatible (e.g., aihubmix), Alpha Vantage, Jina AI

### Installation

```bash
# 1. Clone this repository
git clone https://github.com/YOUR_USERNAME/AI-Trader-Reproduction.git
cd AI-Trader-Reproduction

# 2. Create and activate conda environment
conda create -n xxsc python=3.10 -y
conda activate xxsc

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and fill in your API keys
```

### Running Experiments

```bash
# Step 1: Start MCP tool services (keep this running in a separate terminal)
python agent_tools/start_mcp_services.py

# Step 2: Run reproduction (Claude-3.7-Sonnet, original prompt)
python main.py configs/default_crypto_config.json

# Step 3: Run control group (Claude-Sonnet-4.6, original prompt)
python main.py configs/modified_crypto_config.json

# Step 4: Run modification (Claude-3.7-Sonnet, risk prompt)
python main.py configs/risk_prompt_crypto_config.json

# Step 5: Generate comparison charts
python generate_charts.py
```

## Project Structure

```
AI-Trader/
├── agent/
│   └── base_agent_crypto/
│       └── base_agent_crypto.py        # Trading agent (added prompt_variant support)
├── agent_tools/
│   ├── tool_trade.py                   # Trade tool (Windows fcntl→msvcrt fix)
│   └── tool_crypto_trade.py            # Crypto trade tool (same fix)
├── configs/
│   ├── default_crypto_config.json      # Reproduction config
│   ├── modified_crypto_config.json     # Control: Claude-Sonnet-4.6
│   └── risk_prompt_crypto_config.json  # Modification: risk prompt
├── prompts/
│   ├── agent_prompt_crypto.py          # Original prompt (unchanged)
│   └── agent_prompt_crypto_risk.py     # Risk-controlled prompt (new)
├── data/agent_data_crypto/
│   ├── claude-3.7-sonnet/              # Reproduction results
│   ├── claude-sonnet-4-6/              # Control group results
│   ├── claude-3.7-sonnet-risk/         # Modification results
│   └── claude-3.7-sonnet_PAPER_ORIGINAL/  # Paper reference data
├── report_output/                      # Generated charts (PNG)
├── main.py                             # Entry point (added prompt_variant passthrough)
├── generate_charts.py                  # Chart generation script
├── .env.example                        # API key template (fill in your own)
└── requirements.txt
```

## Code Changes from Original Repo

### Windows Compatibility (infrastructure only, no logic changes)

**`agent_tools/tool_trade.py` and `agent_tools/tool_crypto_trade.py`:**
- Added platform detection to replace Unix-only `fcntl` with Windows-compatible `msvcrt` for file locking.

### Modification: Risk-Controlled Prompt

**`prompts/agent_prompt_crypto_risk.py` (new file):**
- Based on the original `agent_prompt_crypto.py`, adds four risk management rules:
  - Position limit: max 30% per cryptocurrency
  - Cash reserve: maintain at least 20% ($10,000 USDT) in cash
  - Stop-loss: sell if >5% loss from entry
  - Diversification: spread across at least 3 cryptocurrencies

**`agent/base_agent_crypto/base_agent_crypto.py`:**
- Added `prompt_variant` parameter and a dispatch dictionary (`_PROMPT_VARIANTS`) to select between original and risk prompts at runtime.

**`main.py`:**
- Added `prompt_variant` reading from config and passthrough to agent constructor.

**`configs/risk_prompt_crypto_config.json` (new file):**
- Same as default config but with `"prompt_variant": "risk"` in `agent_config`.

**`configs/modified_crypto_config.json` (new file):**
- Same as default config but with model changed to `claude-sonnet-4-6`.

## Results Summary

| Metric | Paper Original | Reproduction | Control (4.6) | Modification (Risk) |
|--------|:-:|:-:|:-:|:-:|
| CR (%) | -15.30 | -17.65 | -16.25 | **-13.68** |
| SR | **-2.27** | -3.11 | -2.71 | -4.96 |
| Vol (%) | **32.18** | 36.08 | 34.45 | 37.44 |
| MDD (%) | -16.93 | -19.34 | -17.76 | **-15.15** |
| Win Rate | 51.4% | 47.3% | **54.4%** | 51.7% |
| Final Value | $42,348 | $41,174 | $41,877 | **$43,161** |

The risk-prompted Claude-3.7-Sonnet outperformed the unconstrained Claude-Sonnet-4.6, demonstrating that structured prompt-level risk management is more effective than model intelligence upgrades for financial trading.

## Notes

- **API Keys:** You must provide your own API keys in `.env`. See `.env.example` for required keys.
- **MCP Services:** All five services must be running before starting experiments.
- **Windows Users:** The `fcntl` compatibility fix is already applied. No additional steps needed.
- **Results Variance:** LLM-based trading is non-deterministic. Exact metric values will differ between runs, but overall trends should be consistent.
