#!/usr/bin/python3

""" домашнее задание B4.12 """

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import User, Sessions as User_Sessions

DEBUG = True
ATHLETE_DB_PATH = "sqlite:///sochi_athletes.sqlite3"

# Объявляем класс для SQLAlchemy-ORM:
Base = declarative_base()
class Athlete(Base):
    """ описание таблицы атлетов """
    __tablename__ = "athelete"

    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

    # при строковом выводе на экран выводим ФИО:
    def __str__(self):
        return self.name

# Инциализируем коннект к базе:
engine = sa.create_engine(ATHLETE_DB_PATH)
Sessions = sessionmaker(engine)

# Функция печатает список пользователей и их uuid
def print_users_uuid():
    """ отладочная функция печатает список имён пользователей и их uuid """

    session = User_Sessions()

    print("\nОтладочная функция для вывода списка пользователей и их uuid:\n" + "-" * 61)
    for user in session.query(User).all():
        print(user, user.uuid)
    print("\n")

# Функция запрашивающая id-пользователя:
def enter_user_uuid():
    """ функция запрашивает от пользователя uuid и ищет по нему запись в базе """

    input_uuid = input("Введите uuid-пользователя:").strip()

    # проверяем существование пользователя в бд:
    session = User_Sessions()

    find_user = session.query(User).filter(User.uuid == input_uuid).first()

    if find_user is None:
        print("Пользователь с таким uuid не найден!")
        exit()
    else:
        print("Найден пользователь: {name} ({birth} г. рождения, {height} рост)".format(
            name=str(find_user),
            birth=find_user.birthdate.strftime("%d %B %Y"),
            height=find_user.height
            ))
        print("Ищем 'ближайших атлетов:'")
        search_athlete(find_user)


# Функция которая по для пользователя находит двух ближайших к пользователю атлетов:
def search_athlete(find_user):
    """ функция для указанного пользователя пытается найти двух "ближайших к нему":
        1. ближайшего по росту
        2. ближайшего по дате рождения
    """
    session = Sessions()

    # ищем ближайшего по росту:
    find_athlete = session.query(Athlete).order_by(Athlete.height).filter(Athlete.height >= find_user.height).first()
    if find_athlete is not None:
        print("Найден ближайший по росту атлет:", find_athlete, find_athlete.height)
    else:
        find_athlete = session.query(Athlete).order_by(Athlete.height.desc()).filter(Athlete.height <= find_user.height).first()
        if find_athlete is not None:
            print("Найден ближайший по росту атлет:", find_athlete, find_athlete.height)
        else:
            print("Странно, ничего не найдено..")

    # ищем ближайшего по дате рождения:
    find_athlete = session.query(Athlete).order_by(Athlete.birthdate).filter(Athlete.birthdate >= find_user.birthdate).first()
    if find_athlete is not None:
        print("Найден ближайший по дате рождения атлет:", find_athlete, find_athlete.birthdate)
    else:
        find_athlete = session.query(Athlete).order_by(Athlete.birthdate.desc()).filter(Athlete.birthdate <= find_user.birthdate).first()
        if find_athlete is not None:
            print("Найден ближайший по дате рождения атлет:", find_athlete, find_athlete.birthdate)
        else:
            print("Странно, ничего не найдено..")

if __name__ == "__main__":

    # чтобы было проще проверить работоспособность программы выведем на экран пользователей и их uuid
    if DEBUG:
        print_users_uuid()

    # предлагаем ввести uuid пользователя
    enter_user_uuid()
