# 🏛️ Nancy Pelosi Tracker

> Automated tracking and reporting system for Nancy Pelosi's congressional stock trading disclosures

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

This tool automatically tracks Nancy Pelosi's disclosed stock positions, monitors real-time prices, calculates option valuations, and generates daily reports. It provides transparency into congressional trading activity as required by the STOCK Act.

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

## 📁 Project Structure

```
nancy-pelosi-tracker/
├── SKILL.md                    # Skill documentation
├── package.json                # Project metadata
├── README.md                   # This file
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

- [x] Core tracking and reporting
- [x] Telegram notifications
- [x] Option valuation calculations
- [ ] Web dashboard
- [ ] CapitolTrades API integration
- [ ] Automatic new filing detection
- [ ] Historical performance backtesting
- [ ] Expand to other Congress members (congress-trading-tracker)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related

- [CapitolTrades](https://capitoltrades.com) - Congressional trading database
- [House Clerk PTR](https://clerk.house.gov) - Official disclosure source
- [STOCK Act](https://en.wikipedia.org/wiki/STOCK_Act) - Stop Trading on Congressional Knowledge Act

---

Made with 💰 by Smrti Lab
