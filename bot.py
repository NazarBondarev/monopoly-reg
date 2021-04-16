from aiogram import executor, exceptions, Dispatcher, Bot, types
import asyncio
from config import API_TOKEN
from keyboards import general_menu, Keyboards
from pprint import pprint
from dbreqs import Database
from datetime import datetime

bot = Bot(API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
dates = Database().get_tables()



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
    keyb,dates = Keyboards().get_dates_keyb()

    if keyb:
        await message.answer("🗒<b>Список доступных игр</b>\n\n💡<em>Число в квадратных скобках обозначает количество забронированных мест</em>", reply_markup=keyb)
    else:
        await message.answer("На данный момент доступных игр нет!")
    
@dp.message_handler(lambda message: message.text == "🌟Мои игры")
async def view_games(message: types.Message):
    history = Keyboards().get_user_games(message.from_user.id)
    if history:
        await message.answer("📒История ваших игр\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             "<em>🔄 - означает что игра еще не была начата\завершена\n"
                             "✅ - означает что игра была завершена</em>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖", reply_markup=history)



@dp.callback_query_handler(lambda call: call.data[0] not in ("✅", "🔄"))
async def select_date(call: types.CallbackQuery):
    dates = Database().get_tables()

    if call.data in dates:
        status = Database().get_users(call.from_user.id, call.data[0:-4])
        if status and call.data[-3:] != "[10]":
            Database().add_new_user(call.from_user.id, call.from_user.first_name, str(datetime.now()), call.data[0:-4])
            Database().add_to_history(call.from_user.id, call.from_user.first_name, str(datetime.now()), call.data[0:-4])
            keyb,dates = Keyboards().get_dates_keyb()
            users = Database().get_usernames(call.data[0:-4])
            temp = []
            i = 0
            for item in users:
                i+=1
                temp.append(f"{i}. {item}")
            users = "\n".join(temp)
            await call.message.edit_text(text=f"✅Вы успешно записались на игру\n"
                                                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>{call.data[0:-4]}</b>!\nНе опаздывайте😉\n"
                                                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n <b>Список игроков:</b>\n{users}")
        elif call.data[-3:] == "[10]":
            await call.message.answer("🙅К сожалению все места на эту игру заняты")
        elif not status:
            await call.answer("❌Вы уже записаны на эту игру")
    else:
        print(False)
    
@dp.callback_query_handler(lambda call: call.data[0] in ("✅", "🔄"))
async def view_user_game(call: types.CallbackQuery):
    action = call.data[0]
    print(action)
    usernames = Database().get_usernames(call.data.replace(action, ''))
    temp = []
    i = 0
    for item in usernames:
        i+=1
        temp.append(f"{i}. {item}")
    users = "\n".join(temp)

    await call.message.answer(f"<b>{call.data}</b>\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"{users}\n"
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)