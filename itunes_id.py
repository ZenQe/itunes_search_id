import sqlite3

# create or connect db
conn = sqlite3.connect('itunes.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS itunes(
    request INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id INT,
    word TEXT,
    pos INT,
    date TEXT);
""")
conn.commit()

# example 860011430

import datetime
import requests
import sys

# текущая дата
curdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def tz():

    # запрос ID
    id = input("Введите ID:\n")

    # Проверка что id - число
    if id.isdigit() is False:
        return print("Некорректный ID")
    id = int(id)
    # получаем имя из id
    response_name = requests.get("https://itunes.apple.com/lookup?id=" + str(id))

    if response_name.json()['resultCount'] == 0:
        return print('id', id, 'не найден')

    name = response_name.json()['results'][0]['trackName']
    convert_word = name.split()

    # поиск по слову
    for word in convert_word:
        pos = 0
        response = requests.get('https://itunes.apple.com/search?term=' + word + '&entity=software&sort=rating')
        over_pos = 0

        # поиск нужного запроса
        for req in response.json()['results']:
            pos += 1
            if 'trackId' in req:
                if req['trackId'] == id:
                    over_pos = 1
                    print(id, word, pos, curdate)
                    insert = (id, word, pos, curdate)
                    cur.execute("INSERT INTO itunes(id, word, pos, date) VALUES(?, ?, ?, ?);", insert)
                    conn.commit()

        # если нет в рейтинге:
        if over_pos == 0:
            print(id, word, 0, curdate)
            insert = (id, word, 0, curdate)
            cur.execute("INSERT INTO itunes(id, word, pos, date) VALUES(?, ?, ?, ?);", insert)
            conn.commit()

tz()

# закомментить если не нужна печать бд
cur.execute("SELECT * FROM itunes;")
print_database = cur.fetchall()
print("\nСодержимое БД:\n")
for row in print_database:
    print(row)
input('Нажмите любую клавишу для закрытия')
