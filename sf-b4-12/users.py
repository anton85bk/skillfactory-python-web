#!/usr/bin/python3

""" домашнее задание B4.12 """

import uuid
import os
from datetime import date
import re
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USERS_DB_PATH = "sqlite:///users.sqlite3"

# Объявляем класс для SQLAlchemy-ORM:
Base = declarative_base()
class User(Base):
    """ описание таблицы пользователей """
    __tablename__ = "users"

    uid = sa.Column(sa.INTEGER, primary_key=True)
    uuid = sa.Column(sa.TEXT)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.DATE)
    height = sa.Column(sa.REAL)

    # при создании генерим поле uuid
    def __init__(self):
        self.uuid = str(uuid.uuid4())

    # при строковом выводе на экран выводим ФИО:
    def __str__(self):
        return self.last_name + " " + self.first_name

# Инциализируем коннект к базе:
engine = sa.create_engine(USERS_DB_PATH)
Sessions = sessionmaker(engine)

# функция запрашивающая информацию при регистрации нового пользователя
def register_new_user():
    """ функция один раз запрашивает регистрацию пользователя и создаёт запись в базе """

    print("\nРегистрация нового пользователя\n" + ("=" * 31))

    print("\n(для отказа от ввода нажмите сочетание: Ctrl + C)")

    # готовимся заносить данные пользователя в соответствующий объект
    session = Sessions()
    new_user = User()

    new_user.first_name = input("Введите имя:").strip().capitalize()
    new_user.last_name = input("Введите фамилию:").strip().capitalize()

    i = False
    while not i:
        new_input = input("Введите пол (м/ж):")
        if new_input in ('м', 'М', 'ж', 'Ж'):
            new_user.gender = new_input.strip().lower()
            i = True

    i = False
    while not i:
        new_input = input("Введите email:")
        if new_input.count("@") == 1 and new_input[new_input.find("@"):].count(".") >= 1:
            new_user.email = new_input.strip().lower()
            i = True

    i = False
    while not i:
        new_input = input("Введите дату рождения (ГГГГ-ММ-ДД):")
        if re.fullmatch(r"^\d{4}\-\d{2}\-\d{2}$", new_input.strip()):
            new_user.birthdate = date.fromisoformat(new_input.strip())
            i = True

    i = False
    while not i:
        new_input = input("Введите рост (ед. измерения метры, формат 'x.xx':")
        if re.fullmatch(r"\d{1}\.\d{2}", new_input.strip()):
            new_user.height = float(new_input.strip())
            i = True

    session.add(new_user)
    session.commit()
    print("\nПользователь '" + str(new_user) + "' успешно создан!\n")

if __name__ == "__main__":

    # если базы нет - создаём пустую с нужной таблицей
    if not os.path.exists(USERS_DB_PATH):
        Base.metadata.create_all(engine)

    # в цикле запрашиваем регистрацию пользователей,
    # пока не отменено через Ctrl + C (о чём сообщается пользователю)
    try:
        while True:
            register_new_user()
    except KeyboardInterrupt:
        print("\n\n" + (45 * "v") + "\nВыполнение программы завершено пользователем.\n")
        exit()
