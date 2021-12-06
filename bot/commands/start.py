from os import environ
from hashlib import md5

from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton)

from objects import globals
from objects.globals import dp, config
from db_models.AuthUser import AuthUser
from keyboards.keyboards import MENU_BUTTONS

@dp.message_handler(commands="start")
async def start(message:Message):

    globals.state_type = "" #Reset state type

    user_data = await AuthUser.objects.filter(user_id=message.from_user.id).all()

    if not user_data:

        username = message.from_user.username if message.from_user.username is not None else "None"
        last_name = message.from_user.last_name if message.from_user.last_name is not None else "None"
        first_name = message.from_user.first_name if message.from_user.first_name is not None else "None"

        await AuthUser.objects.create(password=(md5(str(message.from_user.id).encode("utf-8")).hexdigest())[:10],
                                      user_id=message.from_user.id, username=username,
                                      last_name=last_name, first_name=first_name)

    buttons = list(zip([KeyboardButton(MENU_BUTTONS[k]) for k in range(len(MENU_BUTTONS)) if k % 2 == 0], 
                       [KeyboardButton(MENU_BUTTONS[k]) for k in range(len(MENU_BUTTONS)) if k % 2 != 0]))

    if message.from_user.id == int(eval(environ.get("ADMIN_ID"))):
        buttons.append([KeyboardButton("📊Статистика")])

    buttons = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)

    await message.answer(text=f"🤖Приветствую! Я бот.", reply_markup=buttons)