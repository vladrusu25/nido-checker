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

        return f"❌ No rooms available as of {time.strftime('%H:%M:%S')}."

    except Exception as e:
        error_message = f"❌ Error checking availability at {time.strftime('%H:%M:%S')}: {e}"
        print(error_message)
        return error_message


async def main():
    while True:
        message = check_room_availability()
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"✅ Telegram message sent at {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(60)  # check every 1 minute

if __name__ == '__main__':
    asyncio.run(main())
