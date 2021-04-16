from aiogram import executor, exceptions, Dispatcher, Bot, types
import asyncio
from config import API_TOKEN
from keyboards import general_menu, Keyboards

bot = Bot(API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await message.answer(f"✋Здравствуйте, <b>{message.from_user.first_name}!</b>\n"
                         f"🤖Я бот для регистрации в игре <b>«Монополия»</b>\n\n"
                         f"⬇️Воспользуйтесь меню ниже для того что бы продолжить", reply_markup=general_menu)


@dp.message_handler(lambda message: message.text == "💬Правила игры")
async def view_rules(message: types.Message):
    await message.answer("Здесь либо текст с правилами либо ссылка на статью telega.ph")

@dp.message_handler(lambda message: message.text == "📆Даты игр")
async def view_dates(message: types.Message):
    keyb = Keyboards().get_dates_keyb()
    if keyb:
        await message.answer("🗒<b>Список доступных игр</b>\n\n💡<em>Число в квадратных скобках обозначает количество забронированных мест</em>", reply_markup=keyb)
    else:
        await message.answer("На данный момент доступных игр нет!")
    
@dp.message_handler(lambda message: message.text == "🌟Мои игры")
async def view_games(message: types.Message):
    await message.answer("Список ваших игр пуст")



@dp.callback_query_handler(lambda call: call.data.startswith("date_"))
async def select_date(call: types.CallbackQuery):
    


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)