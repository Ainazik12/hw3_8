# from aiogram import Bot, Dispatcher, types, executor
# from config import token
# import logging

# bot = Bot(token=token)
# dp = Dispatcher(bot)
# logging.basicConfig(level=logging.INFO)

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Привет, я тг бот от компании BMW", reply_markup=start_keyboard)

# @dp.message_handler(commands=['help'])
# async def help(message: types.Message):
#     print(message)
#     await message.answer(f"Привет, {message.from_user.full_name}! Чем могу вам помочь?")

# start_buttons = [
#     types.KeyboardButton("Модели автомобилей"),
#     types.KeyboardButton("Цены"),
#     types.KeyboardButton("Характеристики"),
#     types.KeyboardButton("Специальные предложения")
# ]
# start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

# model_button = [
#     types.KeyboardButton('E30 BMW'),
#     types.KeyboardButton('BMW M5 - e60'),
#     types.KeyboardButton('BMW x6m'),
#     types.KeyboardButton("Назад")
# ]

# model_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*model_button)

# @dp.message_handler(text="Модели автомобилей")
# async def num_3(message: types.Message):
#     await message.answer("Вот модели машин, которые у нас есть", reply_markup=model_keyboard)

# @dp.message_handler(text="E30 BMW")
# async def num_5(message: types.Message):
#     await message.answer_photo('https://gas-kvas.com/uploads/posts/2023-02/1675449783_gas-kvas-com-p-fonovie-risunki-dlya-rabochego-stola-bmv-40.jpg')
#     await message.answer("Это модель E30 BMW")

# @dp.message_handler(text="BMW M5 - e60")
# async def num_6(message: types.Message):
#     await message.answer_photo('https://www.auto-data.net/images/f33/BMW-M5-E60_1.jpg')
#     await message.answer('Это модель M5 - e60')

# @dp.message_handler(text="BMW x6m")
# async def num_7(message: types.Message):
#     await message.answer_photo('https://avatars.mds.yandex.net/i?id=1b72674cfb6301bef60408f4d920bf705796c7da-10807932-images-thumbs&n=13')
#     await message.answer('Это модель BMW x6m')

# num1_button = [
#     types.KeyboardButton('Цена E30 BMW'),
#     types.KeyboardButton('Цена BMW M5 - e60'),
#     types.KeyboardButton('Цена BMW x6m'),
#     types.KeyboardButton("Назад")
# ]

# num00_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num1_button)

# @dp.message_handler(text="Цены")
# async def num_9(message: types.Message):
#     await message.answer("Вот модели машин и их цены", reply_markup=num00_keyboard)

# @dp.message_handler(text="Цена E30 BMW")
# async def num_01(message: types.Message):
#     await message.answer("Эта машинка E30 BMW стоит в 150000 сомов")

# @dp.message_handler(text="Цена BMW M5 - e60")
# async def num_02(message: types.Message):
#     await message.answer("Эта машинка BMW M5 - e60 стоит 1.000.000 сомов")

# @dp.message_handler(text="Цена BMW x6m")
# async def num_03(message: types.Message):
#     await message.answer("Эта машинка BMW x6m стоит 2.500.000 сомов")

# @dp.message_handler(text='Назад')
# async def rollback(message: types.Message):
#     await start(message)

# num01_button = [
#     types.KeyboardButton('Характеристики E30 BMW'),
#     types.KeyboardButton('Характеристики BMW M5 - e60'),
#     types.KeyboardButton('Характеристики BMW x6m'),
#     types.KeyboardButton("Назад")
# ]

# num2_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num01_button)

# @dp.message_handler(text="Характеристики")
# async def num_9(message: types.Message):
#     await message.answer("Характеристики машин", reply_markup=num2_keyboard)

# @dp.message_handler(text='Назад')
# async def rollback(message: types.Message):
#     await start(message)
    


# @dp.message_handler(text="Характеристики E30 BMW")
# async def num_01(message: types.Message):
#     await message.answer("""ТРЕТЬЕ ПОКОЛЕНИЕ BMW 5 СЕРИИ.
#     BMW M Sedan (E30) вид спереди с поворотом в три четверти (BMW E30)
#     BMW 5-й серии (E30), представленный публике в январе 1988 года, значительно крупнее и шире своего предшественника: улучшенная 
#     аэродинамика с коэффициентом аэродинамического сопротивления 0,30 гарантировала, что все бензиновые модели BMW 5-й серии могли развивать 
#     скорость более 200 км/ч. Благодаря длинной колесной базе и почти оптимальному распределению веса 50:50 на переднюю и заднюю оси автомобили 
#     впечатляли своими спортивными ходовыми характеристиками и динамикой — от BMW 518i с четырьмя цилиндрами до BMW M5 мощностью 315 л. с., 
#     который также стал доступным в год запуска. 

