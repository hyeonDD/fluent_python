<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-3/UML_class_diagram.png)
 -->
# 벡터를 더하기 위해 + 오버로딩하기
---

Vector 클래스는 시퀀스형이며, '데이터 모델' 장의 3.3.6절 '컨테이너형 열거하기' 문서 (http://bit.ly/IQOyDQY)에서는 시퀀스의 결합을 위해서는 + 연산자를, 시퀀스의 반복을 위해서는 * 연산자를 지원해야 한다고 설명한다. 그러나 역시ㅓ는 +와 * 연산자로 벡터의 수학 연산을 구현한다. 구현은 약간 더 어렵지만, 벡터형은 더 의미가 있다.

---
유클리드 벡터 두 개를 더하면 양쪽 벡터 각 요소의 합으로 구성된 새로운 벡터가 생성된다. 다음 예제를 보자.
```
v1 = Vector([3, 4, 5])
v2 = Vector([6, 7, 8])
v1 + v2
v1 + v2 == Vector([3+6, 4+7, 5+8])
```
길이가 다른 두 개의 Vector 객체를 더하면 어떻게 될까? 에러를 발생시킬 수도 있지만, 정보 검색 등에서 활용되는 사례를 보면, 짧은 쪽 벡터의 빈 공간을 0으로 채워서 더하는 것이 낫다. 즉, 다음과 같이 작동해야 한다.
```
v1 = Vector([3, 4, 5, 6])
v3 = Vector([1, 2])
v1 + v3
# Vector([4.0, 6.0, 5.0, 6.0])
```
이러한 요구사항을 기반으로 아래예제와 같이 __add__() 메서드를 간단하고도 멋지게 구현할 수 있다.

```
# Vector 클래스 내부
def __add__(self, other):
    pairs = itertools.zip_longest(self, other, fillvalue=0.0) #1
    return Vector(a + b for a, b in pairs) #2
```
1. pairs는 self에서 a를, other에서 b를 가져와서 (a,b) 튜플을 생성하는 제네레이터다. self와 other의 길이가 다른 경우에는 짧은 쪽 반복형의 빠진 값을 fillvalue로 채운다.
2. pairs 양쪽 항목의 합을 생성하는 제너레이터 표현식을 이용해서 새로운 Vector 객체를 생성한다.

__add__() 메서드는 새로운 Vector 객체를 만들며, self나 other의 값을 변경하지 않음에 주의하라.
> 단항 연산자나 중위 연산자를 구현하는 특별 메서드는 결코 피연산자를 변경하면 안 되며, 이 연산자를 사용한 표현식은 새로운 객체를 생성해야 한다. 13.6절 '복합 할당 연산자'에서 설명하듯이 복합 할당 연산자만 첫 번째 피연산자인 self를 변경할 수 있다.

아래 예제에서 입증하는 것처럼 위예제에서 구현한 Vector 클래스를 사용하면 Vector 객체를 Vector2d 객체, 튜플, 그리고 숫자를 생성하는 어떠한 반복형에도 더할 수 있다.
```
v1 = Vector([3, 4, 5])
v1 + (10, 20, 30)
# Vector([13.0, 24.0, 35.0])
from vector2d_v3 import Vector2d
v2d = Vector2d(1, 2)
v1 + v2d
# Vector([4.0, 6.0, 5.0])
```
__add__() 메서드가 어떠한 반복형 객체라도 사용할 수 있는 zip_longest() 함수를 사용하며, zip_longest()가 생성한 쌍의 합을 생성하는(a + b) 제너레이터 표현식을 이용해서 새로운 Vector를 생성하므로, 위 예제처럼 Vector 객체와 다양한 반복형을 더할 수 있다.

그러나 아래예제처럼 피연산자의 순서를 바꾸면 혼합된 덧셈 연산이 실패한다.
```
v1 = Vector([3, 4, 5])
(10, 20, 30) + v1
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
TypeError: can only concatenate tuple (not "Vector") to tuple
from vector2d_v3 import Vector2d
v2d = Vector2d(1, 2)
v2d + v1
Traceback (most recent call last):
    File "<stdin>", line 1 , in <module>
TypeError: unsupported operand type(s) for +: 'Vector2d' and 'Vector'
```
서로 다른 객체형에 대한 연산을 지원하기 위해 파이썬은 중위 연산자의 특별 메서드에 특별 디스패치 메커니즘을 구현한다. 파이썬은 a + b 표현식을 다음과 같은 절차에 따라 처리한다. (아래그림)
1. a에 __add__() 메서드가 정의되어 있으면 a.__add__(b)를 호출하고, 결과가 NotImplemented가 아니면 반환한다.
2. a에 __add__() 메서드가 정의되어 있지 않거나, 정의되어 있더라도 호출 후 NotImplemented가 반환되면, b에 __radd__() 메서드가 정의되어 있는지 확인해서 b.__add__(a)를 호출하고, 결과가 NotImplemented가 아니면 반환한다.
3. b에 __radd__()가 정의되어 있지 않거나, 정의되어 있더라도 호출 후 NotImplemented가 반환되면, '**지원하지 않는 피연산자형**'이라는 메세지와 함께 TypeError가 발생한다.

![연산자 오버로딩](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-3/overload_add.png)

__radd__() 메서드는 __add__() 메서드의 '반사'또는 '역순'버전이다. 필자는 이를 '역순' 특별 메서드라고 부르는 것을 선호한다. r을 역순이라는 의미로 생각할 수도 있고, 오른쪽 피연산자의 메서드를 호출하므로 오른쪽이라고 생각할 수 있다. 이 책의 테크니컬 ㄹ뷰어인 알렉스, 안나, 레오는 '오른쪽'을 더 선호한다고 했다. 역순이든 오른쪽이든 __radd__(), __rsub__() 등의 메서드에서 r이 나타내는 것은 이런의미다.

따라서 위 예제(소스코드)의 혼합형 덧셈을 제대로 실행하려면 Vector.__radd__() 메서드를 구현해야 한다. 왼쪽 피연산자가 __add__()를 구현하고 있지 않거나, 구현하고 있더라도 오른쪽 피연산자를 처리할 수 없어서 NotImplemented를 반환할 때, 파이썬 인터프리터는 최후의 수단으로 오른쪽 연산자의 __radd__() 메서드를 호출한다.

> NotImplemented와 NotImplementedError를 혼동하지 않아야 한다. NotImplemented는 중위 연산자가 주어진 피연산자를 처리할 수 없을 때 파이썬 인터프리터에 '반환'하는 특별한 싱글턴 값이다. 반면 NotImplementedError는 서브클래스에서 반드시 오버라이드해야 함을 알려주기 위해 추상 클래스의 메서드 스텁에서 '발생'시키는 예외다.

__radd__()를 가장 간단히 구현하는 방법은 아래와 같다.

```
# Vector 클래스 내부
def __add__(self, other): #1
    pairs = itertools.zip_longest(self, other, fillvalue=0.0)
    return Vector(a + b for a, b in pairs)

def __radd__(self, other): #2
    return self + other
```
1. __add__()는 아까 구현했던 __add__와 동일하다. __radd__() 메서드가 사용하기 때문에 여기에 포함시켰다.
2. __radd__()는 단지 __add__() 메서드에 처리를 위임한다.

__radd__()를 이렇게 간단히 구현할 수 있는 경우가 종종 있다. 단지 적절한 연산자를 호출하면 된다. 이런 방식은 교환 법칙이 성립하는 모든 연산자에 적용할 수 있다. 숫자나 우리가 구현하는 Vector클래스의 경우 + 연산자의 교환 법칙이 성립하지만, 파이썬에서 시퀀스를 연결할때의 + 연산자는 교환 법칙이 성립하지 않는다.

아까 구현한 메서드들은 Vector객체나 Vector2d, 정수드릐 튜플, 실수들의 배열등 숫자 항목으로 구성된 어떠한 반복형에도 사용할 수 있다. 그러나 비반복형 객체에 적용하면 __add__()는 아래 소스코드와 같이 별로 도움이 되지 않는 메세지와 함께 에러가 발생한다.

```
# Vector.__add__()는 숫자 항목이 들어 있는 반복 가능한 피연산자가 필요하다.
v1 + 'ABC'
Traceback (most recent call last):
""" File "<stdin>", line 1, in<module>
    File "vector_v6.py", line 329, in __add__
        return Vector(a + b for a, b in pairs)
    File "vector_v6.py", line 243, in __init__
        self._components = array(self.typecode, components)
    File "vector_v6.py", line 329, in <genexpr>
        return Vector(a + b for a, b in pairs)
    TypeError: unsupported operand type(s) for +: 'float' and 'str' """
```

Vector.__add__()는 반복형 피연산자가 필요하다의 소스코드와 위 코드는 도움이 되지 않는 에러 메세지보다 더 심각한 문제가 있다. 연산자 특별 메서드가 자료형의 비호환성 문제 때문에 적절한 결과를 반환할 수 없을 때는 NotImplemented 값을 반환해야지 TypeError 예외를 발생시키면 안 된다. NotImplemented를 반환함으로써 파이썬이 역순 메서드를 호출하려고 시도할 때 다른 피연산자 조렿ㅇ의 구현자에 연산을 처리할 수 있는 기회를 줄 수 있기 때문이다.

덕 타이핑 정신을 가지고 있다면 other 피연산자의 자료형이나 그 안에 들어 있는 요소의 자료형을 검사하지 않는다. 대신 에외를 잡은 후 NotImplemented를 반환한다. 이때 아직 파이썬 인터프리터가 역순으로 연산을 시도하지 않았다면 역순 연산자를 시도한다. 역순 연산자 메서드 호출이 NotImplemented를 반환하면 그때서야 파이썬 인터프리터가 'unsupported operand type(s) for +: Vector and str.'등의 표준 에러 메시지와 함께 TypeError를 발생시킨다.

벡터 덧셈을 수행하는 특별 메서드의 최종 버전은 아래예제와 같다.

```
#vector_v6.py: vector_v5.py에 + 연산자 메서드 추가
def __add_(self, other):
    try:
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)
    except TypeError:
        return NotImplemented

def __radd__(self, other):
    return self + other
```
> 중위 연산자 메서드가 예외를 발생시키면, 연산자 디스패치 알고리즘을 중단시킨다. 특히 TypeError의 경우, 이 예외를 잡은 후 NotImplemented 값을 반환하는 것이 좋다. 예외를 발생시키는 대신 에러 코드를 반환하면, 두 피연산자의 데이터형이 다른 경우 파이썬 인터프리터가 역순 연산자 메서드의 호출을 시도해볼 수 있기 때문이다.

지금까지 __add__()와 __radd__() 메서드를 구현해서 + 연산자를 안전하게 오버로드했다. 이제부터 또 다른 중위 연산자인 * 연산자를 구현해보자.

