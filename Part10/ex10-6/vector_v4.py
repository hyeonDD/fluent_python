from array import array
import reprlib
import math
import functools #1
import operator #2

class Vector:
    typecode = 'd'

    # 중간 코드 생략

    def __eq__(self, other): #3
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self._components) #4
        return functoolsreduce(operator.xor, hashes, 0) #5
    # 이후 코드 생략
