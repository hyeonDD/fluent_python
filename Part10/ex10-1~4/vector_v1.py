from array import array
import reprlib
import math

class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components) #1
    
    def __iter__(self):
        return iter(self._components) #2
    
    def __repr__(self):
        components = reprlib.repr(self._components) # 3
        components = components[components.find('['):-1] #4
        return 'Vector({)'.format(components)
    
    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components)) #5
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self)) #6
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv) #7
    
    # 추가
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]

v1 = Vector([3, 4, 5])
print(len(v1))

print(v1[0], v1[-1])

v7 = Vector(range(7))
print(v7[1:4])




