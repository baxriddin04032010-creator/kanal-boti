import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# O'zingizning Token va Kanal username'ingizni joylang:
BOT_TOKEN = "8874351962:AAG0i-3wVofwd0SWeP6hRRPxfJTyOmTUAas"
CHANNEL_ID = "@shshshbaxriddinsh"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Har kuni ertalab avtomatik joylanadigan post funksiyasi
async def daily_day_of_year_post():
    today = datetime.now()
    day_number = today.strftime("%j") # Yilning nechanchi kuni ekanligi (1-366)
    date_str = today.strftime("%d.%m.%Y")
    
    post_text = (
        f"📅 <b>Bugungi sana:</b> {date_str}\n"
        f"✨ Bugun <b>{today.year}-yilning {int(day_number)}-kuni!</b>\n\n"
        f"Kuningiz maroqli va unumli o'tsin! 🚀"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Ulashish", url=f"https://t.me/share/url?url=https://t.me/{CHANNEL_ID[1:]}")
            ]
        ]
    )
    
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Avto-post yuborishda xatolik: {e}")

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Men kanalga post chiqaruvchi va har kuni yilning nechanchi kuni ekanligini eslatuvchi botman.")

@dp.message()
async def post_to_channel(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Yoqdi", callback_data="like"),
                InlineKeyboardButton(text="💬 Ulashish", url=f"https://t.me/share/url?url=https://t.me/{CHANNEL_ID[1:]}")
            ]
        ]
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message.text, reply_markup=keyboard, parse_mode="HTML")
        await message.answer("✅ Post kanalingizga joylandi!")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

async def main():
    # Taymerni ishga tushirish (Har kuni ertalab soat 08:00 da post joylaydi)
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(daily_day_of_year_post, trigger="cron", hour=8, minute=0)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
