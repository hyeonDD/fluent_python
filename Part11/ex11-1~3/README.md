<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-6/UML_class_diagram.png)
 -->
# 파이썬 문화에서의 인터페이스와 프로토콜
파이썬은 ABC가 소개되기 전에 이미 성공을 거두었고, 기존 코드 대부분은 ABC를 전혀 사용하지 않는다. 필자는 1장부터 줄곧 **덕 타이핑**과 프로토콜에 대해 이야기했다. 10.3절 '프로토콜과 덕 타이핑'에서는 프로토콜을 파이썬과 같은 동적 자료형을 제공하는 언어에서 다형성을 제공하는 비공식 인터페이스라고 정의했다.

동적 자료형 언어에서는 인터페이스가 어떻게 작동할까? 우선 기본적으로 파이썬 언어에는 interface라는 키워드가 없지만, ABC에 상관없이 모든 클래스는 인터페이스를 가지고 있다. 클래스가 상속하거나 구현한 공개 속성(메서드나 데이터 속성)들의 집합이 인터페이스다. 여기에는 __getitem__()이나 __add__() 같은 특별 메서드도 포함된다.

보호된 속성은 단지 명명 관례(앞에 언더바를 하나붙임)이고 비공개 속성도 쉽게 접근할 수 있지만(9.7절'파이썬에서의 비공개 속성과 보호된 속서' 참조), 보호된 속성과 비공개 속성은 인터페이스에 속하지 않는다고 정의되어 있다. 이 관례를 어기는 것은 좋지 않다.

한편 공개 데이터 속성을 객체의 인터페이스로 사용하는 것은 나쁘지 않다. 필요하면 언제나 데이터 속성을 호출 코드를 망가뜨리지 않고 <객체>.<속성> 구문을 사용해서 게터/세터를 구현하는 프로퍼티로 변환할 수 있기 때문이다. Vector2d에서 이 작업을 했었다. 아래 에제는 공개 데이터 속성 x와 y를 가진 첫 번째 버전이다.

```
class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    # 이후 메서드 생략
```

- [불변형 Vector 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-6~7/vector2d_v3.py)에서 우리는 x와 y를 읽기 전용 프로퍼티로 변경했다(변경된 부분을 아래예제로 가져왔다). 이것은 상당한 리팩토링이지만, Vector2d 인터페이스의 핵심 부분은 바뀌지 않았다. 사용자는 여전히 my_vector.x와 my_vector.y를 이용해서 값을 읽을 수 있기 때문이다.

```
calss Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
    # 이후 메서드 생략
```
인터페이스의 정의에 대해서는 '시스템에서 어떤 역할을 할 수 있게 해주는 객체의 공개 메서드의 일부'라고 설명을 보충할 수 있다. 바로 이것이 파이썬 문서에서 특정 클래스를 지정하지 않고 'file과 같은 객체'혹은 '반복형'이라고 말할 때 의미하는 것이다. 어떤 역할을 완수하기 위한 메서드 집합으로서의 인터페이스를 스몰토크에서는 **프로토콜**이라고 불렀으며, 이 용어는 다른 동적 언어 커뮤니티에 퍼져나갔다. 프로토콜은 상속과 무관하다. 클래스는 여러 프로토콜을 구현해서 객체가 여러 역할을 할 수 있게 만들 수도 있다.

프로토콜은 인터페이스지만 비공식적이다. 즉, 문서와 관례에 따라 정의되지만, 공식 인터페이스처럼 강제할 수 없다(이 장 뒤에서 인터페이스를 따르도록 ABC가 강제하는 방법을 설명한다). 프로토콜은 특정 클래스에서 부분적으로 구현할 수 있으며, 이렇게 해도 문제가 없다. 어떤 API에서 'file과 같은 객체'를 요구할 때, 단순히 bytes를 반환하는 read()메서드만 구현하면 되는 경우도 종종 있다. 그 상황에서 file의 다른 메서드는 관련이 있을 수도 있고 없을 수도 있다.

