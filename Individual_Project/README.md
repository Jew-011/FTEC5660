# FTEC5660 Individual Project — AI-Trader Reproducibility Study

**Student:** Wu Sitong (1155253147)
**Course:** FTEC5660 — Agentic AI for Business and FinTech
**Original Paper:** AI-Trader: Benchmarking Autonomous Agents in Real-Time Financial Markets (Fan et al., 2025)

---

## Folder Structure

```
Individual_Project/
├── README.md                 ← You are here
├── AI-Trader/                ← All source code, configs, data, and results
│   ├── agent/                    # Trading agent (modified for prompt_variant)
│   ├── agent_tools/              # MCP tools (Windows compatibility fix applied)
│   ├── configs/                  # Experiment configurations
│   ├── prompts/                  # Original + risk-controlled prompts
│   ├── data/agent_data_crypto/   # Experiment results for all 4 runs
│   ├── report_output/            # Generated comparison charts
│   ├── main.py                   # Entry point
│   ├── generate_charts.py        # Chart generation script
│   └── README.md                 # Detailed setup & running instructions
```

---

## Where to View Commit History

All code changes are tracked with clear, descriptive commits in my forked repository:

> **Full commit history:** [https://github.com/Jew-011/AI-Trader/commits/main/](https://github.com/Jew-011/AI-Trader/commits/main/)

The commits are organized as follows:

| Commit | Description |
|--------|-------------|
| `fix: add Windows compatibility for file locking` | Replace Unix `fcntl` with `msvcrt` for Windows |
| `feat: add experiment config files` | Add configs for Claude-4.6 and risk prompt experiments |
| `feat: add prompt_variant support and risk-controlled prompt` | Core modification: dynamic prompt loading + risk rules |
| `data: add experiment results for all four experiments` | All trading logs and portfolio data |
| `docs: update README, .gitignore, .env.example and add chart generation script` | Documentation and tooling |
| `docs: add experiment comparison charts` | Visualization outputs |

> **Forked repository (full code + commit history):** [https://github.com/Jew-011/AI-Trader](https://github.com/Jew-011/AI-Trader)
>
> **Original repository:** [https://github.com/HKUDS/AI-Trader](https://github.com/HKUDS/AI-Trader)

---

## Experiments Overview

| Experiment | Config File | Description |
|------------|-------------|-------------|
| **Reproduction** | `configs/default_crypto_config.json` | Claude-3.7-Sonnet, original prompt |
| **Control Group** | `configs/modified_crypto_config.json` | Claude-Sonnet-4.6, original prompt |
| **Modification** | `configs/risk_prompt_crypto_config.json` | Claude-3.7-Sonnet, risk-controlled prompt |

All three experiments use the same trading period (2025-11-01 to 2025-11-15) and initial capital ($50,000 USDT) on the Bitwise 10 crypto portfolio.

---

## Results Summary

| Metric | Paper Original | Reproduction | Control (4.6) | Modification (Risk) |
|--------|---------------|--------------|---------------|---------------------|
| CR (%) | -15.30 | -17.65 | -16.25 | **-13.68** |
| SR | **-2.27** | -3.11 | -2.71 | -4.96 |
| MDD (%) | -16.93 | -19.34 | -17.76 | **-15.15** |
| Win Rate | 51.4% | 47.3% | **54.4%** | 51.7% |
| Final Value | $42,348 | $41,174 | $41,877 | **$43,161** |

**Key Finding:** The risk-prompted Claude-3.7-Sonnet achieved the best cumulative return and lowest drawdown, outperforming the newer Claude-Sonnet-4.6 model. This demonstrates that structured prompt-level risk management is more effective than model upgrades for financial trading.

---

## How to Run (Quick Start)

For detailed setup instructions, see [`AI-Trader/README.md`](AI-Trader/README.md).

```bash
cd AI-Trader/

# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env   # then edit .env with your keys

# 3. Start MCP services (in a separate terminal)
python agent_tools/start_mcp_services.py

# 4. Run any experiment
python main.py configs/default_crypto_config.json        # Reproduction
python main.py configs/modified_crypto_config.json       # Control (Claude-4.6)
python main.py configs/risk_prompt_crypto_config.json     # Modification (Risk prompt)
```

---

## Code Changes from Original Repository

For a detailed diff, see the commit history: [https://github.com/Jew-011/AI-Trader/commits/main/](https://github.com/Jew-011/AI-Trader/commits/main/)

### Modified Files
- `agent_tools/tool_trade.py` — Windows file locking compatibility
- `agent_tools/tool_crypto_trade.py` — Windows file locking compatibility
- `agent/base_agent_crypto/base_agent_crypto.py` — Added `prompt_variant` support
- `main.py` — Added `prompt_variant` config passthrough

### New Files
- `prompts/agent_prompt_crypto_risk.py` — Risk-controlled system prompt
- `configs/modified_crypto_config.json` — Claude-Sonnet-4.6 experiment config
- `configs/risk_prompt_crypto_config.json` — Risk prompt experiment config
- `generate_charts.py` — Comparison chart generation
