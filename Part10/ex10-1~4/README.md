<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/UML_class_diagram.png)
 -->
# Vector: 사용자 정의 시퀀스형
우리의 전략은 상속이 아니라 구성을 이용해서 벡터를 구현하는 것이다. 요소들을 실수형 배열에 저장하고, 벡터가 불변 균일 시퀀스처럼 작동하게 만들기 위해 필요한 메서드들을 구현한다.

그러나 시퀀스 메서드를 구현하기 전에, 앞에서 구현한 Vector2d 클래스와 호환성이 높은 기본 Vector 클래스를 먼저 만들어보자.

# Vector 버전 #1: Vector2d 호환
최초의 Vector 버전은 앞에서 구현한 Vector2d 클래스와 가능한 한 호환성이 높아야 한다.

그러나 Vector 생성자는 Vector2d 생성자와 호환되지 않도록 설계되어 있다. __init__() 메서드에서 임의의 인수 *args를 받아서 Vector(3, 4)나 Vector(3, 4, 5) 형태로 작동하게 만들 수도 있지만, 시퀀스 생성자는 내장 시퀀스처럼 반복형을 인수로 받게 만드는 것이 좋다.

```
Vector([3.1, 4.2])
# Vector([3.1, 4.2])
Vector((3, 4, 5))
# Vector([3.0, 4.0, 5.0])
Vector(range(10))
# Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
```

생성자 시그너처가 달라진 점 외에 요소 두개를 가진 Vector 클래스는 Vector2d로 수행했던 모든 테스트와 동일한 결과가 나오도록 만들어졌다(예를 들어 Vector([3, 4])는 Vector2d(3, 4)와 동일한 결과를 생성한다.).
> Vector에 요소가 6개 이상 있을 때는 위 예제의 마지막 줄에서 보는 것처럼 repr()이 생성한 문자열은 생략 기호(...)로 축약된다. repr()이 디버깅에 사용되므로 많은 항목을 가진 컬렉션형에서 이런 작동은 중요하다. 커다란 객체 하나가 콘솔이나 로그에서 수천 줄을 차지하게 하고 싶지는 않을 것이다. 아래예제 에서 보는 것처럼 제한된 길이로 표현하려면 reprlib 모듈을 사용하라. 파이썬 2에서는 repr()이 reprlib 모듈을 호출한다. 2to3 도구는 repr()호출을 자동으로 수정해준다.

아래 예제는 Vector 클래스의 최초 버전을 보여준다. 이 예제는 9장의 Vector 클래스를 기반으로 구현했다.

- [vector_v1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/vector_v1.py)
1. '보호된' 객체 속성인 self._components는 벡터 요소를 배열로 저장한다.
2. 반복할 수 있도록 self._components에 대한 반복자를 반환한다.
3. self._components를 제한된 길이로 표현하기 위해 reprlib.repr()을 사용한다(즉, array('d',[0.0, 1.0, 2.0, 3.0, 4.0, ...]) 형태로 출력된다).
4. 문자열을 Vector 생성자에 전달할 수 있도록 앞에 나오는 문자열 'array('d','와 마지막에 나오는 괄호를 제거한다.
5. self._components에서 바로 bytes 객체를 생성한다.
6. 이제는 hypot() 함수를 사용할 수 없으므로, 각 요소의 제곱을 합한 뒤 제곱근을 구하기 위해 sqrt()를 호출한다.
7. 이전 버전의 frombytes()에서 마지막 줄만 변경하면 된다. 이제는 앞에서 했던 것처럼 *를 이용해서 언패킹할 필요 없이, memoryview를 바로 생성자에 전달한다.

reprlib.repr()을 사용한 방법에 대해서는 약간 더 설명을 해야 할 것 같다. 이 함수는 생략 기호를 이용해서 생성할 문자열의 길이를 제한하므로 대형 구조체나 재귀적 구조체도 안전하게 표현한다. 필자는 repr()이 Vector 객체를 Vector(array('d', [3.0, 4.0, 5.0]))이 아니라 Vector([3.0, 4.0, 5.0])으로 출력하기를 원했다. Vector 내부에 배열을 사용하는 구현 내용을 외부에 노출시키고 싶지 않았기 때문이다. 이렇게 생성된 문자열로 동일한 Vector 객체를 생성할 수 있으므로, 필자는 리스트 인수를 이용한 더 간단한 구문을 좋아한다.

