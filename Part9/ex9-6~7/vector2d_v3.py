class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x) #1
        self.__y = float(y)

    @property #2
    def x(self): #3
        return self.__x #4
    
    @property #5
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y)) #6
    
    # 나머지 메서드는 생략한다.

