class DemoException(Exception):
    """설명에 사용할 예외 유형"""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException: #1
            print('*** DemoException handled. Countinuing...')
        else: #2
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.') #3