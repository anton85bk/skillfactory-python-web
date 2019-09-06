""" домашняя работа B6.13 """

from bottle import route, run, request, redirect, HTTPError

## всё что ниже - для возможности работы с базой: 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "album"

    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True)
    # Год запис и альбома
    year = sa.Column(sa.INTEGER)
    # артист или группа, записавшие альбом
    artist = sa.Column(sa.TEXT)
    # жанр альбома
    genre = sa.Column(sa.TEXT)
    # название альбома
    album = sa.Column(sa.TEXT)

    def __repr__(self):
        return self.album
# 

## Обработчик GET запроса
@route("/albums/<artist>")
def get_albums_artist(artist):
    albums = session.query(Album).filter(Album.artist == artist).order_by(Album.year).all()
    result = """
<p>Для группы <strong>'{}'</strong> найдено альбомов <strong>{}</strong></p>
<p><ol>{}</ol></p>
    """.format(artist, len(albums), "\n".join(["<li>" + item.album + " (жанр " + item.genre + ", " + str(item.year) + " г.)</li>"  for item in albums]))

    if len(albums) == 0:
        result += "<p><em>Названия групп чувствительны к регистру, возможно из-за этого ничего не было найдено.</em></p>"


    result += """
<form action="/albums/" method="post">
    <fieldset style="width:25%">
    <input type="text" name="artist" placeholder="Artist" value="New Artist"><br>
    <input type="text" name="genre" placeholder="Genre" value="Rock"></br>
    <input type="text" name="album" placeholder="Album" value="Super"><br>
    <input type="text" name="year" placeholder="Year" value="1999"><br>
    <input type="submit">
    </fieldset>
</form>"""

    return result
#

## Обработчик POST запроса
@route("/albums/", method="POST")
def post_albums():
    new_album = Album()
    new_album.artist = request.forms.get("artist")
    new_album.genre = request.forms.get("genre")
    new_album.album = request.forms.get("album")
    new_album.year = request.forms.get("year")

    if not new_album.year.isnumeric() or len(new_album.year) != 4:
        return HTTPError(409, "Год должен быть 4-х значным числом!")

    if not session.query(Album).filter(Album.album == new_album.album).filter(Album.artist == new_album.artist).first() is None:
        return HTTPError(409, "Альбом '{}' артиста '{}' уже есть в базе!".format(new_album.album, new_album.artist))

    # если все проверки прошли - то сохраняем запись об альбоме и редиректим пользователя на страницу со списком альбомов этого исполнителя
    session.add(new_album)
    session.commit()

    return redirect("/albums/" + request.forms.get("artist"))
#

## Устанавливаем соединение с базой, запускаем bottle-сервер
if __name__ == "__main__":
    engine = sa.create_engine(DB_PATH)
    Sessions = sessionmaker(engine)
    session = Sessions()

    run(host="localhost", port=8080, debug=True)
