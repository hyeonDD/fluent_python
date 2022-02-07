from functools import wraps

def coroutine(func):
    """데커레이터: `func`를 기동해서 첫 번째 `yield`까지 진행한다."""
    @wraps(func)
    def primer(*args, **kwargs): #1
        gen = func(*args, **kwargs) #2
        next(gen) #3
        return gen #4
    return primer