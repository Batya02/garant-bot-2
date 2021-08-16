from objects.globals import dp, config
from db_models.AuthUser import AuthUser

from hashlib import md5

from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton)

from objects import globals

from keyboards.keyboards import MENU_BUTTONS

@dp.message_handler(commands="start")
async def start(message: Message):
    globals.state_type = "" #Reset state type

    user_data = await AuthUser.objects.filter(user_id=message.from_user.id).all()

    if len(user_data) == 0:

        await AuthUser.objects.create(
            password   = (md5(str(message.from_user.id).encode("utf-8")).hexdigest())[:10],
            user_id    = message.from_user.id,
            username   = message.from_user.username,
            last_name  = message.from_user.last_name,
            first_name = message.from_user.first_name
            ) 

    buttons_array = []
    buttons_array.append([KeyboardButton(MENU_BUTTONS[k]) for k in range(len(MENU_BUTTONS)) if k % 2 == 0])
    buttons_array.append([KeyboardButton(MENU_BUTTONS[k]) for k in range(len(MENU_BUTTONS)) if k % 2 != 0])

    if message.from_user.id == int(config["admin_chat_id"]):
        buttons_array.append([KeyboardButton("📊Статистика")])

    buttons = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons_array)
    
    await message.answer(text=f"🤖Приветствую! Я бот.", reply_markup=buttons)