import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot

# Telegram setup
TELEGRAM_BOT_TOKEN = 'YOUR_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Selenium setup
options = Options()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)

URL = "https://nidoeurozone.starrezhousing.com/StarRezPortalX/D830A07A/101/2369/Booking-Select_your_Nido?HadEmptyContext=True"

def check_for_terms():
    driver.get(URL)
    time.sleep(5)  # Wait for dynamic content to load

    try:
        text_element = driver.find_element(By.CSS_SELECTOR, ".starrez-portal-page-content").text
        if "No terms available" not in text_element:
            print("✅ Term available!")
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="🎉 A new term has become available on the Nido booking page!")
            return True
        else:
            print(f"❌ Checked at {time.strftime('%H:%M:%S')} — No terms available.")
    except Exception as e:
        print(f"Error checking page: {e}")
    return False

try:
    while True:
        check_for_terms()
        time.sleep(10)
except KeyboardInterrupt:
    driver.quit()
