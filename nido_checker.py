import requests
import time
import asyncio
from telegram import Bot

# Telegram bot credentials
TELEGRAM_BOT_TOKEN = '7612678098:AAG8m1wxZThFox3lF7trEoZoodblI-qt1bU'
TELEGRAM_CHAT_ID = '950071182'

# API endpoint
URL = 'https://www.nidoliving.com/api/getRoomTypeAvailability?residenceId=39&countryCode=NL&locale=en-gb&ignoreEndDate=true'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def check_for_june_term():
    try:
        response = requests.get(URL)
        data = response.json()

        for term in data.get('terms', []):  # Top-level terms!
            description = term.get('description', '')
            print(description)
            if "ju" in description.lower():  # Use "june" here
                print(f"✅ Found June term: {description}")
                return (
                    f"📅 'June' term detected at {time.strftime('%H:%M:%S')}!\n"
                    f"Term: {description}\n"
                    f"Check-in: {term.get('checkInDate')}\n"
                    f"Check-out: {term.get('checkOutDate')}\n"
                    f"📎 View: https://www.nidoliving.com/en-gb/netherlands/maastricht/randwyck/rooms"
                )

        print(f"Checked at {time.strftime('%H:%M:%S')} - No June term found.")
        return None

    except Exception as e:
        print(f"❌ Error checking terms at {time.strftime('%H:%M:%S')}: {e}")
        return None


async def main():
    while True:
        message = check_for_june_term()
        if message:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            print(f"✅ June term alert sent at {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(10)  # For testing; increase to 60+ for production

if __name__ == '__main__':
    asyncio.run(main())