#     В 1991 году BMW 5-й серии Touring удивил не меньше: впервые в среднеразмерном представительском сегменте появился универсал от BMW.
#      Его уникальная черта — заднее стекло, которое открывалось независимо от задней двери. В том же году двери получили защиту от бокового
#       удара — автомобиль стал безопаснее.

#     В 1992 году на рынок вышел первый BMW 5-й серии с полным приводом — BMW 525iX. Среди нововведений — оснащение моделей BMW 5-й серии
#      восьмицилиндровыми двигателями. В BMW 530i и BMW 540i эти двигатели отличались особенно плавным ходом. BMW M5 сохранил рядный
#       шестицилиндровый двигатель, однако его рабочий объем увеличился до 3,8 л, что привело к повышению мощности до 340 л. с. Более мощный
#        BMW M5 стал также доступен в версии Touring. 

#     Седан перестали производить в 1995 году, а продажи BMW 5-й серии Touring продолжались до 1996 года. Всего владельцам передали 1,3 миллиона автомобилей.

#     Период производства: 1988 – 1996 гг. Двигатели: 1.8 – 4.0 л (83 – 250 кВт, 113 – 340 л. с.), 4-, 6- & 8-цилиндровый Длина/ширина/высота: 4,720/1,751/1,412 – 1,421 мм""")
    
# @dp.message_handler(text="Характеристики BMW M5 - e60")
# async def num_02(message: types.Message):
#     await message.answer("""BMW M5 - e60 имеет следующие характеристики:

#     Марка  BMW
#     Модель  M5
#     Поколения  M5 (E60)
#     Модификация (двигатель)  5.0 V10 (507 лс) SMG
#     Начало выпуска  2005 г
#     Оконч. выпуска  Марш, 2007 г
#     Архитектура силового агрегата  Двигатель внутреннего сгорания
#     Тип кузова  Седан
#     Количество мест  5
#     Количество дверей  4
#     Эксплуатационные характеристики
#     Расход топлива в городе  22.7 л/100 км
#     10.36 US mpg
#     12.44 UK mpg
#     4.41 км/л
#     Расход топлива на шоссе  10.2 л/100 км

#     2005 BMW M5 (E60) 5.0 V10 (507 лс) SMG | Технические характеристики, расход топлива , Габариты: https://www.auto-data.net/ru/bmw-m5-e60-5.0-v10-507hp-smg-9871
#     Страна производства: Германия.""")

# @dp.message_handler(text="Характеристики BMW x6m")
# async def num_03(message: types.Message):
#     await message.answer("""BMW X6 M COMPETITION И X6 M60i xDRIVE.
#     BMW X6 M Competition:
#     Расход топлива в смешанном цикле WLTP, л/100 км: 12.9–12.6
#     Выбросы CO2 в смешанном цикле WLTP, г/км: 293–284

#     BMW X6 M60i xDrive:
#     Расход топлива в смешанном цикле WLTP, л/100 км: 12.3–11.4
#     Выбросы CO2 в смешанном цикле WLTP, г/км: 279–258""")

# @dp.message_handler(text='Назад')
# async def rollback(message: types.Message):
#     await start(message)

# num_button = [
#     types.KeyboardButton('Гарантия 1+1'),
#     types.KeyboardButton('Тест драйв'),  
#     types.KeyboardButton("Назад")
# ]

# num_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*num_button)

# @dp.message_handler(text="Специальные предложения")
# async def num(message: types.Message):
#     await message.answer("Вот какие есть специальные предложения", reply_markup=num_keyboard)

# @dp.message_handler(text="Гарантия 1+1")
# async def num(message: types.Message):
#     await message.answer("Мы дадим гарантию на 3 года")

# @dp.message_handler(text="Тест драйв")
# async def num(message: types.Message):
#     await message.answer("Хотите пройти тест-драйв? Напишите нам, и мы устроим незабываемый опыт вождения!")
    


# @dp.message_handler(text='Назад')
# async def rollback(message: types.Message):
#     await start(message)

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)