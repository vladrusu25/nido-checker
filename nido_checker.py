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

def check_room_availability():
    try:
        response = requests.get(URL)
        data = response.json()

        for room in data.get('roomAvailability', []):
            for term in room.get('Terms', []):
                if term.get('RoomsAvailable', 0) > 0:
                    return (
                        f"🛏️ Room Available at {time.strftime('%H:%M:%S')}!\n"
                        f"Type: {room.get('RoomTypeDescription')}\n"
                        f"Price: {term.get('MinPriceFormatted')}\n"
                        f"📎 View: https://www.nidoliving.com/en-gb/netherlands/maastricht/randwyck/rooms"
                    )

        # Nothing found
        print(f"Checked at {time.strftime('%H:%M:%S')} - No rooms available.")
        return None

    except Exception as e:
        print(f"❌ Error checking availability at {time.strftime('%H:%M:%S')}: {e}")
        return None


async def main():
    while True:
        message = check_room_availability()
        if message:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            print(f"✅ Room alert sent at {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