__repr__()을 구현할 때 reprlib.repr(list(self._components)) 문장으로 components를 간략히 출력할 수도 있엇다. 그러나 단순히 list.repr()을 사용하기 위해 self._components의 모든 항목을 list에 복사하는 것은 낭비다. 대신 reprlib.repr()을 self._components 배열에 직접 적용하고 나서 []바깥족에 있는 글자들을 잘라냈다. 위 예제의 __repr__() 메서드 두 번째 줄이 실행하는 것이 바로 이 과정이다.
> 디버깅에 사용되므로 객체에 호출한 repr()은 결코 예외를 발생시키면 안 된다. __repr__() 구현 안에서 무언가 잘못되면 문제를 안에서 해결하고 사용자가 타깃 객체를 알아볼 수 있는 최상의 형태를 출력해야 한다.

__str__(), __eq__(), __bool__() 메서드는 Vector2d에서 전혀 바뀌지 않았으며, frombytes() 메서드는 글자 하나만 바뀌었다(마지막 행에서 별표 하나만 제거되었다). 원래의 Vector2d 클래스를 반복형으로 만들었기 때문에 이런 장점이 있다.

그건 그렇고, Vector 클래스가 Vector2d 클래스를 상속받도록 만들 수도 있었지만, 다음과 같은 두 가지 이유 때문에 상속하지 않았다. 첫째, 생성자가 호환되지 않으므로 상속받는 것은 좋지 않다. __init__()에서 매개변수를 영리하게 처리해서 이 문제를 해결할 수 있었지만, 두 번째 이유가 더 중요하다. 필자는 Vector 클래스가 시퀀스 프로토콜을 구현하는 독자적인 예제가 되기를 원했다. 이제 **프로토콜**이라는 용어에 대해 살펴보고 나서 Vector 클래스가 시퀀스 프로토콜을 구현하도록 만들어보자.

# 프로토콜과 덕 타이핑
파이썬에서는 완전히 작동하는 시퀀스형을 만들기 위해 어떤 특별한 클래스를 상속할 필요가 없음을 이미 1장에서 설명했다. 단지 시퀀스 프로토콜에 따르는 메서드를 구현하면 된다. 그런데 지금 어떤 프로토콜에 대해 이야기하고 있는 것일까?

객체지향 프로그래밍에서 프로토콜은 문서에만 정의되어 있고 실제 코드에서는 정의되지 않는 비공식 인터페이스다. 예를 들어 파이썬의 시퀀스 프로토콜은 __len__()과 __getitem__()메서드를 동반할 뿐이다. 표준 시그너처와 의미에 따라 이 메서드들을 구현하는 어떠한 클래스도 시퀀스가 필요한 곳에 사용될 수 있다. 그 클래스의 슈퍼클래스가 무엇인지는 중요하지 않다. 단지 필요한 메서드만 제공하면 된다. 이런 사례를 1장 1절에서 이미 보았다. 편의를 위해 1절의 소스 일부분을 가져왔다.

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
위 소스의 FrenchDeck 클래스는 시퀀스 프로토콜을 구현하므로 파이썬에서 제공하는 여러 기능을 활용할 수 있다. 코드 어디에서도 시퀀스 프로토콜을 따른다고 정의한 곳은 없다. 이 클래스가 object를 상속하고 있지만 파이썬 경험이 있는 프로그래머들은 이 코드를 보고 시퀀스라는 것을 알 수 있다. 이 클래스가 시퀀스처럼 **동작**하기 때문에 시퀀스인 것이다. 바로 이 점이 중요하다.

이 장을 시작할 때 인용한 알렉스 마르텔리의 글에 따라 이 메커니즘을 **덕 타이핑**이라고 부른다.

프로토콜이 비공식적이며 강제로 적용되는 사항이 아니므로 클래스가 사용되는 특정 환경에 따라 프로토콜의 일부만 구현할 수도 있다. 예를 들어 반복을 지원하려면 __getitem__() 메서드만 구현하면 되며, __len__() 메서드를 구현할 필요는 없다.

이제 Vector 클래스 안에 시퀀스 프로토콜을 구현하자. 여기에서는 슬라이싱을 지원하지 않지만, 나중에 슬라이싱 지원 기능을 추가한다.

