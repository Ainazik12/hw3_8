import schedule
import asyncio
from aiogram import Dispatcher, Bot, executor, types
from bs4 import BeautifulSoup
import logging
import requests
from config import token
from datetime import datetime


bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


async def send_currency_rates(message):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    currencies = soup.find_all('td', class_='exrate')

    chat_id = message.chat.id
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    await bot.send_message(chat_id=chat_id, text=f"Приветствую! Я бот, который поможет вам узнать текущие курсы валют.\n"
                                                  f"Вот актуальные курсы на {current_time}:\n"
                                                  f"Курс USD: {currencies[0].text}\n"
                                                  f"Курс EUR: {currencies[2].text}\n"
                                                  f"Курс RUB: {currencies[4].text}\n"
                                                  f"Курс KZT: {currencies[6].text}")


async def send_currency_rates_periodically(message):
    while True:
        await send_currency_rates(message)
        await asyncio.sleep(60)  


async def on_startup(dispatcher):
    pass


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await send_currency_rates(message)
    asyncio.create_task(send_currency_rates_periodically(message))




executor.start_polling(dp, on_startup=on_startup)