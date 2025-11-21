import os
import sys
import subprocess
import importlib
import requests
from datetime import datetime

def install_and_import(package):
    """نصب و ایمپورت خودکار کتابخانه‌ها"""
    try:
        importlib.import_module(package)
        print(f"✅ {package} از قبل نصب شده")
    except ImportError:
        print(f"📦 در حال نصب {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} با موفقیت نصب شد")

def create_requirements():
    """ساخت فایل requirements.txt"""
    requirements = """telethon==1.28.5
pytz==2023.3
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)
    print("✅ فایل requirements.txt ساخته شد")

def create_main_bot():
    """ساخت فایل اصلی ربات"""
    bot_code = '''from telethon import TelegramClient, functions
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
    print("⏹️ برای توقف: Ctrl+C\\n")
    
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
            print("\\n⏹️ برنامه توسط کاربر متوقف شد")
            break
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 تلاش مجدد در 30 ثانیه...")
            time.sleep(30)
    
    if restart_count >= max_restarts:
        print("❌ تعداد ریستارت‌ها بیش از حد مجاز")

if __name__ == "__main__":
    run_bot()
'''

    with open("TimeUpdaterBot.py", "w", encoding="utf-8") as f:
        f.write(bot_code)
    print("✅ فایل اصلی ربات ساخته شد")

def create_render_config():
    """ساخت فایل پیکربندی Render"""
    render_yaml = '''services:
  - type: web
    name: telegram-time-updater
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python TimeUpdaterBot.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
'''

    with open("render.yaml", "w", encoding="utf-8") as f:
        f.write(render_yaml)
    print("✅ فایل render.yaml ساخته شد")

def create_verification_bot():
    """ساخت ربات برای تأیید کد"""
    verification_code = '''import asyncio
from telethon import TelegramClient

async def verify_session():
    """تأیید session"""
    API_ID = 20590237
    API_HASH = 'fc781b623a1b8689652c0afbd936cc33'
    PHONE_NUMBER = '+989050396751'
    
    client = TelegramClient('mahyae_session', API_ID, API_HASH)
    
    try:
        await client.start(phone=PHONE_NUMBER)
        me = await client.get_me()
        print(f"✅ تأیید موفق! متصل به: {me.first_name}")
        await client.disconnect()
        return True
    except Exception as e:
        print(f"❌ خطا در تأیید: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_session())
'''

    with open("verify_session.py", "w", encoding="utf-8") as f:
        f.write(verification_code)
    print("✅ فایل تأیید session ساخته شد")

def main():
    """تابع اصلی ساخت خودکار"""
    print("🚀 شروع ساخت خودکار ربات...")
    print("=" * 50)
    
    # نصب کتابخانه‌های مورد نیاز
    print("📦 مرحله 1: نصب کتابخانه‌ها...")
    libraries = ['telethon', 'pytz']
    for lib in libraries:
        install_and_import(lib)
    
    # ساخت فایل‌ها
    print("\\n📁 مرحله 2: ساخت فایل‌ها...")
    create_requirements()
    create_main_bot()
    create_render_config()
    create_verification_bot()
    
    print("\\n✅ ساخت خودکار کامل شد!")
    print("=" * 50)
    print("📋 فایل‌های ساخته شده:")
    print("  📄 requirements.txt - لیست کتابخانه‌ها")
    print("  📄 TimeUpdaterBot.py - ربات اصلی")
    print("  📄 render.yaml - پیکربندی Render")
    print("  📄 verify_session.py - تأیید session")
    print("\\n🎯 مراحل بعدی:")
    print("  1. فایل‌ها را در GitHub آپلود کنید")
    print("  2. در Render.com اکانت بسازید")
    print("  3. از GitHub به Render متصل شوید")
    print("  4. ربات به صورت خودکار اجرا می‌شود")
    print("\\n⚠️ نکته: بار اول باید کد تأیید را وارد کنید")

if __name__ == "__main__":
    main()
