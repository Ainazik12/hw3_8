# from aiogram import Bot, Dispatcher, types, executor
# from bs4 import BeautifulSoup
# import requests
# from config import token  


# bot = Bot(token=token)
# dp = Dispatcher(bot)



# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Привет! Я бот для новастей /news.")


# @dp.message_handler(commands=['news'])

# async def news(message: types.Message):

#     for page in range(1, 11):
#         url = f'https://24.kg/page_{page}'
#         try:
#             response = requests.get(url=url)
#             response.raise_for_status()  
#             soup = BeautifulSoup(response.text, 'lxml')
#             all_news = soup.find_all('div', class_='title')        
#             for news in all_news:
#                 news_text = news.text
#                 while len(news_text) > 0:
#                     await message.answer(news_text[:4096])
#                     news_text = news_text[4096:]
#         except Exception as e:
#             await message.answer(f"Произошла ошибка")


# executor.start_polling(dp)