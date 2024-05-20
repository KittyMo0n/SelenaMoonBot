"""
Декораторы — это мощный инструмент в Python, который позволяет изменять поведение функции
      или метода. Декораторы оборачивают функции или методы, добавляя дополнительную
                    функциональность перед или после основной функции.
"""
import random

def simple_decorator(func):

    def wrapper():
        print("Что-то происходит перд декорируемой функцией")
        # func()
        print(func())
        print("Что-то происходит после декорируемой функции")
    return wrapper

@simple_decorator
def say_kukusiki():
    some_static_calculating = 2
    some_dynamics = random.randint(1,100)
    return {
            'static': [3, some_static_calculating],
            'dynamic': [random.randint(1,10), some_dynamics]
            }

say_kukusiki()