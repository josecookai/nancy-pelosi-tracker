# 🏛️ Nancy Pelosi Tracker

> Automated tracking and reporting system for Nancy Pelosi's congressional stock trading disclosures
> 
> **🤖 Now compatible with OpenClaw Skill & Claude Code Skill**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawd.bot)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-green)](https://claude.ai)

## 📋 Overview

This tool automatically tracks Nancy Pelosi's disclosed stock positions, monitors real-time prices, calculates option valuations, and generates daily reports. It provides transparency into congressional trading activity as required by the STOCK Act.

**Dual Skill Support**: This repository works as both an **OpenClaw Skill** and a **Claude Code Skill**, allowing seamless integration with both AI agent platforms.

## ✨ Features

- 📊 **Portfolio Tracking**: Monitor all disclosed positions (AMZN, NVDA, GOOGL, etc.)
- 💰 **Option Valuations**: Calculate intrinsic values and moneyness for LEAPS
- 🔔 **Price Alerts**: Set custom alerts for key price levels
- 📱 **Telegram Integration**: Automatic daily reports to your channel
- 📈 **Performance Metrics**: Track position performance since disclosure
- 🔍 **New Filing Detection**: Monitor for new PTR (Periodic Transaction Report) filings

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/josecookai/nancy-pelosi-tracker.git
cd nancy-pelosi-tracker

# Generate report
./scripts/pelosi-tracker report

# Generate markdown report for Telegram
./scripts/pelosi-tracker report --format markdown --notify telegram

# Update price data
./scripts/pelosi-tracker refresh

# Check for new filings
./scripts/pelosi-tracker check-filings
```

## 🤖 Skill Integration

### OpenClaw Skill

Install as an OpenClaw skill to enable natural language commands:

```bash
# Install skill
clawdhub install nancy-pelosi-tracker

# Use via OpenClaw
clawd nancy-pelosi-tracker report
clawd nancy-pelosi-tracker position AMZN
clawd nancy-pelosi-tracker check-filings --alert-on-new
```

**OpenClaw Commands:**
- `Generate Pelosi portfolio report` → Auto-detects and runs tracker
- `Check for new Pelosi trades` → Checks CapitolTrades API
- `What's the status of AMZN position?` → Shows position details
- `Set alert for NVDA at $200` → Configures price alert

### Claude Code Skill

Use with Claude Code for advanced analysis and development:

```bash
# In Claude Code workspace
/claude nancy-pelosi-tracker analyze
/claude nancy-pelosi-tracker backtest --days 90
/claude nancy-pelosi-tracker extend --politician "Josh Gottheimer"
```

**Claude Code Features:**
- **Code Analysis**: Review and improve tracker logic
- **API Integration**: Implement new data sources
- **Architecture**: Refactor for multi-politician support
- **Dashboard**: Build web visualization
- **Backtesting**: Historical performance analysis

### Skill Development Mode

Both platforms can collaborate on development:

```bash
# Codex handles API integrations
@codex Implement CapitolTrades API connection per ROADMAP.md 2.1

# Claude Code handles architecture
@claude-code Refactor database schema for multi-politician support
```

See [ROADMAP.md](ROADMAP.md) for detailed task assignments.

## 📁 Project Structure

```
nancy-pelosi-tracker/
├── SKILL.md                    # OpenClaw skill documentation
├── README.md                   # This file
├── ROADMAP.md                  # Development roadmap (Phase 2-3)
├── package.json                # Project metadata
├── .clawdhublink               # OpenClaw Hub registration
├── config/
│   └── positions.json          # Tracked positions database
├── scripts/
│   ├── pelosi-tracker          # Main CLI entry point
│   ├── fetch-prices.py         # Yahoo Finance API integration
│   ├── generate-report.py      # Report generation
│   ├── check-filings.py        # New filing detection
│   └── notify-telegram.py      # Telegram bot integration
└── templates/
    └── report-template.md      # Report formatting template
```

## 📊 Tracked Positions

| Ticker | Type | Strike | Expiry | Status |
|--------|------|--------|--------|--------|
| AMZN | Call Option | $120 | Jan 2027 | 🟢 Active |
| NVDA | Call Option | $800 | Jan 2027 | 🟢 Active |
| GOOGL | Call Option | $150 | Jan 2027 | 🟢 Active |
| AB | Stock | - | - | 🟢 Active |
| VST | Stock | - | - | 🟢 Active |
| TEM | Stock | - | - | 🟢 Active |

## ⚙️ Configuration

Edit `config/positions.json` to customize:

```json
{
  "politician": "Nancy Pelosi",
  "positions": [
    {
      "id": "amzn-call-jan2027",
      "ticker": "AMZN",
      "type": "call_option",
      "strike": 120,
      "expiry": "2027-01-15",
      "alerts": {
        "upside_target": 240,
        "support_level": 190
      }
    }
  ]
}
```

## 🤖 Automation

### Cron Setup

```bash
# Daily report at 10:43 AM
0 10 * * * cd /path/to/nancy-pelosi-tracker && ./scripts/pelosi-tracker report --format markdown --notify telegram

# Check filings every 6 hours
0 */6 * * * cd /path/to/nancy-pelosi-tracker && ./scripts/pelosi-tracker check-filings

# Refresh prices hourly
0 * * * * cd /path/to/nancy-pelosi-tracker && ./scripts/pelosi-tracker refresh
```

## 📈 Sample Report

```
📊 Nancy Pelosi Portfolio Tracker Report
==================================================
📅 Report Date: 2026-03-04 10:43
📈 Last Data Update: 2026-03-04

💼 Active Positions: 6

📊 AMZN
   Type: Call Option $120 Strike
   Expiry: 2027-01-15 (318 days)
   Current: $208.03
   Intrinsic Value: $88.03/share
   Moneyness: 73.4% ITM
   🟢 Status: Normal range
   💡 Deep ITM call, ~73% moneyness, strong AI/AWS thesis

📊 NVDA
   Type: Call Option $800 Strike
   Expiry: 2027-01-15 (318 days)
   Current: $180.05
   Intrinsic Value: $0.00/share
   Moneyness: -77.5% OTM
   🟢 Status: Normal range
   💡 AI/semiconductor play, high volatility
```

## 🔌 API Data Sources

- **Stock Prices**: Yahoo Finance API (real-time, 15-min delay)
- **Disclosure Data**: CapitolTrades API / House Clerk PTR Database
- **Option Calculations**: Intrinsic value based on Black-Scholes principles

## ⚠️ Disclaimer

- Data is based on public PTR filings, delayed up to 45 days per STOCK Act
- Option quantities are often not fully disclosed
- This tool is for **informational purposes only**, not investment advice
- Congressional trading data has inherent delays; real-time positions may differ

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed Phase 2-3 specifications.

### Phase 1: MVP ✅ (Completed)
- [x] Core tracking and reporting
- [x] Telegram notifications
- [x] Option valuation calculations
- [x] OpenClaw Skill support
- [x] Claude Code Skill support

### Phase 2: Automation 🚧 (In Progress)
- [ ] CapitolTrades API integration → **@codex**
- [ ] Real-time price alert system → **@claude-code**
- [ ] Web dashboard → **@codex**
- [ ] Multi-politician support → **@claude-code**

### Phase 3: Scale 📊 (Planned)
- [ ] Historical performance backtesting
- [ ] Predictive analytics
- [ ] Mobile app
- [ ] Community contributions

**Development Approach**: Phase 2-3 tasks are split between **Codex** (API/Full-stack) and **Claude Code** (Real-time systems/Architecture) for parallel development. See ROADMAP.md for task assignments.

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

### Dual Skill Development Workflow

This project uses both OpenClaw and Claude Code for parallel development:

1. **Feature Request** → Create GitHub issue
2. **Task Assignment** → Assign to @codex or @claude-code per ROADMAP.md
3. **Development** → Agent implements feature in their branch
4. **Code Review** → Other agent reviews PR
5. **Integration** → Merge to main, update both skill registries

**Example Workflow:**
```bash
# Assign API integration to Codex
gh issue create --title "Integrate CapitolTrades API" \
  --assignee "@codex" \
  --label "enhancement,api"

# Assign alert system to Claude Code  
gh issue create --title "Build price alert system" \
  --assignee "@claude-code" \
  --label "enhancement,real-time"
```

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related

- [CapitolTrades](https://capitoltrades.com) - Congressional trading database
- [House Clerk PTR](https://clerk.house.gov) - Official disclosure source
- [STOCK Act](https://en.wikipedia.org/wiki/STOCK_Act) - Stop Trading on Congressional Knowledge Act

---

Made with 💰 by Smrti Lab
