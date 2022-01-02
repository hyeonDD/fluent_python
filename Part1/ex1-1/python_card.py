import collections

Card = collections.namedtuple('Card', ['rank','suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank,suit) for suit in self.suits
                                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

beer_card = Card('7', 'diamonds')

print(beer_card)

deck = FrenchDeck()
print(f'전체 카드수 : {len(deck)}') # __len__ 특별메서드로 인해 _cards의 전체수를 바로 반환

print(f'첫번째 _cards : {deck[0]}') # __getitem__ 특별메서드로 인해 n번째 카드를 읽을 수 있음.
print(f'마지막째 _cards : {deck[-1]}') # __getitem__ 특별메서드로 인해 n번째 카드를 읽을 수 있음.

# 임의의 카드를 골라내는 메서드 random.choice()모듈

from random import choice
print(f'임의의 카드 {choice(deck)}') # 시퀀스에서 항목을 무작위로 가져와주는 random 모듈의 choice 메서드
print(f'임의의 카드 {choice(deck)}') # 시퀀스에서 항목을 무작위로 가져와주는 random 모듈의 choice 메서드
print(f'임의의 카드 {choice(deck)}') # 시퀀스에서 항목을 무작위로 가져와주는 random 모듈의 choice 메서드

# 위경우 __getitem__() 메서드는 list 형의 self._cards 를 반환해주기에 list형의 slicing도 자동으로 지원가능하게해줌.

print(f'list형의 슬라이싱 기능 {deck[:3]}') # list형의 슬라이싱 사용가능 확인
print(f'list형의 슬라이싱 기능 {deck[12::13]}') # list형의 슬라이싱 사용가능 확인

# list 형은 이터러블한 자료구조이기에 반복문 (for,while 도 사용가능)

for card in deck:
    print(f'반복문 for 확인 {card}')

# __contains__() 특별 메서드가 없다면 in 연산자는 차례대로 검색한다.
print('in연산자 확인', Card('Q','hearts') in deck)
print('in연산자 확인', Card('7','beasts') in deck)

# 정렬의 경우
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

# print(len(suit_values) , suit_values[card.suit])

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


# 카드를 오름차순으로 나열
for card in sorted(deck, key=spades_high): # sorted 메서드의 key 파라미터 사용시 key=??? 의 기준으로 정렬시켜줌.
    print(f'오름차순 확인 {card}')




