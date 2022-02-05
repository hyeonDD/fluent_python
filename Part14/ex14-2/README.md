<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-2/UML_class_diagram.png)
 -->
# 반복형과 반복자

14.1.1절 'Sequence가 반복 가능한 이유: iter() 함수'에서 설명한 내용을 바탕으로 다음과 같은 정의를 도출할 수 있다.

---

**반복형**
iter() 내장 함수가 반복자를 가져올 수 있는 모든 객체와 **반복자**를 반환하는 __iter__() 메서드를 구현하는 객체는 반복형이다. 0에서 시작하는 인덱스를 받는 __getitem__() 메서드를 구현하는 객체인 시퀀스도 마찬가지다.

---

반복형과 반복자의 관계를 명확히 하는 것은 중요하다. 파이썬은 반복형 객체에서 반복자를 가져온다.

다음은 문자열을 반복하는 간단한 for 루프다. 여기서 'ABC' 문자열은 반복형이다. 반복자가 보이지 않지만, 내부 어딘가에 있다.
```
s = 'ABc'
for char in s:
    print(char)
"""
A
B
C
"""
```
for 문 대신 while 문을 이용해서 직접 이 괒ㅇ을 흉내 내려면 다음과 같이 작성해야 한다.
```
s = 'ABC'
it = iter(s) #1
while True:
    try:
        print(next(it)) #2
    except StopIteration: #3
        del it #4
        break #5

"""
A
B
C
"""
```
1. 반복형에서 반복자 it를 생성한다.
2. 반복자에서 next를 계속 호출해서 다음 항목을 가져온다.
3. 더 이상 항목이 없으면 반복자가 StopIteration 예외를 발생시킨다.
4. it에 대한 참조를 해제해서 반복자 객체를 제거한다.
5. 루프를 빠져나온다.

Stopiteration은 반복자가 모두 소진되었음을 알려준다. 이 예외는 for 루프 및 지능형 리스트, 튜플 언패킹 등 다른 반복 과정에서 내부적으로 처리된다.

반복자에 대한 표준 인터페이스는 다음과 같은 메서드 두 개를 정의한다.

---

**__next__()**
다음에 사용할 항목을 반환한다. 더 이상 항목이 남아 있지 않으면 StopIteration을 발생시킨다.
**__iter__()**
self를 반환한다. 그러면 for 루프 등 반복형이 필요한 곳에 반복자를 사용할 수 있게 해준다.

---
이는 __next__() 추상 메서드를 정의하는 collections.abc.Iterator ABC 및 추상 __iter__() 메서드를 정의한 서브클래스 Iterable에 공식화되어 있다. 아래 그림을 보자.

![Iterable, Iterator ABC추상메서드](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-2/iter.png)

Iterator ABC는 return self 문장만으로 __iter__() 메서드를 구현한다. 이렇게 하면 반복형이 필요한 곳에 반복자를 사용할 수 있다. abc.Iterator의 소스코드는 아래와 같다.

(http://bit.ly/1C14QOi) 에서 발췌
```
# abc.Iterator 클래스의 일부.
class Iterator(Iterable):

    __slots__ = ()

    @abstractmethod
    def __next__(self):
        '반복자에서 다음 항목을 반환한다. 항목이 소진되면 StopIteration 예외를 발생시킨다.'
        raise StopIteration

    def __iter__(self):
        return self

    @classmethod
    def __subclasshook__(cls, C):        
        if cls is Iterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and
                any("__iter__" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemente
```
> Iterator ABC 추상 메서드가 파이썬 3에서는 it.__netx__()며, 파이썬 2에서는 it.next()다. 언제나 그렇듯이 특별 메서드를 직접 호출하면 안 되며, 파이썬 2와 3에서 내장 함수인 next()를 이용해서 next(it) 형태로 호출해야 한다.

파이썬 3.4의 Lib/types.py 모듈 소스 코드 (https://hg.python.org/cpython/file/3.4/Lib/types.py) 에는 다음과 같은 주석이 붙어 있다.

---

- 파이썬의 반복자는 자료형이 아니라 프로토콜이다.
- 상당히 많은 유동적인 수의 내장 자료형이 반복자의 *일부*를 구현한다.
- 자료형을 검사하면 안 된다! 대신 hasattr()을 이용해서
- '__iter__'와 '__next__' 속성이 있는지 검사하라.

---

사실 이 방식이 abc.Iterator ABC의 __subclasshook__() 메서드가 수행하는 방식이다 (위 abc.Iterator클래스의 일부)
> Lib/types.py 모듈에 들어 있는 조언과 Lib/_collections_abc.py에 구현된 논리를 고려하면, x가 반복자인지 확인하는 가장 좋은 방법은 isinstance(x, abc.iterator)를 호출하는 것이다. Iterator.__subclasshook__() 메서드 덕분에 이 방법은 x가 Iterator의 실제 서브클래스인 경우와 가상 서브클래스인 경우 모두 제대로 작동한다.

다시 14-1장의 [sentence.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-1/sentence.py)의 Sentence 클래스로 돌아가자. 이제는 파이썬 콘솔 세션에서 iter()로 반복자를 생성하고 next()로 항목을 소비하는 방법을 명확히 이해할 수 있을 것이다.
```
s3 = Sentence('Pig and Pepper') #1
it = iter(s3) #2
it # doctest: +ELLIPSIS
# <iterator object at 0x...>
next(it) #3
# 'Pig'
next(it)
# 'and'
next(it)
# 'Pepper'
next(it) #4
"""
Traceback (most recent call last):
 ...
StopIteration
"""
list(it) #5
# []
list(iter(s3)) #6
# ['Pig', 'and', 'Pepper']
```
1. 세 단어로 구성된 Sentence 객체 s3를 생성한다.
2. s3에서 반복자를 가져온다.
3. next(it)는 다음 단어를 가져온다.
4. 더 이상 단어가 없으므로 반복자가 StopIteration 예외를 발생시킨다.
5. 일단 소진된 후에는 반복자가 필요 없다.
6. Sentence를 ㅂ다시 반복하려면 생성자를 새로 만들어야 한다.

반복자가 필수적으로 구현해야 하는 메서드는 __next__()와 __iter__() 밖에 없으므로, next()를ㄹ 호출하고 StopIteration 예외를 잡는 방법 외에는 항목이 소진되었는지 확인할 방법이 없다. 그리고 반복자는 '재설정'할 수 없다. 다시 반복해야 하면 처음 반복자를 생성했던 반복형에 iter()를 호출해야 한다. 반복자 자체에 iter()를 호출하는 것은 소용이 없다. 앞에서 설명한 것처럼 Iterator.__iter__()는 단지 self를 반환하도록 구현되어 있으므로 소진된 반복자를 재설정하지 못한다.

다음의 반복자를 정의를 살펴보면서 이 절의 내용을 정리하자.

---

**반복자**
다음 항목을 반환하거나, 다음 항목이 없을 때 StopIteration 예외를 발생시키는, 인수를 받지 않는 __next__() 메서드를 구현하는 객체. 파이썬 반복자는 __iter__() 메서드도 구현하므로 **반복형이기도 하다.**

---

내장 함수 iter()가 시퀀스에 제공하는 특별한 처리 덕분에 Setence 클래스의 첫 번째 버전은 반복형이었다. 이제 표준 반복형 프로토콜을 구현해보자.