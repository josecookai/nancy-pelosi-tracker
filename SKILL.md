---
name: nancy-pelosi-tracker
description: >
  Automated tracking and reporting system for Nancy Pelosi's congressional stock
  trading disclosures. Monitors disclosed positions, tracks ticker performance,
  calculates option intrinsic values, and alerts on price movements.

  Use when: (1) Generating daily Pelosi trading portfolio reports,
  (2) Tracking specific disclosed positions (AMZN, NVDA, GOOGL, etc.),
  (3) Monitoring new Periodic Transaction Report (PTR) filings,
  (4) Setting up automated alerts for position changes or price targets.
---

# Nancy Pelosi Tracker

Track Nancy Pelosi's congressional stock trading disclosures with automated
portfolio monitoring, price tracking, and alerting.

## Overview

This skill provides automated tracking of Nancy Pelosi's disclosed stock positions,
including:
- Real-time price monitoring of disclosed holdings
- Option intrinsic value calculations
- New filing detection
- Price alert notifications
- Daily portfolio reports

## Supported Positions

Currently tracks disclosed positions including:
- **AMZN** - Call options $120 strike, Jan 2027 expiry
- **NVDA** - Call options (various strikes)
- **GOOGL** - Call options $150 strike, Jan 2027 expiry
- **AB** - AllianceBernstein stock position
- **VST** - Vistra Corp position
- **TEM** - Tempus AI position

## Commands

### Generate Report
```bash
clawd nancy-pelosi-tracker report [--notify <channel>]
```

Generate a comprehensive portfolio report with current prices, option valuations,
and position status. Optionally send to Telegram or email.

### Check New Filings
```bash
clawd nancy-pelosi-tracker check-filings [--alert-on-new]
```

Check for new Periodic Transaction Report (PTR) filings. With `--alert-on-new`,
send notification if new trades are detected.

### Refresh Price Data
```bash
clawd nancy-pelosi-tracker refresh
```

Update all position prices from Yahoo Finance API.

### View Position Details
```bash
clawd nancy-pelosi-tracker position --ticker <TICKER>
```

Show detailed information for a specific position including entry price,
current value, alerts, and performance metrics.

### Set Price Alerts
```bash
clawd nancy-pelosi-tracker alert --ticker <TICKER> --above <PRICE> --below <PRICE>
```

Configure price alerts for specific positions.

## Data Sources

- **Stock Prices**: Yahoo Finance API (real-time, 15-min delay)
- **Disclosure Data**: CapitolTrades API, House Clerk PTR database
- **Option Calculations**: Black-Scholes for intrinsic value

## Report Format

Reports include:
- Position summary with current prices
- Option intrinsic value calculations
- Days to expiry for options
- Alert status (triggered/pending)
- Key price levels (support/resistance)
- News and catalyst watchlist

## Automation

Set up cron jobs for automated monitoring:

```bash
# Daily report at 10:43 AM
0 10 * * * /path/to/scripts/generate-report.sh

# Check filings every 6 hours
0 */6 * * * /path/to/scripts/check-filings.sh
```

## Configuration

Edit `config/positions.json` to add or modify tracked positions:

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
      "disclosed_date": "2026-02-18",
      "alerts": {
        "upside": 240,
        "support": 190
      }
    }
  ]
}
```

## Extending to Other Politicians

To track other members of Congress:

1. Copy this skill structure
2. Update `config/positions.json` with new politician's disclosures
3. Modify `scripts/fetch-filings.py` to query different PTR sources
4. Rename skill folder and SKILL.md references

## Output Templates

Customize report format by editing `templates/report-template.md`.
Available variables:
- `{{date}}` - Report generation date
- `{{politician}}` - Politician name
- `{{positions}}` - Array of position objects
- `{{alerts}}` - Array of triggered alerts

## Dependencies

- Python 3.8+
- `requests` - API calls
- `python-dateutil` - Date calculations
- `jinja2` - Template rendering

## Notes

- Data is based on public PTR filings, delayed up to 45 days per STOCK Act
- Option quantities are often not fully disclosed; calculations use disclosed ranges
- This tool is for informational purposes only, not investment advice
- Congressional trading data has inherent delays; real-time positions may differ
