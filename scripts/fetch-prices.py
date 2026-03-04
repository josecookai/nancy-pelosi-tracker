#!/usr/bin/env python3
"""
Fetch stock prices from Yahoo Finance API
"""
import json
import requests
import sys
from datetime import datetime

def fetch_yahoo_price(ticker):
    """Fetch current price for a ticker from Yahoo Finance"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result['meta']
            
            price = meta.get('regularMarketPrice', 0)
            previous_close = meta.get('previousClose', price)
            change_pct = ((price - previous_close) / previous_close * 100) if previous_close else 0
            
            return {
                'ticker': ticker,
                'price': round(price, 2),
                'change_pct': round(change_pct, 2),
                'previous_close': round(previous_close, 2),
                'currency': meta.get('currency', 'USD'),
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}", file=sys.stderr)
    
    return None

def fetch_batch_prices(tickers):
    """Fetch prices for multiple tickers"""
    results = {}
    for ticker in tickers:
        data = fetch_yahoo_price(ticker)
        if data:
            results[ticker] = data
    return results

def update_positions_file(config_path):
    """Update positions.json with latest prices"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Get unique tickers
    tickers = list(set(p['ticker'] for p in config['positions'] if p['status'] == 'active'))
    
    # Fetch prices
    prices = fetch_batch_prices(tickers)
    
    # Update positions
    for position in config['positions']:
        if position['ticker'] in prices:
            position['current_price'] = prices[position['ticker']]['price']
            position['last_updated'] = datetime.now().isoformat()
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return prices

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch stock prices')
    parser.add_argument('--ticker', help='Single ticker to fetch')
    parser.add_argument('--config', default='config/positions.json', help='Config file path')
    parser.add_argument('--update', action='store_true', help='Update config file')
    
    args = parser.parse_args()
    
    if args.ticker:
        result = fetch_yahoo_price(args.ticker)
        print(json.dumps(result, indent=2))
    elif args.update:
        prices = update_positions_file(args.config)
        print(f"Updated {len(prices)} tickers")
        for ticker, data in prices.items():
            print(f"  {ticker}: ${data['price']} ({data['change_pct']}%)")
    else:
        # Just fetch without updating
        with open(args.config, 'r') as f:
            config = json.load(f)
        tickers = list(set(p['ticker'] for p in config['positions'] if p['status'] == 'active'))
        prices = fetch_batch_prices(tickers)
        print(json.dumps(prices, indent=2))
