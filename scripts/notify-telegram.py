#!/usr/bin/env python3
"""
Send Telegram notification
"""
import os
import sys
import requests
import argparse

def send_telegram_message(message, chat_id, bot_token=None):
    """Send message to Telegram"""
    if not bot_token:
        # Try to get from environment or config
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("Error: No Telegram bot token provided", file=sys.stderr)
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print(f"Message sent successfully to {chat_id}")
            return True
        else:
            print(f"Error: {result.get('description')}", file=sys.stderr)
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
    
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Telegram notification')
    parser.add_argument('--message', '-m', required=True, help='Message to send')
    parser.add_argument('--chat-id', default='1327790737', help='Telegram chat ID')
    parser.add_argument('--bot-token', help='Bot token (or set TELEGRAM_BOT_TOKEN env)')
    
    args = parser.parse_args()
    
    success = send_telegram_message(args.message, args.chat_id, args.bot_token)
    sys.exit(0 if success else 1)
