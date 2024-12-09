"""
Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

Задача "Регистрация покупателей":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса. Эта таблица должна
содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)
add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна
добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000.
 Для добавления записей в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users,
в противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age,
balance(по умолчанию 1000).
Создайте цепочку изменений состояний RegistrationState.
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и
запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной
crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
"""
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging

from crud_function14_5 import *

api = '123'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

baza = get_all_products()

in_kb = InlineKeyboardMarkup()
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(in_button1)
in_kb.add(in_button2)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button1)
kb.insert(button2)
kb.add(button3)
kb.add(button4)

by_kb = InlineKeyboardMarkup(row_width=4)
by_button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
by_button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
by_button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
by_button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
by_kb.add(by_button1, by_button2, by_button3, by_button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for number in range(4):
        await message.answer(f'Название: {baza[number][1]} | Описание: {baza[number][2]} | Цена: {baza[number][3]}')
        with open(f'Tovary/{number+1}.jpg', 'rb') as img_number:
            await message.answer_photo(img_number,)
        await message.answer("Выберите продукт для покупки:", reply_markup=by_kb)


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('мужчинам: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n '
                              'женщинам: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    # await call.answer         # чтобы инлайн-кнопка после выполнения команды становилась кликабельна.
                                # Hо у меня и без этой команды она кликабельна ?????? !!!!!!)


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Это бот для рассчета калорий, необходимых ежедневно человеку, '
                         'в зависимости от параметров человека')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight=message.text)
    data = await state.get_data(['user_age', 'user_growth', 'user_weight'])
    count_calories = (10.0 * float(data['user_weight']) + 6.25 * float(data['user_growth'])
                      - 5.0 * float(data['user_age']) + 5)
    await message.answer(f'Ваша норма калорий : {count_calories} ')
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(users_name=message.text)
    data = await state.get_data(['users_name'])
    if is_included(data['users_name']):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(users_name=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(users_email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(users_age=message.text)
    data1 = await state.get_data(['users_name', 'users_email', 'users_age'])
    add_user(data1['users_name'], data1['users_email'], int(data1['users_age']))
    conn.commit()
    await message.answer('Вы зарегистрированы.')

    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
