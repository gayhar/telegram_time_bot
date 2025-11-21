from pyrogram import Client
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
            self.client = Client(
                "mahyae_session",
                api_id=API_ID,
                api_hash=API_HASH
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
            # زمان UTC
            utc_now = datetime.utcnow()
            # تبدیل به تهران (UTC+3:30)
            tehran_hour = (utc_now.hour + 3) % 24
            tehran_minute = (utc_now.minute + 30) % 60
            if utc_now.minute + 30 >= 60:
                tehran_hour = (tehran_hour + 1) % 24
            
            return f"{tehran_hour:02d}:{tehran_minute:02d}"
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه زمان: {e}")
            return "00:00"
    
    async def update_profile(self):
        """آپدیت last name"""
        try:
            current_time = self.get_tehran_time()
            
            await self.client.update_profile(
                last_name=current_time
            )
            
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
            
            update_count = 0
            while self.is_running:
                try:
                    success = await self.update_profile()
                    if success:
                        update_count += 1
                        logger.info(f"📊 تعداد آپدیت‌ها: {update_count}")
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
    
    # اجرای ربات تلگرام
    run_telegram()

if __name__ == "__main__":
    main()
