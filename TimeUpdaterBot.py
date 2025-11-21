from telethon import TelegramClient, functions
from datetime import datetime
import pytz
import asyncio
import logging
import os
from flask import Flask
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# اطلاعات شما
API_ID = 20590237
API_HASH = 'fc781b623a1b8689652c0afbd936cc33'

# Flask app برای پورت
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Time Bot is Running!"

class TelegramTimeUpdater:
    def __init__(self):
        self.client = None
        self.is_running = True
        
    async def connect_to_telegram(self):
        """اتصال به تلگرام"""
        try:
            self.client = TelegramClient(
                "mahyae_session",
                API_ID,
                API_HASH
            )
            
            await self.client.start()
            me = await self.client.get_me()
            logger.info(f"✅ متصل شدیم به: {me.first_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در اتصال: {e}")
            return False
    
    def get_tehran_time(self):
        """دریافت وقت تهران"""
        try:
            tehran_tz = pytz.timezone('Asia/Tehran')
            tehran_time = datetime.now(tehran_tz)
            return tehran_time.strftime("%H:%M")
        except:
            # اگر pytz کار نکرد، از آفست استفاده کن
            utc_time = datetime.utcnow()
            tehran_time = utc_time.replace(hour=(utc_time.hour + 3) % 24, 
                                         minute=utc_time.minute + 30)
            # اگر دقیقه از 60 بیشتر شد
            if tehran_time.minute >= 60:
                tehran_time = tehran_time.replace(hour=(tehran_time.hour + 1) % 24,
                                                minute=tehran_time.minute - 60)
            return tehran_time.strftime("%H:%M")
    
    async def update_profile(self):
        """آپدیت last name"""
        try:
            current_time = self.get_tehran_time()
            
            await self.client(functions.account.UpdateProfileRequest(
                last_name=current_time
            ))
            
            logger.info(f"✅ Last name آپدیت شد: {current_time}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در آپدیت: {e}")
            return False
    
    async def run_telegram_bot(self):
        """اجرای ربات تلگرام"""
        logger.info("🚀 شروع ربات تلگرام...")
        if await self.connect_to_telegram():
            logger.info("✅ ربات تلگرام فعال شد")
            
            while self.is_running:
                try:
                    success = await self.update_profile()
                    if success:
                        await asyncio.sleep(60)  # هر دقیقه
                    else:
                        await asyncio.sleep(30)  # اگر خطا داشت
                except Exception as e:
                    logger.error(f"❌ خطا در حلقه اصلی: {e}")
                    await asyncio.sleep(30)
        else:
            logger.error("❌ نمی‌توان به تلگرام متصل شد")

def run_flask():
    """اجرای Flask روی پورت"""
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_telegram():
    """اجرای ربات تلگرام"""
    updater = TelegramTimeUpdater()
    asyncio.run(updater.run_telegram_bot())

def main():
    """تابع اصلی"""
    print("🤖 ربات آپدیت زمان فعال شد")
    
    # اجرای Flask در thread جداگانه
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # اجرای ربات تلگرام در thread اصلی
    telegram_thread = threading.Thread(target=run_telegram, daemon=True)
    telegram_thread.start()
    
    # نگه داشتن برنامه فعال
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("⏹️ برنامه متوقف شد")

if __name__ == "__main__":
    main()
