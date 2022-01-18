def deco(func):
    def inner():
        print('running inner()')
    return inner #1

@deco
def target(): #2
    print('running target()')

target() #3
print(target) #4

