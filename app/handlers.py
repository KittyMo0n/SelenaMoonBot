from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from app.database.requests import set_user
from app.scripts.parce_handler import get_moon_phase_info

from datetime import datetime

router = Router()


async def get_moon_data_and_respond(message: Message, date_text: str):
    try:
        moon_phase, visibility, age, distance, moon_image_url = await get_moon_phase_info(date_text)
        response_message = f"Данные получены: {date_text.split('-')}\n"
        if moon_phase:
            response_message += f"Тип фазы Луны: {moon_phase}\n"
        if visibility:
            response_message += f"Видимость: {visibility}\n"
        if age:
            response_message += f"Возраст: {age}\n"
        if distance:
            response_message += f"Расстояние: {distance}\n"
        if moon_image_url:
            await message.answer_photo(moon_image_url, caption=response_message, parse_mode=ParseMode.HTML)
        else:
            await message.answer(response_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@router.message(CommandStart())
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    await set_user(tg_id=tg_id, username=message.from_user.full_name)
    user_name = message.from_user.full_name
    # I need name for bot
    greeting = (
        f"Приветствую, <b>{user_name}</b>!\n\n"
        "Я <b>Selena Moon bot</b>\n"
        "Я получаю данные о Луне с astrolab.ru, и всегда готов ими поделиться.\n\n"
        "Ты можешь легко получить необходимые данные, отправив мне сообщение в формате: <b>YYYY-MM-DD</b> (к примеру, <b>2024-04-25</b>).\n\n"
        "Если Вам нужна точность 'до секунды', введите дату в формате: <b>YYYY-MM-DD-HH-MM-SS</b> (к примеру, <b>2024-04-25-01-01-01</b>).\n\n"
        "Или просто нажми <b>'moon_now'</b> для получения актуальной информации о Луне.\n\n"
    )
    await message.answer_photo(photo=types.FSInputFile("./start_banner.jpg"), caption=greeting, parse_mode=ParseMode.HTML)



@router.message(Command('moon_now'))
async def handle_get_info_now(message: Message):
    nowdate = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    await get_moon_data_and_respond(message, nowdate)


DATE_REGEX_ = r'\d{4}-\d{2}-\d{2}'
@router.message(F.text.regexp(DATE_REGEX_))
async def handle_date_message(message: Message):
    await get_moon_data_and_respond(message, message.text)


DATE_REGEX = r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}'
@router.message(F.text.regexp(DATE_REGEX))
async def handle_date_message(message: Message):
    await get_moon_data_and_respond(message, message.text)