# Vector 버전 #2: 슬라이스 가능한 시퀀스

FrenchDeck 예제에서 self._components를 가용한 것처럼 객체 안에 들어 있는 시퀀스 속성에 위임하면 시퀀스 프로토콜을 구현하기 위한 __len__()과 __getitem__() 메서드를 다음과 같이 구현할 수 있다.

```
class Vector:
    # 중략
    # ...

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]
```
이 두 메서드가 추가되었으니, 다음과 같은 연산을 수행할 수 있다.

```
v1 = Vector([3, 4, 5])
len(v1)
# 3
v1[0], v1[-1]
# 3.0 5.0

v7 = Vector(range(7))
v7[1:4]
# array('d', [1.0, 2.0, 3.0])
```
여기에서 볼 수 있는 것처럼 슬라이싱도 지원된다(제대로 하는 것은 아니지만). Vector의 슬라이스도 배열이 아니라 Vector 객체가 되면 더 좋을 것이다. 이전의 FrenchDeck 클래스도 동일 한 문제가 있다. FrenchDeck을 슬라이싱하면 리스트가 생성된다. Vector를 슬라이싱해서 생성된 평범한 배열은 Vector의 기능을 상실한다.

내장된 시퀀스형은 슬라이싱했을 때 다른 자료형이 아니라 자신과 동일한 자료의 객체를 생성한다.

Vector를 슬라이싱해서 Vector 객체를 생성하려면, 슬라이싱 연산을 배열에 위임하면 안 되며, __getitem__() 메서드가 받은 인수를 분석해서 제대로 처리해야 한다.

my_seq[1:3]과 같은 구문에서 1:3을 my_seq.__getitem__() 메서드의 인자로 어떻게 변환하는지 살펴보자.

## 슬라이싱의 작동 방식
천 번 말로 하는 것보다 예제 한 번 보여주는 게 더 낫다. 아래의 예제를 살펴보자.

- [슬라이싱의 작동 방식]](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/slice_how.py)
1. 이 예제를 위해 __getitem__() 메서드는 전달받은 인수를 그대로 반환한다.
2. 인덱스는 하나며, 새로운 것은 없다.
3. 1:4 표현식이 slice(1, 4, None)이 된다.
4. slice(1, 4, 2)는 1에서 시작해 4에서 멈추며, 2씩 증가하는 것을 의미한다.
5. 놀랍다. [] 안에 콤마가 들어가면 __getitem__()이 튜플을 받는다.
6. 튜플 안에 여러 슬라이스 객체가 들어 있을 수도 있다.

이제 아래에서 slice의 속성에 대해 자세히 살펴보자
```
slice #1
# <class 'slice'>
dir(slice) #2
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']
```
1. slice는 내장된 자료형이다(이 자료형은 2.4.2절 '슬라이스 객체'에서 처음 나왔다.)
2. slice 객체를 조사하면 start, stop, step 속성과 indices() 메서드를 볼 수 있다.

위 소스 코드에서 dir(slice)를 호출하면 indices라는 흥미로운 메서드가 보이는데, 여기에 대해서는 알고 있는 것이 별로 없다. help(slice.indices) 명령을 실행하면 다음과 같은 도움말을 볼 수 있다.

---
**S.indices(len) -> (start, stop, stride)**

길이가 LEN인 시퀀스 S가 나타내는 확장된 슬라이스의 start와 stop 인덱스 및 stride 길이를 계산한다.
경계를 벗어난 인데긋의 일반적인 슬라이스를 처리하는 방법과 동일하게 잘라낸다.
---

