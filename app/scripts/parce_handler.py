from datetime import datetime, timedelta  # добавляем timedelta в импорт
from app.scripts import parce


async def get_moon_phase_info(date):
    if len(date.split('-')) == 3:
        year, month, day = date.split('-')
        hour, minute, second = '00', '00', '00'  # Устанавливаем время по умолчанию
        moon_phase, visibility, age, distance, _, moon_image_url = parce.get_moon_phases(day, month, year, hour, minute, second)
        return moon_phase, visibility, age, distance, moon_image_url
    else:
        year, month, day, hour, minute, second = date.split('-')
        moon_phase, visibility, age, distance, _, moon_image_url = parce.get_moon_phases(day, month, year, hour, minute, second)
        return moon_phase, visibility, age, distance, moon_image_url


async def generate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=1)
    while start <= end:
        year, month, day = start.year, start.month, start.day
        hour, minute, second = start.hour, start.minute, start.second
        yield year, month, day, hour, minute, second
        start += step