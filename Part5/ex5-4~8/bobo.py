import bobo

@bobo.query('/') # bobo.query() 데커레이터는
def hello(person):
    return 'Hello %s!' % person