"""
Задача "Средний баланс пользователя":
Для решения этой задачи вам понадобится решение предыдущей.
Для решения необходимо дополнить существующий код:
Удалите из базы данных not_telegram.db запись с id = 6.
Подсчитать общее количество записей.
Посчитать сумму всех балансов.
Вывести в консоль средний баланс всех пользователя.

Пример результата выполнения программы:
Выполняемый код:
# Код из предыдущего задания
# Удаление пользователя с id=6
# Подсчёт кол-ва всех пользователей
# Подсчёт суммы всех балансов
print(all_balances / total_users)
connection.close()

Вывод на консоль:
700.0
"""

import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)',
#                    (f'User{i}', f'example{i}@gmail.com',
#                     f'{i * 10}', '1000'))

# for i in range(1, 11, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id = ?',
#                    (500, f'{i}'))

# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE id = ?',
#                    (f'{i}',))

# cursor.execute('DELETE FROM Users WHERE id = ', (6,))
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
all_balance = cursor.fetchone()[0]
print(all_balance / total_users)


connection.commit()
connection.close()
