# telegram_scraper.py
from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import emoji
import re
import logging

# Load environment variables
load_dotenv(r'C:\Users\Aman\Desktop\kifyaw5\dotenv.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('phone')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Preprocess text (remove emojis, normalize)
def preprocess_text(text):
    if text:
        text = emoji.demojize(text)
        text = re.sub(r'[^\w\s፡።፤፥፦፧]', '', text)
    return text or ""

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)

            # Preprocess message text
            processed_message = preprocess_text(message.message)

            # Write to CSV
            writer.writerow([channel_title, channel_username, message.id, processed_message, message.date, media_path])
    except Exception as e:
        logger.error(f"Error scraping {channel_username}: {e}")

# Initialize the client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()

    # Create directories
    root_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    media_dir = os.path.join(root_dir, 'data/photos')
    os.makedirs(media_dir, exist_ok=True)

    # Open CSV file
    with open('data/telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        # List of channels to scrape
        channels = [
        #    '@ZemenExpress',
        #    '@sinayelj',
        #    '@MerttEka',
        #    '@helloomarketethiopia',
           "@nevacomputer"
        ]

        for channel in channels:
            logger.info(f"Scraping channel: {channel}")
            await scrape_channel(client, channel, writer, media_dir)
            logger.info(f"Finished scraping {channel}")

with client:
    client.loop.run_until_complete(main())
