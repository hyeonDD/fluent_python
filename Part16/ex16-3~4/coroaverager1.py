"""
coro_avg = averager() #1
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg)) #2
print(coro_avg.send(10)) #3
print(coro_avg.send(300))
print(coro_avg.send(50))

"""
from coroutil import coroutine #4

@coroutine #5
def averager(): #6
    total = 0.0
    count =0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average =  total/count

coro_avg = averager() #1
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg)) #2
print(coro_avg.send(10)) #3
print(coro_avg.send(300))
print(coro_avg.send(50))