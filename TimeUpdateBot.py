from pyrogram import Client
from pyrogram.types import User
from datetime import datetime
import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# اطلاعات شما
API_ID = 20590237
API_HASH = 'fc781b623a1b8689652c0afbd936cc33'
PHONE_NUMBER = '+989050396751'

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
                api_hash=API_HASH,
                phone_number=PHONE_NUMBER
            )
            
            await self.client.start()
            me = await self.client.get_me()
            logger.info(f"✅ متصل شدیم به: {me.first_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در اتصال: {e}")
            return False
    
    def get_current_time(self):
        """دریافت زمان فعلی"""
        return datetime.now().strftime("%H:%M")
    
    async def update_profile(self):
        """آپدیت last name"""
        try:
            current_time = self.get_current_time()
            
            await self.client.update_profile(
                last_name=current_time
            )
            
            logger.info(f"✅ Last name آپدیت شد: {current_time}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در آپدیت: {e}")
            return False
    
    async def run(self):
        """اجرای اصلی"""
        if await self.connect_to_telegram():
            logger.info("🚀 ربات فعال شد")
            
            while self.is_running:
                try:
                    await self.update_profile()
                    await asyncio.sleep(60)
                except Exception as e:
                    logger.error(f"❌ خطا: {e}")
                    await asyncio.sleep(30)

async def main():
    updater = TelegramTimeUpdater()
    await updater.run()

if __name__ == "__main__":
    print("🤖 ربات آپدیت زمان فعال شد")
    asyncio.run(main())
