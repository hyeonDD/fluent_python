import weakref

class Cheese:

    def __init__(self, kind):
        self.kind = kind
    
    def __repr__(self):
        return 'Cheese(%r)' % self.kind

stock = weakref.WeakValueDictionary() #1
catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
                Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    stock[cheese.kind] = cheese #2

print(sorted(stock.keys())) #3
del catalog
print(sorted(stock.keys())) #4
del cheese
print(sorted(stock.keys()))
