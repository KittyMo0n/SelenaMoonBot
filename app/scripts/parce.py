import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime, timedelta

def parse_moon_info(container):
    phase = re.search(r'<b>(.*?)<br>', container)
    if phase:
        phase = phase.group(1)
    else:
        phase = None

    age_visibility_distance = re.findall(r'Видимость.*?(\d+\s*%).*?Возраст.*?(\d+\s*д\s*\d+\s*ч\s*\d+\s*м).*?Расстояние.*?(\d+\s*км)', container, re.DOTALL)
    if age_visibility_distance:
        visibility, age, distance = age_visibility_distance[0]
        return phase, visibility, age, distance
    else:
        return None, None, None, None

def get_moon_image_url(html_text, url):
    soup = BeautifulSoup(html_text, 'html.parser')
    container = soup.find('div', class_='top-page-text')
    if container:
        image_tag = container.find('img')
        if image_tag:
            image_src = image_tag['src']
            full_image_url = urljoin(url, image_src)
            return full_image_url
        else:
            print('Изображение не найдено.')
            return None
    else:
        print('Контейнер с информацией о фазах Луны не найден.')
        return None

def get_moon_phases(day, month, year, hour, minute, second):
    url = 'https://www.astronews.ru/cgi-bin/moonphases.cgi'
    data = {
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
        'minute': minute,
        'second': second
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.find('div', class_='top-page-text')
        if container:
            text = container.get_text()
            moon_phase, visibility, age, distance = parse_moon_info(text)
            moon_image_url = get_moon_image_url(response.text, url)
            return moon_phase, visibility, age, distance, text, moon_image_url
        else:
            print('Контейнер с информацией о фазах Луны не найден.')
            return None, None, None, None, None, None
    else:
        print('Ошибка при получении данных о фазах Луны.')
        return None, None, None, None, None, None

def generate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    step = timedelta(days=1)
    while start <= end:
        yield start.strftime("%d"), start.strftime("%m"), start.strftime("%Y"), start.strftime("%H"), start.strftime("%M"), start.strftime("%S")
        start += step

def main():
    start_date = input("Введите начальную дату в формате YYYY-MM-DD: ")
    end_date = input("Введите конечную дату в формате YYYY-MM-DD: ")

    for day, month, year, hour, minute, second in generate_date_range(start_date, end_date):
        print(f"Информация о фазах Луны на {day}.{month}.{year} {hour}:{minute}:{second}")
        moon_phase, visibility, age, distance, moon_phases_text, moon_image_url = get_moon_phases(day, month, year, hour, minute, second)
        if moon_phase:
            print('Тип фазы Луны:', moon_phase)
        if visibility:
            print('Видимость:', visibility)
        if age:
            print('Возраст:', age)
        if distance:
            print('Расстояние:', distance)

        if moon_image_url:
            print('Полный URL изображения фазы Луны:')
            print(moon_image_url)
        print("")

if __name__ == "__main__":
    main()