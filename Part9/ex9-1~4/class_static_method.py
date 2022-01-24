class Demo:
    @classmethod
    def klassmeth(*args):
        return args #1
    @staticmethod
    def statmeth(*args):
        return args #2

print(Demo.klassmeth()) #3

print(Demo.klassmeth('spam'))

print(Demo.statmeth()) #4

print(Demo.statmeth('spam'))