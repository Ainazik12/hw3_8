from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, sqlite3
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token = token)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect("bank_system.db", check_same_thread=False)

cursor= connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(115),
    lastname VARCHAR(115),
    phone_number VARCHAR(150)
    );""")

connect.commit()

cursor.execute(""" CREATE TABLE IF NOT EXISTS user_info(
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(115),
    first_name VARCHAR(150),
    last_name VARCHAR(115),
    balance INTEGER DEFAULT 0,
    date_register DATETIME
    );""")

cursor.execute("""CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER,
    recipient_id INTEGER,
    amount INTEGER,
    FOREIGN KEY (sender_id) REFERENCES users (user_id),
    FOREIGN KEY (recipient_id) REFERENCES users (user_id)
    );""")

async def transfers_funds(sender_id, recipient_id, amount):
    cursor.execute("UPDATE user_info SET balance = balance - ? WHERE user_id = ?",(amount, sender_id ))
    cursor.execute("UPDATE user_info SET balance = balance + ? WHERE user_id = ?",(amount, recipient_id ))
    cursor.execute("INSERT INTO transfers (sender_id, recipient_id, amount) VALUES(?, ?, ?)",
                   (sender_id, recipient_id, amount))
    connect.commit()
    
def get_balance(user_id):
    cursor.execute(f"SELECT balance FROM user_info WHERE user_id = {user_id}")
    connect.commit()
    result = cursor.fetchone()
    return result[0] if result is None else None

@dp.message_handler(commands='balance')
async def cmd_balance(message:types.Message):
    user_id = message.from_user.id 
    balance=  get_balance(user_id)
    if balance is not None:
        await message.answer(f"ваш текущий баланс: {balance} сомов")
    else:
        await message.answer(f"У вас нет счета. Для создания выбырите команда /start ")
        
    
class OrderPersonState(StatesGroup):
    lastname = State()    
    username = State()    
    phone_number = State()
    
buttons = [
    types.KeyboardButton("справичник"),
    types.KeyboardButton("Регистрация"),
    types.KeyboardButton("/balance"),
    types.KeyboardButton("/transfer"), 
    types.KeyboardButton("/deposit")

]    
key_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
@dp.message_handler(commands='start')
async def start(message: types.Message):
    
    cursor=connect.cursor()
    cursor.execute(f"SELECT user_id FROM user_info WHERE user_id = {message.from_user.id};")
    res = cursor.fetchall()
    if not res:
        cursor.execute(f"""INSERT INTO user_info (user_id, user_name, first_name, last_name,  date_register) 
        VALUES ('{message.from_user.id}',  
               '{message.from_user.username}',
               '{message.from_user.first_name}',
               '{message.from_user.last_name}',
               '{datetime.now()}'
);""")
        connect.commit()

    await message.answer("""Здравствуйте , вас приветсвует компания 'Cash_bank'благодарим вас что выбрали именно нашу компанию.Пожалуйста чтобы в дальшем продолжить сотредничествa нажмите кнопку РЕГИСТРАЦИЯ  |
                                                                                              V
                          """, reply_markup = key_buttons)
    await message.answer(f"Ваш номер счет: {message.from_user.id}\nНикнейм: {message.from_user.username}")
    
    
@dp.message_handler(text= "справичник")
async def directory(message:types.Message):
    await message.answer(f"")

@dp.message_handler(text= "справичник")
async def directory(message:types.Message):
    await message.answer(f" /balance - чтобы посмотреть ваш баланс /n /transfer -чтобы сделать перевод  /deposit - пополнить баланс   ")

class DepositState(StatesGroup):
    amount = State()
    
@dp.message_handler(commands='deposit')
async def cmd_deposit(message: types.Message):
    await message.answer("Введите сумму для пополнения баланса:")
    await DepositState.amount.set()
    
@dp.message_handler(state=DepositState.amount)
async def deposit_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM user_info WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")

        cursor.execute('UPDATE user_info SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        connect.commit()

        await message.answer(f"Баланс успешно пополнен на {amount}")

    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        await state.finish()


@dp.message_handler(text='Регистрация')
async def registration(message: types.Message):
    await message.answer("Для регистратция нам нужны ваши данные: ")
    await message.answer("Введите вашу фамилию:")
    await OrderPersonState.lastname.set()
    
@dp.message_handler(state = OrderPersonState.lastname)
async def first_n(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] =message.text
        await message.answer("Введите ваше имя: ")
        await OrderPersonState.next()
        
        
@dp.message_handler(state = OrderPersonState.username)
async def later(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Введите ваш номер :")
    await OrderPersonState.next()      
    
@dp.message_handler(state = OrderPersonState.phone_number)
async def later(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
        
    username = data['username']
    lastname = data['lastname']
    phone_number = data['phone_number']
    
    await message.answer("Вы теперь в базе, \n чтобы пополнить /deposit")
    await state.finish()

    cursor.execute(""" INSERT INTO users (username, lastname, phone_number)
                   VALUES (?,?,?) """, (username, lastname, phone_number ))
    connect.commit()


class TransferState(StatesGroup):
    amount = State()
    recipient_balance = State()

@dp.message_handler(commands=['transfer'])
async def transfer_command(message: types.Message):
    await message.answer('Введите сумму перевода:')
    await TransferState.amount.set()

@dp.message_handler(state=TransferState.amount)
async def process_amount(message: types.Message, state: FSMContext):
    amount = float(message.text)
    await state.update_data(amount=amount)
    await message.answer('Введите ID пользователя или номер счета получателя:')
    await TransferState.recipient_balance.set()

@dp.message_handler(state=TransferState.recipient_balance)
async def process_recipient_balance(message: types.Message, state: FSMContext):
    recipient_balance_data = int(message.text)
    data = await state.get_data()
    amount = data.get('amount')
    result = process_transfer(message.from_user.id, recipient_balance_data, amount)

    if result:
        await message.answer('Перевод выполнен успешно!')
        await message.answer(f'Сумма перевода: {amount} руб.')
        await message.answer(f'Получатель: {recipient_balance_data}')
    else:
        await message.answer('Ошибка при выполнении перевода. Пожалуйста, проверьте данные получателя.')

    await state.finish()

def process_transfer(sender_id, recipient_balance_data, amount):
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()

    try:
        conn.execute('BEGIN TRANSACTION')

        cursor.execute('SELECT balance FROM user_info WHERE user_id = ?',
        (sender_id,))
        sender_balance = cursor.fetchone()[0]

        if sender_balance >= amount:
            cursor.execute('UPDATE user_info SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))

            cursor.execute('SELECT user_id FROM user_info WHERE user_id = ?', (recipient_balance_data,))
            recipient_exists = cursor.fetchone()

            if recipient_exists:
                cursor.execute('UPDATE user_info SET balance = balance + ? WHERE user_id = ?', (amount, recipient_balance_data))

                
                conn.execute('COMMIT')

                return True
            else:
                return False  
        else:
            return False  

    except Exception as e:
        conn.execute('ROLLBACK')
        print(f'Error: {e}')
        return False

    finally:
        
        conn.close()

@dp.message_handler()
async def mistake(message: types.Message):
    await message.answer("Я не понял ваш запрос, введите команду /start")


executor.start_polling(dp)