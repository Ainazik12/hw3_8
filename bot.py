from aiogram import Bot, Dispatcher, types, executor
from config import token
import random

bot = Bot(token = token)
dp = Dispatcher(bot)
num = ["1", "2", "3"]
chaice_num = random.choice(num)
print(chaice_num)


@dp.message_handler(commands ='start')
async def random(message:types.Message):
    await message.answer('Я загадал число от 1 до 3 угадайте')
    
@dp.message_handler(text ='1')
async def choice_one(message:types.Message):
    if chaice_num == "1":
        await message.reply('Вы угадали число')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif chaice_num != "1":
        await message.reply('Вы не угадали число')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
        
@dp.message_handler(text ='2')
async def choice_one(message:types.Message):
    if chaice_num == "2":
        await message.reply('Вы угадали число')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif chaice_num != "2":
        await message.reply('Вы не угадали число')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
          
@dp.message_handler(text ='3')
async def choice_one(message:types.Message):
    if chaice_num == "3":
        await message.reply('Вы угадали число')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif chaice_num != "3":
        await message.reply('Вы не угадали число')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
           
executor.start_polling(dp) 