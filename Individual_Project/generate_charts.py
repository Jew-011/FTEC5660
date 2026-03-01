import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['figure.dpi'] = 150

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data", "agent_data_crypto")
OUT_DIR = os.path.join(BASE, "report_output")
os.makedirs(OUT_DIR, exist_ok=True)

experiments = {
    "Paper Original": "claude-3.7-sonnet_PAPER_ORIGINAL",
    "Reproduction (3.7-Sonnet)": "claude-3.7-sonnet",
    "Mod 1: Claude-Sonnet-4.6": "claude-sonnet-4-6",
    "Mod 2: Risk Prompt": "claude-3.7-sonnet-risk",
}

colors = {
    "Paper Original": "#2196F3",
    "Reproduction (3.7-Sonnet)": "#FF9800",
    "Mod 1: Claude-Sonnet-4.6": "#4CAF50",
    "Mod 2: Risk Prompt": "#E91E63",
}

# ── Chart 1: Portfolio Value Over Time ──
fig, ax = plt.subplots(figsize=(12, 6))

for label, folder in experiments.items():
    csv_path = os.path.join(DATA_DIR, folder, "position", "portfolio_values.csv")
    df = pd.read_csv(csv_path)
    daily = df.groupby("date")["total_value"].last().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    ax.plot(daily["date"], daily["total_value"], label=label, color=colors[label], linewidth=2)

ax.axhline(y=50000, color='gray', linestyle='--', alpha=0.5, label='Initial Capital ($50,000)')
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Portfolio Value (USDT)", fontsize=12)
ax.set_title("Portfolio Value Over Time — Four Experiments Comparison", fontsize=14, fontweight='bold')
ax.legend(loc='lower left', fontsize=10)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "portfolio_curves.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Saved portfolio_curves.png")

# ── Chart 2: Performance Metrics Comparison (Bar Chart) ──
metrics_data = {}
for label, folder in experiments.items():
    json_path = os.path.join(DATA_DIR, folder, "position", "performance_metrics.json")
    with open(json_path, 'r') as f:
        metrics_data[label] = json.load(f)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Performance Metrics Comparison — Four Experiments", fontsize=16, fontweight='bold', y=1.02)

metric_configs = [
    ("CR", "Cumulative Return (%)", lambda m: m["CR"] * 100, True),
    ("SR", "Sortino Ratio", lambda m: m["SR"], True),
    ("Vol", "Volatility (%)", lambda m: m["Vol"] * 100, False),
    ("MDD", "Max Drawdown (%)", lambda m: m["MDD"] * 100, True),
    ("Win Rate", "Win Rate (%)", lambda m: m["Win Rate"] * 100, True),
    ("Trades", "Number of Trades", lambda m: m["Number of Trades"], False),
]

labels = list(experiments.keys())
short_labels = ["Paper\nOriginal", "My\nReprod.", "Sonnet\n4.6", "Risk\nPrompt"]

for idx, (key, ylabel, extractor, higher_better) in enumerate(metric_configs):
    ax = axes[idx // 3][idx % 3]
    values = [extractor(metrics_data[l]) for l in labels]
    bar_colors = [colors[l] for l in labels]
    bars = ax.bar(short_labels, values, color=bar_colors, edgecolor='white', linewidth=0.5)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(key, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, values):
        fmt = f"{val:.2f}" if abs(val) < 100 else f"{val:.0f}"
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                fmt, ha='center', va='bottom' if val >= 0 else 'top', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "metrics_comparison.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Saved metrics_comparison.png")

# ── Chart 3: Daily Returns Distribution ──
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Daily Return Distribution — Four Experiments", fontsize=16, fontweight='bold')

for idx, (label, folder) in enumerate(experiments.items()):
    ax = axes[idx // 2][idx % 2]
    csv_path = os.path.join(DATA_DIR, folder, "position", "portfolio_values.csv")
    df = pd.read_csv(csv_path)
    daily = df.groupby("date")["total_value"].last().reset_index()
    daily["return"] = daily["total_value"].pct_change()
    daily = daily.dropna()
    ax.bar(range(len(daily)), daily["return"] * 100, color=colors[label], alpha=0.7)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_title(label, fontsize=11, fontweight='bold')
    ax.set_ylabel("Daily Return (%)")
    ax.set_xlabel("Trading Day")
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "daily_returns.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Saved daily_returns.png")

# ── Chart 4: Cumulative Return Comparison ──
fig, ax = plt.subplots(figsize=(12, 6))

for label, folder in experiments.items():
    csv_path = os.path.join(DATA_DIR, folder, "position", "portfolio_values.csv")
    df = pd.read_csv(csv_path)
    daily = df.groupby("date")["total_value"].last().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily["cum_return"] = (daily["total_value"] / 50000 - 1) * 100
    ax.plot(daily["date"], daily["cum_return"], label=label, color=colors[label], linewidth=2)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Cumulative Return (%)", fontsize=12)
ax.set_title("Cumulative Return Over Time — Four Experiments", fontsize=14, fontweight='bold')
ax.legend(loc='lower left', fontsize=10)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "cumulative_returns.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Saved cumulative_returns.png")

# ── Chart 5: Cash Position Over Time ──
fig, ax = plt.subplots(figsize=(12, 6))

for label, folder in experiments.items():
    csv_path = os.path.join(DATA_DIR, folder, "position", "portfolio_values.csv")
    df = pd.read_csv(csv_path)
    daily = df.groupby("date")["cash"].last().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily["cash_pct"] = daily["cash"] / 50000 * 100
    ax.plot(daily["date"], daily["cash_pct"], label=label, color=colors[label], linewidth=2)

ax.axhline(y=20, color='red', linestyle=':', alpha=0.5, label='20% Cash Reserve Rule')
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Cash as % of Initial Capital", fontsize=12)
ax.set_title("Cash Position Over Time — Risk Prompt Maintains Cash Reserve", fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "cash_positions.png"), dpi=150, bbox_inches='tight')
plt.close()
print("Saved cash_positions.png")

print("\nAll charts generated successfully in report_output/")
