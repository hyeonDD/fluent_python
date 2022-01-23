class HauntedBus:
    """ 유령 승객이 출몰하는 버스 모델"""

    def __init__(self, passengers=[]):
        self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)
bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers) #1

bus2 = HauntedBus() #2
bus2.pick('Carrie')
print(bus2.passengers) #3

bus3 = HauntedBus()
print(bus3.passengers) #4
bus3.pick('Dave')
print(bus2.passengers) #5
print(bus2.passengers is bus3.passengers) #6
print(bus1.passengers) #7

print(dir(HauntedBus.__init__))
print(HauntedBus.__init__.__defaults__)