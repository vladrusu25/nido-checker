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
                        f"🛏️ Room Available!\n"
                        f"Type: {room.get('RoomTypeDescription')}\n"
                        f"Price: {term.get('MinPriceFormatted')}\n"
                        f"📎 View: https://www.nidoliving.com/en-gb/netherlands/maastricht/randwyck/rooms"
                    )
        return None

    except Exception as e:
        print("❌ Error checking availability:", e)
        return None


async def main():
    notified = False
    while True:
        message = check_room_availability()
        if message and not notified:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            print("✅ Telegram message sent.")
            notified = True
        elif not message:
            print(f"Checked at {time.strftime('%H:%M:%S')} - No rooms available yet.")
            notified = False

        await asyncio.sleep(60)  # check every 2 minutes

if __name__ == '__main__':
    asyncio.run(main())
