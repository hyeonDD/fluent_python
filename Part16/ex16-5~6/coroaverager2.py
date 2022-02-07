from collections import namedtuple

Result = namedtuple('Result', 'count averager')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break #1
        total += term
        count += 1
        averager = total/count
    return Result(count, average) #2
