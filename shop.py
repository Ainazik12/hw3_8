from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests, sqlite3, logging


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())  
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect("shop.db")
cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS laptop (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
''')
connect.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        laptop TEXT NOT NULL,
        total_price REAL NOT NULL
    )
''')
connect.commit()

class OrderState(StatesGroup):
    name = State()
    address = State()
    phone = State()
    laptop = State() 
    confirm_order = State()
    
    
@dp.message_handler(commands='order')
async def start_order(message: types.Message, state: FSMContext):
    cursor.execute("SELECT * FROM laptop")
    items = cursor.fetchall()
    if items:
        await message.answer("Введите ваше имя:")
        await OrderState.name.set()
    else:
        await message.answer("Ваша корзина пуста. Добавьте товары в корзину с помощью команды /buy.")

@dp.message_handler(state=OrderState.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введите ваш адрес доставки:")
    await OrderState.next()

@dp.message_handler(state=OrderState.address)
async def address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer("Введите ваш номер телефона:")
    await OrderState.next()

@dp.message_handler(state=OrderState.phone)
async def phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    
    cursor.execute("SELECT * FROM laptop")
    items = cursor.fetchall()
    if not items:
        await message.answer("Ваша корзина пуста. Добавьте товары в корзину с помощью команды /buy.")
        await state.finish()  
        return
    
    total_price = sum(item[2] for item in items)
    cursor.execute("SELECT * FROM laptop ORDER BY id DESC LIMIT 1")
    last_item = cursor.fetchone()
    if last_item:
        laptop_name = last_item[1]
    else:
        laptop_name = "Товар не указан"
    
    await state.update_data(total_price=total_price)
    
    order_info = f"Имя: {data['name']}\n" \
                 f"Адрес: {data['address']}\n" \
                 f"Телефон: {data['phone']}\n" \
                 f"Товар: {laptop_name}\n" \
                 f"Итоговая стоимость: {total_price} cом."
 
    await message.answer("Пожалуйста, подтвердите ваш заказ:\n" + order_info)
    await OrderState.laptop.set()  
    
@dp.message_handler(state=OrderState.laptop)
async def laptop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['laptop'] = message.text
    
    async with state.proxy() as data:
        laptop = data['laptop']
        name = data['name']
        address = data['address']
        phone = data['phone']
        total_price = data['total_price']
          
    cursor.execute('''
        INSERT INTO orders (name, address, phone, laptop, total_price)
        VALUES (?, ?, ?, ?, ?)''', (name, address, phone, laptop, total_price))
    connect.commit()

    await state.finish()
    await message.answer("Заказ успешно оформлен!\n")

class ResumeState(StatesGroup):
    title = State()
    price = State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Здравствуйте, вас приветствует магазин ноутбуков Barmak.Store. Чтобы сделать покупки, нажмите /help")

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply("Доступные команды:\n"
                        "/start - начать чат\n"
                        "/info - Информация о магазине ноутбуков https://www.barmak.store\n"
                        "/laptops - Отправляет ноутбуки в наличии\n"
                        "/help - вывести список доступных команд\n"
                        "/buy - Купить ноутбук \n"
                        "/order - заказать ноутбук \n"
                        "/bucket - посмотреть корзину \n "
                        "/remove - для удаления товара с корзины  ")
    

@dp.message_handler(commands='laptops')
async def send_laptops(message: types.Message):
    await message.answer("Отправляю ноутбуки в наличии....")
    url = f'https://www.barmak.store/category/Laptop/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_laptops = soup.find_all('div', class_='tp-product-tag-2')
    all_prices = soup.find_all('span', class_='tp-product-price-2 new-price')

    laptops_info = ""
    for name, price in zip(all_laptops, all_prices):
        laptops_info += f"{name.text} - {price.text}\n"

    await message.answer(laptops_info.strip())
    await message.answer("Вот все ноутбуки в наличии")


@dp.message_handler(commands='bucket')
async def bucket(message: types.Message):
    cursor.execute("SELECT * FROM laptop")
    items = cursor.fetchall()
    if items:
        await message.answer("Ваша корзина:")
        for item in items:
            await message.answer(f"Товар: {item[1]}, Цена: {item[2]} сом")
    else:
        await message.answer("Ваша корзина пуста.")

@dp.message_handler(commands='buy')
async def order_for(message: types.Message):
    await message.answer("Введите название товара:")
    await ResumeState.title.set()

@dp.message_handler(state=ResumeState.title)
async def get_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите цену товара:")
    await ResumeState.next()

@dp.message_handler(state=ResumeState.price)
async def get_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    async with state.proxy() as data:
        title = data['title']
        price = data['price']

    cursor.execute('''
        INSERT INTO laptop (title, price)
        VALUES (?, ?)''', (title, price))
    connect.commit()

    await state.finish()
    await message.answer("Товар добавлен в корзину. Можете посмотреть /bucket")
    

class RemoveState(StatesGroup):
    waiting_for_item = State()

remove_button = KeyboardButton('/remove')
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(remove_button)

@dp.message_handler(commands='remove')
async def remove_start(message: types.Message):
    cursor.execute("SELECT * FROM laptop")
    items = cursor.fetchall()

    if items:
        await message.answer("Выберите номер товара, который хотите удалить из корзины:")
        await message.answer("\n".join([f"{idx}. {item[1]} - {item[2]} сом" for idx, item in enumerate(items, start=1)]), reply_markup=main_menu_keyboard)
        await RemoveState.waiting_for_item.set()
    else:
        await message.answer("Ваша корзина пуста.")

@dp.message_handler(state=RemoveState.waiting_for_item)
async def remove_item(message: types.Message, state: FSMContext):
    try:
        item_number = int(message.text)
        cursor.execute("SELECT * FROM laptop")
        items = cursor.fetchall()



        if 1 <= item_number <= len(items):
            item_to_remove = items[item_number - 1]
            cursor.execute("DELETE FROM laptop WHERE id=?", (item_to_remove[0],))
            connect.commit()
            await message.answer(f"Товар '{item_to_remove[1]}' удален из корзины.")
        else:
            await message.answer("Некорректный номер товара.")
    except ValueError:
        await message.answer("Введите корректный номер товара (целое число).")

    await state.finish()
    await message.answer("Чем еще могу помочь?", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text.lower() in ['где мой заказ?', 'как сделать заказ?', 'как оплатить?'])
async def faq_handler(message: types.Message):      
    if message.text.lower() == 'где мой заказ?':
        await message.answer("Ваш заказ в процессе обработки. Ожидайте уведомлений о статусе.")
    elif message.text.lower() == 'как сделать заказ?':
        await message.answer("Чтобы сделать заказ, введите команду /order и следуйте инструкциям.")
    elif message.text.lower() == 'как оплатить?':
        await message.answer("Вы можете оплатить ваш заказ наличными или банковской картой при получении товара.")
    else:
        await message.answer("Сожалеем, но не можем ответить на ваш вопрос. Обратитесь к нашему менеджеру для получения дополнительной информации.")

async def send_order_status(user_id: int, status: str):
    await bot.send_message(user_id, f"Статус вашего заказа: {status}")

async def send_special_offers():
    special_offers = [
        "Только сегодня! Скидка 20% на все ноутбуки!",
        "При покупке двух ноутбуков - третий в подарок!",
        "Успейте купить ноутбук по выгодной цене в нашем магазине!"
    ]
    all_users = await get_all_users() 
    for user_id in all_users:
        for offer in special_offers:
            await bot.send_message(user_id, offer)
          

async def get_all_users():
    return [5875325460]  

async def on_startup(dp):
    await send_special_offers()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)