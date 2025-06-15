# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 12:08:31 2025

@author: ayush
"""

import requests
from bs4 import BeautifulSoup
import time
import logging

# ===== CONFIGURATION =====
TELEGRAM_BOT_TOKEN = "7689875794:AAEFp7UBwlw4xuiWAb08e_lshS1YlZRkWdA"  # Your actual token
TELEGRAM_CHAT_ID = "6936930461"  # The number you just got (e.g., 123456789)
PRODUCT_URL = "https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-60-sachets"
CHECK_INTERVAL = 300  # 5 minutes (in seconds)

# ===== SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===== STOCK CHECKER =====
def check_stock():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check both button and stock text for reliability
        add_to_cart = soup.find('button', {'name': 'add-to-cart'})
        stock_status = soup.find('p', {'class': 'stock'})
        
        if (add_to_cart and 'disabled' not in add_to_cart.attrs) or \
           (stock_status and 'out of stock' not in stock_status.text.lower()):
            return True
        return False
        
    except Exception as e:
        logging.error(f"Error checking stock: {e}")
        return False

# ===== TELEGRAM ALERT =====
def send_alert():
    message = f"🚨 **AMUL WHEY PROTEIN IN STOCK!** 🚨\n\n{PRODUCT_URL}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    })

# ===== MAIN =====
if __name__ == "__main__":
    logging.info("Starting Amul Stock Monitor...")
    logging.info(f"Bot Token: {TELEGRAM_BOT_TOKEN[:5]}...{TELEGRAM_BOT_TOKEN[-5:]}")
    logging.info(f"Chat ID: {TELEGRAM_CHAT_ID}")
    
    try:
        while True:
            if check_stock():
                send_alert()
                logging.info("ALERT SENT! Exiting...")
                break
            logging.info("Still out of stock. Checking again soon...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Stopped by user")