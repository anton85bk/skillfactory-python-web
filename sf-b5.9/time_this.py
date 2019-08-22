#!/usr/bin/python3

""" 5.9 задание на декораторы и тайминг """

import time

class TimeThis():
    def test(self, *args):
        avg_time = 0
        for i in range(1, self.iterations + 1):
            t0 = time.time()
            self.test_function(*args)
            t1 = time.time()
            avg_time += (t1 - t0)
        print("Количество запусков: %d. Среднее время выполнения: %.5f секунд\n" % (self.iterations, float(avg_time/self.iterations)))

    def __init__(self, arg):

        if isinstance(arg, int):
            # первое для декоратора - принимаемый аргумент количество итераций 
            self.iterations = arg
        else:
            # второе для случая использованяи класса с `with`
            self.test_function = arg
            self.iterations = 10

    def __call__(self, func):
        def wrapper(*args):
            self.test_function = func
            self.test(*args)

            ## возвращаем функцию на случай если её результат требуется для чего-то
            # (например для нашего "print(do_fibo(400000000000000000000000))")
            return func(*args)
        return wrapper

    def __enter__(self, *args):
        self.test()
        return self

    def __exit__(self, *args):
        pass

@TimeThis(100)
def do_fibo(stop):
    numbers = [1, 2]
    current_a = 1
    current_b = 2
    while (current_a + current_b) < stop:
        numbers.append(current_a + current_b)
        current_b, current_a = current_a + current_b, current_b
    return numbers

    if a + b < stop:
        print(a + b)
        do_fibo(b, a + b)
    else:
        print(a + b)

def do_progression():

    print("time to sleep")
    time.sleep(1)

    return True

    print("asdfasdfasdf")
if __name__ == "__main__":

    # запускаем функцию 1 раз, но на самом деле она выполнится 10 раз
    print(do_fibo(400000000000000000000000))

    with TimeThis(do_progression) as timer:
        pass
