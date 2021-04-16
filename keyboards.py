from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from dbreqs import Database



general_menu = ReplyKeyboardMarkup(keyboard=[
    [
     KeyboardButton(text="📆Даты игр")
    ],
    [
        KeyboardButton(text="💬Правила игры")
    ],
    [
    KeyboardButton(text="🌟Мои игры")
    ]
], resize_keyboard=True)




class Keyboards:
    def __init__(self, db=None):
        self.db = Database()
    def get_dates_keyb(self):
        dates = self.db.get_tables()
        if dates:
            keyb = InlineKeyboardMarkup(row_width=2)
            i = 0
            for item in dates:
                i+=1
                keyb.add(InlineKeyboardButton(text=item, callback_data=f"date_{i}"))
            
            return keyb
        
        else:
            return False
