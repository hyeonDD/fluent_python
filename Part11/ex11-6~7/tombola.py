import abc

class Tombola(abc.ABC): #1

    @abc.abstractmethod
    def load(self, iterable): #2
        """iterable의 항목들을 추가한다."""
    
    @abc.abstractmethod
    def pick(self): #3
        """무작위로 항목을 하나 제거하고 반환한다.
        객체가 비어 있을 때 이 메서드를 실행하면 `LookupError`가 발생한다.
        """
    
    def loaded(self): #4
        """최소 한 개의 항목이 있으면 True를, 아니면 False를 반환한다."""
        return bool(self.inspect()) #5

    def inspect(self): #3
        """현재 안에 있는 항목들로 구성된 정렬된 튜플을 반환한다."""
        items = []
        while True:
            try: #6
                items.append(self.pick())
            except LookupError:
                break
        self.load(items) #7
        return tuple(sorted(items))
