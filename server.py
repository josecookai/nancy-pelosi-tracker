#!/usr/bin/env python3
"""
Nancy Pelosi Stock Tracker - MCP Server for Claude Code
Tracks disclosed congressional stock positions via Yahoo Finance
"""
import json
import requests
from datetime import datetime, date
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nancy-pelosi-tracker")

POSITIONS_FILE = Path(__file__).parent / "positions.json"


def _load_positions() -> dict:
    try:
        with open(POSITIONS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"positions": []}
    except json.JSONDecodeError as e:
        raise ValueError(f"positions.json is malformed: {e}") from e


def _fetch_price(ticker: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        meta = data["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev = meta.get("previousClose", price)
        return {
            "ticker": ticker,
            "price": round(price, 2),
            "change_pct": round((price - prev) / prev * 100, 2) if prev else 0,
            "previous_close": round(prev, 2),
        }
    except Exception:
        return None


def _days_to_expiry(expiry_str: str) -> int:
    try:
        return max(0, (datetime.strptime(expiry_str, "%Y-%m-%d").date() - date.today()).days)
    except Exception:
        return 0


def _intrinsic_value(price: float, strike: float) -> float:
    return round(max(0, price - strike), 2)


def _moneyness(price: float, strike: float) -> float:
    return round((price - strike) / strike * 100, 1)


@mcp.tool()
def get_prices(tickers: list[str] | None = None) -> str:
    """
    Fetch current stock prices from Yahoo Finance.
    If tickers is None, fetches all active positions.
    """
    if tickers is None:
        config = _load_positions()
        tickers = list(dict.fromkeys(p["ticker"] for p in config["positions"] if p["status"] == "active"))

    results = []
    for t in tickers:
        data = _fetch_price(t)
        if data:
            sign = "+" if data["change_pct"] >= 0 else ""
            results.append(f"{t}: ${data['price']}  ({sign}{data['change_pct']}%)")
        else:
            results.append(f"{t}: fetch failed")

    return "\n".join(results)


@mcp.tool()
def generate_report() -> str:
    """
    Generate a full portfolio report with current prices, option valuations,
    and alert status for all active Pelosi positions.
    """
    config = _load_positions()
    active = [p for p in config["positions"] if p["status"] == "active"]
    tickers = list(dict.fromkeys(p["ticker"] for p in active))

    # Fetch all prices
    prices = {t: _fetch_price(t) for t in tickers}

    lines = [
        "📊 Nancy Pelosi Portfolio Tracker",
        "=" * 48,
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"💼 Active positions: {len(active)}",
        "",
    ]

    alerts_triggered = []

    for pos in active:
        ticker = pos["ticker"]
        price_data = prices.get(ticker)
        current = price_data["price"] if price_data else pos.get("current_price", 0)
        sign = ("+" if price_data["change_pct"] >= 0 else "") + str(price_data["change_pct"]) + "%" if price_data else "N/A"

        lines.append(f"📊 {ticker}  ${current}  ({sign})")

        if pos["type"] == "call_option":
            strike = pos["strike"]
            expiry = pos["expiry"]
            intrinsic = _intrinsic_value(current, strike)
            money = _moneyness(current, strike)
            dte = _days_to_expiry(expiry)
            itm_otm = "ITM" if money > 0 else "OTM"
            lines.append(f"   Call ${strike} | Expiry {expiry} ({dte}d)")
            lines.append(f"   Intrinsic: ${intrinsic}/share | {money}% {itm_otm}")
        elif pos["type"] == "stock":
            qty = pos.get("quantity")
            if isinstance(qty, int):
                lines.append(f"   Stock | {qty:,} shares | Est. ${current * qty:,.0f}")
            else:
                lines.append(f"   Stock | Range: {pos.get('value_range', 'unknown')}")

        if "alerts" in pos and price_data:
            up = pos["alerts"].get("upside_target")
            dn = pos["alerts"].get("support_level")
            if up and current >= up:
                lines.append(f"   🚨 ABOVE upside target ${up}")
                alerts_triggered.append(f"{ticker} ≥ ${up}")
            elif dn and current <= dn:
                lines.append(f"   🚨 BELOW support ${dn}")
                alerts_triggered.append(f"{ticker} ≤ ${dn}")
            else:
                lines.append(f"   🟢 Normal  ↑${up}  ↓${dn}")
        elif "alerts" in pos:
            lines.append(f"   ⚠️ Price unavailable — alerts skipped")

        if "notes" in pos:
            lines.append(f"   💡 {pos['notes']}")
        lines.append("")

    lines.append("🚨 Alert Summary")
    lines.append("-" * 30)
    if alerts_triggered:
        for a in alerts_triggered:
            lines.append(f"  ⚠️  {a}")
    else:
        lines.append("  🟢 No alerts triggered")

    return "\n".join(lines)


@mcp.tool()
def get_position(ticker: str) -> str:
    """
    Get detailed info for a single position by ticker symbol (e.g. AMZN, NVDA).
    """
    config = _load_positions()
    matches = [p for p in config["positions"] if p["ticker"].upper() == ticker.upper()]
    if not matches:
        return f"No position found for {ticker}"

    pos = matches[0]
    price_data = _fetch_price(ticker)
    current = price_data["price"] if price_data else pos.get("current_price", 0)

    lines = [f"=== {ticker} ==="]
    lines.append(f"Type: {pos['type']}")
    lines.append(f"Status: {pos['status']}")
    lines.append(f"Disclosed: {pos.get('disclosed_date', 'N/A')}")
    lines.append(f"Current price: ${current}")

    if price_data:
        lines.append(f"Change: {'+' if price_data['change_pct'] >= 0 else ''}{price_data['change_pct']}%")

    if pos["type"] == "call_option":
        strike = pos["strike"]
        expiry = pos["expiry"]
        lines.append(f"Strike: ${strike}")
        lines.append(f"Expiry: {expiry} ({_days_to_expiry(expiry)} days)")
        lines.append(f"Intrinsic value: ${_intrinsic_value(current, strike)}/share")
        lines.append(f"Moneyness: {_moneyness(current, strike)}%")

    if "alerts" in pos:
        lines.append(f"Upside target: ${pos['alerts'].get('upside_target')}")
        lines.append(f"Support level: ${pos['alerts'].get('support_level')}")

    if "notes" in pos:
        lines.append(f"Notes: {pos['notes']}")

    return "\n".join(lines)


@mcp.tool()
def check_filings() -> str:
    """
    Check House Clerk PTR database for recent Nancy Pelosi filings.
    Queries the public eFD API and returns any trades disclosed in the last 30 days.
    Note: STOCK Act allows up to 45-day disclosure delay.
    """
    url = "https://efts.house.gov/LATEST/search-index?q=%22Nancy+Pelosi%22&dateRange=custom&fromDate={from_date}&toDate={to_date}&type=ptr"
    from datetime import timedelta
    to_date = date.today().strftime("%Y-%m-%d")
    from_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    query_url = f"https://efts.house.gov/LATEST/search-index?q=%22Nancy+Pelosi%22&dateRange=custom&fromDate={from_date}&toDate={to_date}&type=ptr"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(query_url, headers=headers, timeout=10)
        if r.status_code != 200:
            return f"House eFD returned HTTP {r.status_code}"
        data = r.json()
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            return f"No new PTR filings found for Nancy Pelosi between {from_date} and {to_date}."
        lines = [f"📋 PTR Filings ({from_date} → {to_date})", "-" * 40]
        for h in hits:
            src = h.get("_source", {})
            lines.append(f"• {src.get('filing_date', 'N/A')}  {src.get('document_type', '')}  {src.get('pdf_url', '')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Could not reach House eFD: {e}"


if __name__ == "__main__":
    mcp.run()
