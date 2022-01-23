class TwilightBus:
    """승객이 사라지게 만드는 버스 모델"""

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = [] #1
        else:
            self.passengers = passengers #2

    def pick(self, name):
        self.passengers.append(name)
    
    def drop(self, name):
        self.passengers.remove(name)
