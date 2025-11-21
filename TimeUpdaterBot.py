from telethon import TelegramClient, functions
from datetime import datetime
import asyncio
import logging
import time
import sys

# تنظیمات پیشرفته لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('telegram_bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# اطلاعات شما
API_ID = 20590237
API_HASH = 'fc781b623a1b8689652c0afbd936cc33'
PHONE_NUMBER = '+989050396751'

class TelegramTimeUpdater:
    def __init__(self):
        self.client = None
        self.is_running = True
        self.session_file = 'mahyae_session'
        
    async def initialize_client(self):
        """راه‌اندازی کلاینت تلگرام"""
        try:
            self.client = TelegramClient(
                self.session_file,
                API_ID,
                API_HASH,
                connection_retries=10,
                retry_delay=2,
                timeout=60
            )
            return True
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد کلاینت: {e}")
            return False
    
    async def connect_to_telegram(self):
        """اتصال به تلگرام"""
        try:
            if not self.client:
                if not await self.initialize_client():
                    return False
            
            await self.client.start(phone=PHONE_NUMBER)
            
            # بررسی اتصال
            me = await self.client.get_me()
            logger.info(f"✅ متصل شدیم به: {me.first_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در اتصال به تلگرام: {e}")
            return False
    
    def get_current_time(self):
        """دریافت زمان فعلی"""
        return datetime.now().strftime("%H:%M")
    
    async def update_profile_time(self):
        """آپدیت last name با زمان فعلی"""
        try:
            current_time = self.get_current_time()
            
            # آپدیت پروفایل
            await self.client(functions.account.UpdateProfileRequest(
                last_name=current_time
            ))
            
            logger.info(f"✅ Last name آپدیت شد: {current_time}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در آپدیت پروفایل: {e}")
            return False
    
    async def run_updater(self):
        """اجرای اصلی آپدیت‌کننده"""
        # اتصال به تلگرام
        if not await self.connect_to_telegram():
            logger.error("❌ نمی‌توان به تلگرام متصل شد")
            return
        
        logger.info("🚀 ربات آپدیت زمان فعال شد")
        logger.info("⏰ هر دقیقه last name آپدیت می‌شود")
        
        # حلقه اصلی آپدیت
        update_count = 0
        while self.is_running:
            try:
                success = await self.update_profile_time()
                if success:
                    update_count += 1
                    logger.info(f"📊 تعداد آپدیت‌ها: {update_count}")
                
                # انتظار 60 ثانیه
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"❌ خطا در حلقه اصلی: {e}")
                await asyncio.sleep(30)  # اگر خطا داشت، کمتر صبر کن
    
    def stop(self):
        """توقف ربات"""
        self.is_running = False
        logger.info("⏹️ ربات متوقف شد")

async def main_async():
    """تابع اصلی async"""
    updater = TelegramTimeUpdater()
    try:
        await updater.run_updater()
    except KeyboardInterrupt:
        updater.stop()
    except Exception as e:
        logger.error(f"❌ خطای غیرمنتظره: {e}")

def run_bot():
    """اجرای ربات با حلقه دائمی"""
    print("🤖 ربات آپدیت خودکار Last Name")
    print("📍 ساخته شده برای Render")
    print("⏰ هر دقیقه آپدیت می‌شود")
    print("🔄 سیستم Self-Building فعال")
    print("⏹️ برای توقف: Ctrl+C\n")
    
    restart_count = 0
    max_restarts = 50
    
    while restart_count < max_restarts:
        try:
            restart_count += 1
            print(f"🔄 اجرای شماره {restart_count}")
            
            # اجرای ربات
            asyncio.run(main_async())
            
            print("🔄 ریستارت در 10 ثانیه...")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n⏹️ برنامه توسط کاربر متوقف شد")
            break
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 تلاش مجدد در 30 ثانیه...")
            time.sleep(30)
    
    if restart_count >= max_restarts:
        print("❌ تعداد ریستارت‌ها بیش از حد مجاز")

if __name__ == "__main__":
    run_bot()
