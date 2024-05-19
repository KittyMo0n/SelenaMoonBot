from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.requests import get_users

admin = Router()
A = 1410612869


class Newsletter(StatesGroup):
    message = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [A]


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer('Возможные команды: /newsletter\n'
                         '/some_func')


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям')


@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.copy_to(chat_id=user.tg_id)
        except Exception as e:
            print(f"Failed to send message to user {user.tg_id}: {e}")
    await message.answer('Рассылка успешно завершена.')
    await state.clear()