#!/usr/bin/python3

" Возвращаем шаблонизированную главную страницу "

from datetime import date
from bottle import route, run, view, static_file
from horoscope import generate_prophecies

# API ------------------------------------------------

@route("/api/forecasts")
def cast_forecasts():
    " Возвращаем 6 строчек с предсказаниями  "
    return {"prophecies" : generate_prophecies(total_num=6, num_sentences=2)}

@route("/api/test")
def api_test():
    " Возвращает True если тест успешен "
    return {"test_passed": True}

# DYNAMIC ------------------------------------------------

@route("/")
@view("index.tpl")
def gen_index():
    return {"date" : date.today()}


# STATIC ------------------------------------------------

@route("/styles.css")
def styles_css():
    return static_file("styles.css", root="")

@route("/helper.js")
def helper_js():
    return static_file("helper.js", root="")

run(host="localhost", port=8080, autoreload=True)
