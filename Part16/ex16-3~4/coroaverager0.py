def averager():
    total = 0.0
    count =0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average =  total/count

coro_avg = averager() #1
next(coro_avg) #2
print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
