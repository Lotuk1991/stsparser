from aiogram import Dispatcher, types
from parser_iaai import fetch_iaai_info_by_stock_number
from parser_copart import get_lot_info
import asyncio

user_auction = {}  # user_id: 'copart' | 'iaai'

def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Copart", "IAAI")
        await message.answer("🔍 Оберіть аукціон:", reply_markup=keyboard)

    @dp.message_handler(lambda msg: msg.text == "Copart")
    async def ask_copart(message: types.Message):
        user_auction[message.from_user.id] = "copart"
        await message.reply("🔢 Введіть *номер лота Copart*:", parse_mode="Markdown")

    @dp.message_handler(lambda msg: msg.text == "IAAI")
    async def ask_iaai(message: types.Message):
        user_auction[message.from_user.id] = "iaai"
        await message.reply("🔢 Введіть *номер лота IAAI* (stock number):", parse_mode="Markdown")

    @dp.message_handler(lambda msg: msg.text.isdigit() and len(msg.text) >= 6)
    async def handle_lot_number(message: types.Message):
        auction = user_auction.get(message.from_user.id)
        if not auction:
            await message.reply("❗️Спочатку оберіть аукціон: Copart або IAAI.")
            return

        await message.answer("⏳ Зачекайте...")

        if auction == "copart":
            result = await get_lot_info(message.text.strip())  # <--- await обязательно!
            await message.reply(result, parse_mode="HTML")

        elif auction == "iaai":
            data = fetch_iaai_info_by_stock_number(message.text)
            if "error" in data:
                await message.reply(data["error"])
                return

            text = "📄 *Інформація про авто IAAI:*\n"
            for k, v in data.items():
                text += f"*{k}*: {v}\n"
            await message.reply(text, parse_mode="Markdown")