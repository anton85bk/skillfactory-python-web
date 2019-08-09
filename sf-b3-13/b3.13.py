#!/usr/bin/python3

""" Домашнее задание модуля B.3 """

import sys # чтобы выбирать между файлом и выводом на экран через 'sys.stdout'

class HTML():
    def __init__(self, output=None):
        # заранее известен таг - <html>
        self.tag = "html"
        self.innerHTML = ""

        # определяем вывод - на экран или в файл
        if output is None:
            self.output = sys.stdout
        else:
            self.output = output

    # чтобы поддерживался менеджер контекста 'with'
    def __enter__(self):
        return self

    # только когда with завершается у экземпляра класса HTML - тогда происходит вывод
    # в наследуемых классах _необходимо_ переписать этот метод чтобы вывод не происходил 
    def __exit__(self, type, value, traceback):
        # формирование вывода осуществляется методом .output_html()
        print(self.output_html(), file=self.output)

    # функция для формирования HTML-структуры с этим тегом и вложенными в него html-элементами
    def output_html(self):
        # простой режим вывода только парных тегов, без аттрибутов
        return("<{tag}>{html}</{tag}>".format(tag=self.tag, html=self.innerHTML))

    # реализация оператора сложения, применяемого в условии для формирования содержимого html-документа
    def __add__(self, other):
        # формирование содержимого вложенного html-содержимого осуществляется методом .output_html()
        self.innerHTML += "\n" + other.output_html() + "\n"
        return self

class TopLevelTag(HTML):
    def __init__(self, tag=None):
        # чтобы не повторять код родительской инициализации с self.innerHTML:
        super().__init__(tag)

        # расширяем реализацию поддержкой поля self.tag
        # (теперь доступны любые другие тэги кроме <html>)
        self.tag = tag

    def __exit__ (self, type, value, traceback):
        # при выходе из вложенного тега ничего не нужно делать
        # в отличие от выхода из класса HTML
        # (иначе бы экран был заполне промежуточными данными)
        pass

class Tag(TopLevelTag):
    def __init__(self, tag=None, is_single=False, **kwargs):
        # чтобы не повторять код родительской инициализации с self.tag, self.innerHTML:
        super().__init__(tag)

        # расширение реализации поддержкой is_single (теперь доступны одинарные тэги) 
        self.is_single = is_single

        # расширение реализации поддержкой параметра text
        # (вложенное текстовое содержание свойственное для <h1>, <p> и т.д. тегов)
        self.text = ""

        # расширение поддержкой аттрибутов у html-элемента
        self.attributes = ""
        for key, value in kwargs.items():
            # я не понял зачем вообще передавать в виде кортежа аргументы для klass, но ладно, распакуем кортеж:
            if isinstance(value, tuple):
                value = " ".join(value)

            # приводим Python условности к нормальному HTML-виду:
            if key == "klass":
                key = "class"
            key.replace("_", "-")

            # формируем строчку содержащую аттрибуты текущего тэга:
            self.attributes += " {key}=\"{value}\"".format(key=key, value=value)

    def output_html(self):
        # полностью переопределяем функцию
        # теперь поддерживаются аттрибуты тегов и одинарные теги: 
        if self.is_single:
            return("<{tag}{attrib}/>{html}".format(tag=self.tag, attrib=self.attributes, html=self.innerHTML))
        else:
            return("<{tag}{attrib}>{text}{html}</{tag}>".format(tag=self.tag, attrib=self.attributes, text=self.text, html=self.innerHTML))

if __name__ == "__main__":
    with HTML(output=None) as doc:

        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body

