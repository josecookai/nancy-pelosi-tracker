# 🗺️ Nancy Pelosi Tracker - Product Development Roadmap

**Version**: 2.0.0  
**Last Updated**: 2026-03-04  
**Status**: Phase 2 Planning

---

## 📋 Roadmap Overview

### Phase 1: MVP ✅ (Completed)
- [x] Core tracking infrastructure
- [x] Price data integration (Yahoo Finance)
- [x] Report generation (text + markdown)
- [x] Telegram notifications
- [x] GitHub repository setup

### Phase 2: Automation & Intelligence 🚧 (In Progress)
- [ ] 新披露自动检测 (Automated Filing Detection)
- [ ] 价格提醒系统 (Price Alert System)
- [ ] Web Dashboard (可视化界面)
- [ ] 扩展支持其他议员 (Multi-Politician Support)

### Phase 3: Scale & Analytics 📊 (Future)
- [ ] Performance backtesting
- [ ] Portfolio analytics & insights
- [ ] Predictive alerting
- [ ] Mobile app

---

## 🎯 Phase 2: Detailed Specifications

### 2.1 新披露自动检测 (Automated Filing Detection)

**Objective**: Automatically detect new PTR (Periodic Transaction Report) filings within 1 hour of publication

**Data Sources**:
- **Primary**: CapitolTrades API (https://api.capitoltrades.com)
- **Secondary**: House Clerk PTR Database (scraping)
- **Tertiary**: QuiverQuant feed

**Technical Requirements**:
```python
# Core functionality
- Poll CapitolTrades API every 30 minutes
- Parse new trades for Nancy Pelosi
- Extract: ticker, transaction_type, amount_range, date
- Compare against known positions database
- Trigger alert if new position or modification detected
- Auto-update positions.json with new data
```

**Alert Format**:
```
🚨 NEW PELOSI FILING DETECTED

📊 Transaction: BUY AMZN Call Options
💰 Amount: $500K - $1M
📅 Filed: 2026-03-04 (Transaction date: 2026-03-01)
📄 PTR ID: PTR-2026-03-04-001

🔗 View on CapitolTrades: [link]
```

**API Integration**:
```bash
# CapitolTrades API endpoint
GET https://api.capitoltrades.com/trades
  ?politician=Nancy%20Pelosi
  &from_date=2026-03-01
  &sort=-date
  
Headers:
  Authorization: Bearer {API_KEY}
```

**Assigned Developer**: Codex (API integration specialist)
**Estimated Effort**: 2-3 days
**Dependencies**: CapitolTrades API key

---

### 2.2 价格提醒系统 (Price Alert System)

**Objective**: Real-time price monitoring with configurable alerts for key price levels

**Features**:
- [ ] Upside target alerts (break above resistance)
- [ ] Support level alerts (break below support)
- [ ] Percentage change alerts (±5%, ±10%, ±15%)
- [ ] Option intrinsic value alerts (reaches ITM/ATM)
- [ ] Daily high/low summaries

**Alert Configuration Schema**:
```json
{
  "alerts": {
    "amzn-call-jan2027": {
      "upside_target": 240,
      "support_level": 190,
      "stop_loss": 180,
      "pct_change_threshold": 5,
      "intrinsic_value_alert": true
    },
    "nvda-call-jan2027": {
      "upside_target": 220,
      "support_level": 150,
      "break_even_alert": 800
    }
  },
  "notification_settings": {
    "telegram": {
      "chat_id": "1327790737",
      "silent_hours": "23:00-08:00"
    },
    "email": {
      "recipients": ["user@example.com"]
    }
  }
}
```

**Alert Triggers**:
```python
# Check logic
def check_alerts(position, current_price):
    alerts = []
    
    # Upside break
    if current_price >= position['alerts']['upside_target']:
        alerts.append(f"🚀 {position['ticker']} ABOVE target ${position['alerts']['upside_target']}!")
    
    # Support break
    if current_price <= position['alerts']['support_level']:
        alerts.append(f"⚠️ {position['ticker']} BELOW support ${position['alerts']['support_level']}")
    
    # Option specific
    if position['type'] == 'call_option':
        intrinsic = current_price - position['strike']
        if intrinsic > 0 and position.get('was_otm', True):
            alerts.append(f"💰 {position['ticker']} Call now ITM! Intrinsic: ${intrinsic:.2f}")
    
    return alerts
```

**Monitoring Frequency**:
- Market hours (9:30-16:00 ET): Every 5 minutes
- After hours: Every 30 minutes
- Pre-market: Every 15 minutes (8:00-9:30 ET)

**Assigned Developer**: Claude Code (Real-time systems specialist)
**Estimated Effort**: 2-3 days
**Dependencies**: Yahoo Finance API, Telegram bot

---

### 2.3 Web Dashboard (可视化持仓界面)

**Objective**: Web-based dashboard for visualizing portfolio performance

**Tech Stack**:
- **Frontend**: React + Tailwind CSS
- **Backend**: Python Flask/FastAPI
- **Database**: SQLite (local) or PostgreSQL (production)
- **Charts**: Chart.js or D3.js
- **Hosting**: Vercel/Netlify (frontend), Railway/Render (backend)

**Dashboard Views**:

#### 1. Portfolio Overview
```
┌─────────────────────────────────────────────────────┐
│  📊 Nancy Pelosi Portfolio Tracker                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [Portfolio Value Chart - 30/60/90 days]            │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Positions│ │   Day    │ │   Total  │           │
│  │    6     ││   +2.3%  │ │  +15.7%  │           │
│  └──────────┘ └──────────┘ └──────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 2. Position Details Table
```
┌────────┬──────────┬──────────┬──────────┬──────────┐
│Ticker  │ Type     │ Entry    │ Current  │ P&L      │
├────────┼──────────┼──────────┼──────────┼──────────┤
│ AMZN   │ Call $120│ $201.15  │ $208.03  │ +$6.88   │
│ NVDA   │ Call $800│ $185.50  │ $180.05  │ -$5.45   │
│ GOOGL  │ Call $150│ $306.52  │ $299.17  │ -$7.35   │
│ ...    │ ...      │ ...      │ ...      │ ...      │
└────────┴──────────┴──────────┴──────────┴──────────┘
```

#### 3. Option Greeks & Valuation
```
┌────────────────────────────────────────────────────┐
│  💰 AMZN Call Option Analysis                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  Strike: $120    Expiry: Jan 15, 2027             │
│  Days to Expiry: 318                              │
│                                                    │
│  [Intrinsic Value Gauge: $88.03 ▓▓▓▓▓▓▓▓▓▓]      │
│  [Moneyness: 73% ITM]                             │
│                                                    │
│  Estimated Contract Value: ~$9,500-$10,000        │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### 4. Historical Performance
- Line chart: Position value over time
- Heatmap: Daily P&L by position
- Calendar: Filing dates and earnings

**API Endpoints**:
```python
GET /api/portfolio           # Portfolio summary
GET /api/positions           # All positions
GET /api/positions/<ticker>  # Specific position
GET /api/performance         # Performance metrics
GET /api/alerts              # Active alerts
GET /api/filings             # Recent filings
```

**Assigned Developer**: Codex (Full-stack, dashboard specialist)
**Estimated Effort**: 5-7 days
**Dependencies**: Phase 2.1 and 2.2 completion

---

### 2.4 扩展支持其他议员 (Multi-Politician Support)

**Objective**: Refactor system to track multiple Congress members

**New Name**: `congress-trading-tracker`

**Supported Politicians** (Phase 2.4.1):
1. **Nancy Pelosi** (existing)
2. **Josh Gottheimer** (active trader)
3. **Dan Crenshaw**
4. **Ro Khanna**
5. **Susie Lee**

**Database Schema Refactor**:
```json
{
  "politicians": {
    "nancy-pelosi": {
      "name": "Nancy Pelosi",
      "chamber": "house",
      "party": "D",
      "state": "CA",
      "positions": [...]
    },
    "josh-gottheimer": {
      "name": "Josh Gottheimer",
      "chamber": "house",
      "party": "D",
      "state": "NJ",
      "positions": [...]
    }
  }
}
```

**CLI Commands**:
```bash
# Track specific politician
congress-tracker report --politician "Josh Gottheimer"

# Compare politicians
congress-tracker compare --politicians "Pelosi,Gottheimer,Crenshaw"

# List all tracked politicians
congress-tracker list-politicians

# Add new politician
congress-tracker add-politician --name "Ro Khanna" --id "ro-khanna"
```

**Telegram Bot Multi-Chat Support**:
```json
{
  "notification_channels": [
    {
      "politician": "nancy-pelosi",
      "telegram": "1327790737"
    },
    {
      "politician": "josh-gottheimer",
      "telegram": "987654321"
    }
  ]
}
```

**Renaming Plan**:
```bash
# Repository migration
mv nancy-pelosi-tracker congress-trading-tracker

# Update all internal references
sed -i 's/nancy-pelosi-tracker/congress-trading-tracker/g' *.py *.md

# Maintain backward compatibility
ln -s congress-trading-tracker nancy-pelosi-tracker  # symlink
```

**Assigned Developer**: Claude Code (Architecture & refactoring specialist)
**Estimated Effort**: 3-4 days
**Dependencies**: Phase 2.1, 2.2 completion

---

## 👥 Development Team Assignments

### Codex Tasks
- [ ] **2.1** CapitolTrades API integration
- [ ] **2.3** Web Dashboard (Frontend + Backend)
- [ ] **3.1** Performance backtesting engine

**Codex Specialization**: API integrations, data pipelines, full-stack development

### Claude Code Tasks
- [ ] **2.2** Price Alert System (real-time monitoring)
- [ ] **2.4** Multi-politician support (architecture refactoring)
- [ ] **3.2** Portfolio analytics engine

**Claude Code Specialization**: Real-time systems, architecture design, data modeling

---

## 📅 Development Timeline

### Sprint 1: Foundation (Week 1)
- **Day 1-2**: API integration (CapitolTrades)
- **Day 3-4**: Alert system core logic
- **Day 5**: Integration testing

### Sprint 2: Dashboard (Week 2)
- **Day 1-2**: Backend API development
- **Day 3-4**: Frontend dashboard
- **Day 5**: Dashboard deployment

### Sprint 3: Scale (Week 3)
- **Day 1-2**: Multi-politician database refactor
- **Day 3-4**: CLI command updates
- **Day 5**: Repository rename & migration

---

## 🔧 Technical Stack Summary

| Component | Technology |
|-----------|------------|
| CLI | Python 3.10+ |
| API | FastAPI/Flask |
| Frontend | React + Tailwind |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Charts | Chart.js |
| Hosting | Vercel + Railway |
| Notifications | Telegram Bot API |
| Data Sources | CapitolTrades, Yahoo Finance |

---

## 📊 Success Metrics

- [ ] New filings detected within 1 hour of publication
- [ ] Price alerts triggered in < 5 minutes during market hours
- [ ] Dashboard loads in < 2 seconds
- [ ] Support for 5+ politicians by end of Phase 2
- [ ] 99.9% uptime for alert system

---

## 📝 Notes

- **API Rate Limits**: CapitolTrades (100 req/min), Yahoo Finance (2000 req/hour)
- **Data Freshness**: PTR filings can be delayed up to 45 days per STOCK Act
- **Privacy**: All data is public record; tool provides aggregation only
- **Disclaimer**: Not investment advice; for informational purposes only

---

*Last updated: 2026-03-04 by Smrti Lab*
