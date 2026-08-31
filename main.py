import asyncio
import logging
import random
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = "8874351962:AAG0i-3wVofwd0SWeP6hRRPxfJTyOmTUAas"  # Tokeningizni to'liq joylashtiring
CHANNEL_ID = "@shshshbaxriddinsh"
ADMIN_ID = 7548485438

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
users = set()

NEWS_FACTS = [
    "Samarqanddagi Registon maydonida joylashgan Sherdor madrasasi peshtoqida quyosh va sher tasviri tushirilgan boʻlib, bu islom meʼmorchiligida kam uchraydigan noyob uslubdir.",
    "Buxorodagi Somoniylar maqbarasi Markaziy Osiyoda poydevoridan to gumbazigacha toʻliq pishgan gʻishtdan qurilgan eng qadimiy meʼmoriy obidadir.",
    "Toshkent metropoliteni Markaziy Osiyoda ishga tushirilgan birinchi metro hisoblanadi (1977-yil).",
    "Xivadagi Ichan-Qalʼa toʻliq saqlanib qolgan shaharlar-muzey boʻlib, YUNESKOning Butunjahon merosi roʻyxatiga kiritilgan birinchi obidadir.",
    "Shahrisabzdagi Oqsaroy majmuasi Amir Temur tomonidan qurdirilgan eng muazzam saroy boʻlib, uning ravogʻi oʻz davrida Markaziy Osiyoda eng kattasi boʻlgan.",
    "Buyuk alloma Muhammad al-Xorazmiy nol (0) raqamini matematikaga olib kirgan va 'Algoritm' hamda 'Algebra' fanlariga asos solgan.",
    "Fibonachchi ketma-ketligi (1, 1, 2, 3, 5, 8...) tabiatdagi chigʻanoqlar spiralida va kungaboqar urugʻlarining joylashishida aniq namoyon boʻladi.",
    "Inson tanasidagi qon tomirlarining umumiy uzunligi taxminan 100,000 kilometrni tashkil etadi — bu Yer sharini ikki yarim marta oʻrab chiqishga yetadi.",
    "Delfinlar uxlayotganida miyasining faqat bir yarim shari dam oladi, ikkinchi yarmi esa nafas olish va xavfni kuzatish uchun uygʻoq turadi."
]

async def check_sub(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception:
        return False

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    users.add(message.from_user.id)
    is_sub = await check_sub(message.from_user.id)
    if not is_sub:
        btn = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Kanalga a'zo bo'lish 📢", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")
        ]])
        await message.answer("Botdan foydalanish uchun avval kanalimizga a'zo bo'ling!", reply_markup=btn)
        return
    await message.answer("Xush kelibsiz! Kanallarga post yuborish uchun matn yoki media jo'nating.")

@dp.message(Command("stat"))
async def stat_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"📊 **Bot statistikasi:**\nJami foydalanuvchilar: {len(users)} ta")

async def send_daily_post():
    tz = pytz.timezone("Asia/Tashkent")
    now = datetime.now(tz)
    day_of_year = now.timetuple().tm_yday
    date_str = now.strftime("%Y-%m-%d")
    
    random_fact = random.choice(NEWS_FACTS)
    
    text = (
        f"📅 Bugungi sana: {date_str}\n"
        f"📊 Yilning {day_of_year}-kuni\n\n"
        f"💡 **Kun maʼlumoti:**\n{random_fact}"
    )
    
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
    except Exception as e:
        print(f"Post yuborishda xatolik: {e}")

@dp.message(F.text | F.photo | F.video)
async def forward_to_channel(message: types.Message):
    users.add(message.from_user.id)
    is_sub = await check_sub(message.from_user.id)
    if not is_sub:
        await message.answer("Avval kanalga a'zo bo'ling!")
        return
    await message.copy_to(chat_id=CHANNEL_ID)
    await message.answer("Post kanalingizga muvaffaqiyatli joylandi! ✅")

async def main():
    scheduler.add_job(send_daily_post, 'cron', hour=8, minute=0)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
yncio.run