이 책을 쓰고 있는 현재, 파이썬 3의 memoryview 문서 (http://bit.ly/1QOxU2e)에는 memoryview 객체는 'C API 수준에서만 문서화되어 있는 버퍼 프로토콜을 지원하는' 객체와 작동한다고 설명되어 있다. bytearray 생성자 (http://bit.ly/1MDR1Lw)는 '버퍼 인터페이스에 따르는 객체'를 받는다고 설명되어 있다. 이제 'bytes와 같은 객체'를 친숙한 용어로 받아들이는 움직임이 일고 있다. 여기에서 이렇게 설명하는 것은 'X와 같은 객체', 'X 프로토콜', 'X 인터페이스'가 파이썬주의자에게는 동의어라는 것을 강조하기 위해서다.

시퀀스 프로토콜은 파이썬에서 가장 핵심적인 인터페이스 중 하나다. 다음 절에서 설명하는 것처럼, 최소한이라도 시퀀스 프로토콜을 구현하면 파이썬 인터프리터는 해당 객체를 처리하기 위해 특별한 노력을 기울인다.

# 파이썬은 시퀀스를 찾아낸다
파이썬 데이터 모델은 가능한 한 많이 핵심 프로토콜과 협업하겠다는 철학을 가지고 있다. 시퀀스의 경우, 가장 단순한 객체를 사용하는 경우에도 파이썬은 최선을 다한다.
아래 그림은 ABC로 정의된 공식적인 Sequence 인터페이스를 보여준다.

![sequence사진](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-1~3/sequence.png)

이제 아래예제의 Foo 클래스를 보자. 이 클래스는 abc.Sequence를 상속하지 않으며, 시퀀스 프로토콜 메서드 중 __getitem__() 메서드 하나만 구현한다(__len__()은 구현하지 않는다).

```
class Foo:
    def __getitem__(self, pos):
        return range(0, 30, 10)[pos]


f = Foo()
f[1]

for i in f: print(i)

20 in f
15 in f
```
__iter__() 메서드는 아직 구현하지 않았지만, 대체 수단인 __getitem__() 메서드가 구현되어 있으므로 Foo 객체를 반복할 수 있다. 파이썬 인터프리터는 0부터 시작하는 정수 인덱스로 __getitem__() 메서드를 호출하여 객체 반복을 시도하기 때문이다. 파이썬은 Foo 객체를 반복할 만큼 충분히 똑똑하므로 Foo에 __contains__() 메서드가 구현되어 있지 않더라도, 객체 전체를 조사해서 항목을 찾아냄으로써 in 연산자도 작동시킬 수 있다.

정리하면, 시퀀스 프로토콜의 중요성 때문에 __iter__()와 __contains__() 메서드가 구현되어 있지 않더라도 파이썬은 __getitem()메서드를 호출해서 객체를 반복하고 in 연산자를 사용할 수 있게 해준다.

1장에서 구현한 FrenchDeck 클래스도 abc.Sequence를 상속하지 않지만, 시퀀스 프로토콜의 __getitem__()과 __len__() 메서드를 구현한다. 아래 1장의 예제를 다시보자.

```
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
```
파이썬은 약간이라도 시퀀스를 닮은 객체는 모두 특별하게 처리하므로 1장에서 구현한 테스트 코드 대부분이 작동한다. 객체를 반복하기 위해 파이썬 인터프리터는 두 가지 다른 메서드를 시도하므로, 반복은 덕 타이핑의 극단적인 예를 보여준다.

이제 프로토콜의 동적인 성질을 잘 보여주는 또 다른 예를 살펴보자.

# 런타임에 프로토콜을 구현하는 멍키 패칭
FrenchDeck 클래스는 카드를 섞을 수 없다는 커다란 결함이 있다. 몇 년 전 필자가 FrenchDeck 예제를 처음으로 작성했을 때는 shuffle() 메서드를 구현했었다. 그러나 나중에 파이썬에 대해 어느 정도 눈을 뜬 후에는, 시퀀스처럼 작동하는 FrenchDeck 클래스라면 shuffle() 메서드를 직접 구현할 필요가 없다는 것을 깨달았다. random.shuffle()함수 문서 (https://docs.python.org/3/library/random.html#random.shuffle) 에서 설명하는것처럼 random.shuffle() 함수가 시퀀스 객체 안의 항목들을 섞어주기 때문이다.
> 규정된 프로토콜을 잘 따르면, 덕 타이핑 덕분에 기존 표준 라이브러리와 서드파티 코드를 활용할 수 있는 가능성이 높아진다.

표준 random.shuffle() 함수는 다음과 같이 사용한다.
```
from random import shuffle
l = list(range(10))
shuffle(1)
l
```
그러나 FrenchDeck 객체를 섞으려하면 아래와 같은 예외가 발생한다.
```
from random import shuffle
from frenchdeck import FrenchDeck
deck = FrenchDeck()
shuffle(deck)
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# File ".../python3.3/random.py", line 265, in shuffle
#    x[i], x[j] = x[j], x[i]
# TypeError: 'FrenchDeck' object does not support item assignment
```
에러 메세지가 원인을 잘 설명하고 있다. 'FrenchDeck 객체가 할당을 지원하지 않기'때문이다. shuffle() 함수는 컬렉션 안의 항목들을 교환시킴으로써 작동하는데, FrenchDeck 클래스는 **불변** 시퀀스 프로토콜만 구현하고 있다. 가변 시퀀스는 __setitem__() 메서드도 지원해야 한다.
파이썬은 동적 언어이므로 코드를 대화형 콘솔에서 실행하는 동안에도 이 문제를 수정할 수 있다. 아래예제에서 어떻게 처리하는지 알아보자.
```
def set_card(deck, position, card): #1
    deck._cards[position] = card

FrenchDeck.__setitem__ = set_card #2
shuffle(deck) #3
deck[:5]
```
1. deck, position, card를 인수로 받는 함수를 생성한다.
2. 그 함수를 FrenchDeck 클래스의 __setitem__이라는 이름의 속성에 할당한다.
3. 이제 FrenchDeck 클래스가 가변 시퀀스 프로토콜에 필요한 메서드를 구현하므로, deck을 섞을 수 있다.

__setitem__() 특별 메서드의 시그너처는 파이썬 언어 참조 문서의 3.3.6절 '컨테이너 자료형 열거하기' (http://bit.ly/1QOyDQY) 에 정의되어 있다. 참조 문서에 들어 있는 self, key, value 대신 여기서 deck, position, card를 매개변수로 사용한 것은 파이썬 메서드는 단지 평범한 함수며, 첫 번째 매개변수로 self를 사용하는 것은 관례일 뿐이라는점을 보여주기 위한 것이다. 콘솔 세션에서는 이렇게 해도 괜찮지만, 파이썬 소스 파일에서는 문서화된 대로 self, key, value를 매개변수로 사용하는 것이 좋다.

deck 객체에 _cards라는 이름의 속석이 있고, _cards가 가변 시퀀스임을 set_card()가 알고있다는 것이 비결이다. 그러고 나서 set_card() 함수가 FrenchDeck 클래스의 __setitem__특별 메서드에 연결된다. 이 방법은 **멍키 패칭**의 한 예다. 멍키 패칭은 소스코드를 건드리지 않고 런타임에 클래스나 모듈을 변경하는 행위를 말한다. 멍키 패칭은 강력하지만, 비공개 속성이나 문서화되지 않은 부분을 다루는 경우가 많기 때문에 패치하는 코드와 패치될 프로그램이 아주 밀접하게 연관되어 있다.

위의 예제는 멍키패칭의 사례를 보여주는 것 외에도 프로토콜이 동적이라는 것을 잘 보여준다. random.shuffle()함수는 자신이 받는 인수의 자료형에 대해서는 신경 쓰지 않는다. 단지 받은 객체가 일부 가변 시퀀스 프로토콜을 구현하고 있으면 될 뿐이다. 심지어 해당 객체가 필요한 메서드를 '원래부터' 가지고 있었는지, 아니면 나중에 얻었는지는 전혀 문제가 되지 않는다. 지금까지 객체가 어떤 프로토콜을 구현하는 한 자료형에 상관없이 객체를 작동시키는 '덕 타이핑'에 대해 알아보았다.

ABC 다이어그램은 프로토콜이 추상 클래스에 문서화된 명시적인 인터페이스와 어떻게 연관되는지 보여주기 위한 것이었지만, 지금까지 실제로 어떠한 ABC 클래스도 상속하지 않았다. 다음 절에서는 ABC를 단지 문서로서가 아니라 직접 활용해본다.