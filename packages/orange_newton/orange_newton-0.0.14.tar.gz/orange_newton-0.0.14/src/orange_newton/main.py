def hello():
    print("Hello, Python")


def add(a: int, b: int) -> int:
    return a + b


def minus(a: int, b: int) -> int:
    return a - b


class Calc:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def minus(self):
        return self.a - self.b

    def multiply(self):
        return self.a * self.b

    def divide(self):
        return self.a / self.b


class Person:
    def __init__(self, name: str):
        self.name = name

    def say_name(self):
        return "My name is " + self.name

    def get_name(self):
        return self.name
