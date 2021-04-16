from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from dbreqs import Database
from datetime import datetime
from dateparser import parse


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
            for item in dates:
                
                t = parse(item[0:-4], settings={'DATE_ORDER': 'DMY'})
                if datetime.now() < t:
                    keyb.add(InlineKeyboardButton(text=item, callback_data=f"{item}"))
            
            return keyb, dates
        
        else:
            return False

    def get_user_games(self, userid):
        dates = self.db.get_user_history(userid)
        print(dates)
        if dates:
            keyb = InlineKeyboardMarkup(row_width=2)
            i = 0
            for item in dates:
                i+=1
                t = parse(item, settings={'DATE_ORDER': 'DMY'})
                print(datetime.now() < t)
                if datetime.now() > t:
                    keyb.add(InlineKeyboardButton(text=f"✅{item}", callback_data=f"✅{item}"))
                elif datetime.now() < t:
                    keyb.add(InlineKeyboardButton(text=f"🔄{item}", callback_data=f"🔄{item}"))
            
            return keyb
        else:
            return False
            