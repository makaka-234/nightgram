import asyncio
import random
import string
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "8868607092:AAF2xYWHzv1eT85SFzEXUBY-2OQqRwyx0P8"
OWNER_ID = 8707911673

users = {}
codes = {}

router = Router()

def menu():
    kb = [
        [KeyboardButton(text="🔑 Получить код")],
        [KeyboardButton(text="⭐ Купить звёзды")],
        [KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="ℹ️ О NightGram")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart())
async def start(message: Message):
    tg_id = message.from_user.id
    if tg_id not in users:
        users[tg_id] = {"tg_id": tg_id, "username": message.from_user.username, "stars": 1000}
    await message.answer("🌙 <b>NightGram</b>\n\nЯ — бот для входа в NightGram.\nВыбери действие 👇", reply_markup=menu())

@router.message(F.text == "🔑 Получить код")
async def get_code(message: Message):
    tg_id = message.from_user.id
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    codes[tg_id] = code
    number = "+7 999 " + str(random.randint(100, 999)) + "-" + str(random.randint(10, 99)) + "-" + str(random.randint(10, 99))
    text = "🔑 <b>Данные для входа</b>\n\n"
    text += "📱 Номер: <code>" + number + "</code>\n"
    text += "🔐 Код: <code>" + code + "</code>\n\n"
    text += "⭐ Бонус: 1000 звёзд"
    await message.answer(text)

@router.message(F.text == "⭐ Купить звёзды")
async def buy_stars(message: Message):
    text = "⭐ <b>Купить звёзды</b>\n\n"
    text += "• 100 звёзд — 99 ₽\n"
    text += "• 500 звёзд — 449 ₽\n"
    text += "• 1000 звёзд — 849 ₽\n"
    text += "• 5000 звёзд — 3999 ₽"
    await message.answer(text)

@router.message(F.text == "👤 Профиль")
async def profile(message: Message):
    tg_id = message.from_user.id
    user = users.get(tg_id)
    if not user:
        await message.answer("Сначала /start")
        return
    text = "👤 <b>Профиль</b>\n\n"
    text += "🆔 ID: <code>" + str(user["tg_id"]) + "</code>\n"
    text += "🔤 Username: @" + (user["username"] or "—") + "\n"
    text += "⭐ Звёзды: <b>" + str(user["stars"]) + "</b>"
    await message.answer(text)

@router.message(F.text == "ℹ️ О NightGram")
async def about(message: Message):
    await message.answer("🌙 <b>NightGram</b>\n\nСвой мессенджер.\nСкоро — приложение!")

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(router)
    print("✅ Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
