from array import array
import math

class Vector2d:
    typecode = 'd' #1

    def __init__(self, x, y):
        self.x = float(x) #2
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y)) #3

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self) #4
    
    def __str__(self):
        return str(tuple(self)) #5

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + #6
                bytes(array(self.typecode, self))) #7

    def __eq__(self, other):
        return tuple(self) == tuple(other) #8
    
    def __abs__(self):
        return math.hypot(self.x, self.y) #9
    
    def __bool__(self):
        return bool(abs(self)) #10