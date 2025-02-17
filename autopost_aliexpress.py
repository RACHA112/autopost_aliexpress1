import requests
import time
from telegram import Bot
from datetime import datetime
import pytz

# Telegram Bot Token (Replace with your token)
TELEGRAM_BOT_TOKEN = '7601389265:AAHMx6qeOsHjO7dCKgXcfYEXGcfLZw5lXNM'
TELEGRAM_CHANNEL_ID = '@TopDealsEverBot'  # Replace with your channel username

# AliExpress Affiliate API Credentials (Replace with your credentials)
APP_KEY = '512774'
APP_SECRET = '8rpLXpFDuNdiBTWvPKesrSMUlZ4T6TAK'
AFFILIATE_API_URL = 'https://api.aliexpress.com/rest'

# Function to fetch products from AliExpress Affiliate API
def fetch_products(category_id, keywords):
    params = {
        'app_key': APP_KEY,
        'app_secret': APP_SECRET,
        'category_id': category_id,
        'keywords': keywords,
        'page_size': 10,  # Number of products to fetch
        'sort': 'priceAsc',  # Sort by price ascending
    }
    response = requests.get(f'{AFFILIATE_API_URL}/products', params=params)
    if response.status_code == 200:
        return response.json().get('data', {}).get('products', [])
    else:
        print(f"Failed to fetch products: {response.status_code}")
        return []

# Function to post products to Telegram channel
def post_to_telegram(bot, products):
    for product in products:
        title = product.get('title', 'No Title')
        price = product.get('price', 'N/A')
        product_url = product.get('product_url', '#')
        image_url = product.get('image_url', '')

        message = f"🚀 *{title}* 🚀\n\n"
        message += f"💰 *Price:* {price}\n"
        message += f"🔗 [Buy Now]({product_url})\n"

        try:
            if image_url:
                bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=image_url, caption=message, parse_mode='Markdown')
            else:
                bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode='Markdown')
        except Exception as e:
            print(f"Failed to send message: {e}")

# Function to check if current time matches any of the specified posting times
def is_time_to_post():
    # Define time zones
    utc = pytz.utc
    et = pytz.timezone('US/Eastern')  # USA Eastern Time
    cet = pytz.timezone('CET')  # Central European Time

    # Get current time in UTC
    now_utc = datetime.now(utc)

    # Convert to ET and CET
    now_et = now_utc.astimezone(et)
    now_cet = now_utc.astimezone(cet)

    # Define posting times for USA (ET) and Europe (CET)
    usa_times = ['08:00', '12:00', '18:00', '22:00']  # 8 AM, 12 PM, 6 PM, 10 PM ET
    europe_times = ['08:00', '12:00', '18:00', '22:00']  # 8 AM, 12 PM, 6 PM, 10 PM CET

    # Check if current time matches any posting time in ET or CET
    current_time_et = now_et.strftime('%H:%M')
    current_time_cet = now_cet.strftime('%H:%M')

    return current_time_et in usa_times or current_time_cet in europe_times

# Main function
def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    while True:
        if is_time_to_post():
            # Fetch products from AliExpress Affiliate API
            products = fetch_products(category_id='100003070', keywords='smartphone')  # Example category and keywords
            if products:
                post_to_telegram(bot, products)

            # Sleep for 1 minute to avoid multiple posts in the same minute
            time.sleep(60)

        # Sleep for 30 seconds before checking again
        time.sleep(30)

if __name__ == '__main__':
    main()