즉, indices는 '빠지거나 음수인 인덱스' 그리고 '대상 시퀀스보다 긴 슬라이스'를 우아하게 처리하는 내장된 시퀀스에 구현된 복잡한 논리를 보여준다. 이 메서드는 주어진 길이의 시퀀스 경계안에 들어가도록 조정된 0이나 양수인 start, stop, stride로 구셩된 '정규화된' 튜플을 생성한다.
'ABCDE'처럼 길이가 5인 시퀀스에 적용한 슬라이스의 예는 다음과 같다.
```
slice(None, 10,2).indices(5) #1
# (0, 5, 2)
slice(-3, None, None).indices(5) #2
# (2, 5, 1)
```
1. 'ABCDE'[:10:2]는 'ABCDE'[0:5:2]와 동일하다.
2. 'ABCDE'[-3:]은 'ABCDE' [2:5:1]과 동일하다.
> 이 책을 쓰고 있는 현재 온라인 파이썬 라이브러리 참조문서에는 slice.indices() 메서드가 문서화되어 있지 않다. Python/C API 참조 문서 중 'PySlice_GetIndicesEx' (https://docs.python.org/3/c-api/slice.html#c.PySlice_GetIndicesEx) 는 비슷한 C 수준 함수인 PySlice_GetIndicesEx()에 대한 문서를 담고 있다. slice.indices() 메서드는 파이썬 콘솔에서 dir()과 help()로 slice 객체를 탐색하다 발견했다. 대화형 콘솔이 발견 도구로서 빛을 발휘하는 또 하나의 증거다.

우리가 구현할 Vector 코드에서는 slice 인수를 받을 때 _components 배열에 처리를 위임할 것이므로 slice.indices() 메서드를 구현할 필요가 없다. 그렇지만 기반 시퀀스가 제공하는 서비스에 의존할 수 없을 때는 이 메서드가 큰 도움이 된다.

이제 슬라이스 처리 방법을 알게 되었으니, 개선된 Vector.__getitem__() 메서드가 어떻게 구현되어 있는지 살펴보자.

## 슬라이스를 인식하는 __getitem__()
아래 예제는 Vector가 시퀀스로 동작하기 위해 필요한 __len__()과 __getitem__(), 총 2개의 메서드를 보여준다. 이제는 __getitem__()이 슬라이싱도 제대로 처리하도록 구현되어 있다.

```
# vector_v2.py의 일부: Vector 클래스에 추가된 __len__()과 __getitem__() 메서드

def __len__(self):
    return len(slef._components)

def __getitem__(self, index):
    cls = type(self) #1
    if isinstance(index, slice): #2
        return cls(self._components[index]) #3
    elif isinstance(index, numbers.Integral): #4
        return self._components[index] #5
    else:
        msg = '{cls.__name__} indices must be integers'
        raise TypeError(msg.format(cls=cls)) #6
```
1. 나중에 사용하기 위해 객체의 클래스(즉, Vector)를 가져온다.
2. index 인수가 슬라이스면,
3. _compoennts 배열의 슬라이스로부터 Vector 클래스 생성자를 이용해서 Vector 객체를 생성한다.
4. index 인수가 int 등의 정수형이면(numbers 모듈을 사용하고 있으므로, 이 함수를 사용하려면 numbers 모듈을 임포트해야 한다),
5. _components에서 해당 항목을 가져와서 반환한다.
6.  그렇지 않으면 예외를 발생시킨다.

> isinstacne()를 많이 사용한다는 것은 객체지향 설계가 잘못되었다는 것을 나타낼 수 있지만, __getitem__()에서 슬라이스를 처리하는 경우에는 정당화될 수 있다. 위 소스코드에서 추상 베이스 클래스(ABC)인 numbers.Integral에 대해 테스트하는 것을 보라. isinstance() 테스트에서 ABC를 사용하면 API를 더욱 융통성 있고 미래의 확장에 대비할 수 있게 해준다. 11장에서 이유를 설명한다. 불행히도 파이썬 3.4 표준 라이브러리에는 slice에 대한 ABC가 없다.

__getitem__()의 else 문에서 어떤 예외가 발생하는지 알아내기 위해 대화형 콘솔을 이용해서 'ABC'[1, 2] 문장의 결과를 확인했다. 파이썬에서는 TypeError를 발생시키며, '인덱스는 정수형이어야 한다'는 에러 메세지를 출력한다. 파이썬스러운 객체를 만들려면, 파이썬의 객체를 흉내 내야 한다.

일단 위 코드를 Vector 클래스에 추가한 후에는 아래 소스코드 에서 보는 것처럼 슬라이싱을 제대로 처리하게 된다.
- [vector_v1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/vector_v1_getitem_fix.py)
1. 정수형 인덱스는 단 한 요소의 값을 실수형으로 반환한다.
2. 슬라이스 인덱스는 Vector를 새로 만든다.
3. 길이가 1인 슬라이스도 Vector 객체를 생성한다.
4. Vector는 다차원 인덱싱을 지원하지 않으므로 인덱스나 슬라이스로 구성된 튜플은 에러를 발생시킨다.
