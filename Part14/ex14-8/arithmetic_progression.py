class ArithmeticProgression:

    def __init__(self, begin, step, end=None): #1
        self.begin = begin
        self.step = step
        self.end = end # None이면 무한 수열이다.

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin) #2
        forever = self.end is None #3
        index = 0
        while forever or result < self.end: #4
            yield result #5
            index += 1
            result = self.begin + self.setp * index #6