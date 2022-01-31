<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-5/UML_class_diagram.png)
 -->
# Tombola 서브클래스 테스트 방법
Tombola 클래스를 테스트하기 위해 사용한 스크립트는 클래스 계층구조를 조사할 수 있게 해주는 다음과 같은 두 가지 클래스 속성을 사용한다.

---

**__subclasses__()
클래스의 바로 아래 서브클래스이 리스트를 반환하는 메서드. 리스트에 가상 서브클래스는 들어가지 않는다.

**_abc_registry
ABC에서만 사용할 수 잇는 데이터 속성으로, 추상 클래스의 등록된 가상 서브클래스에 대한 약한 참조를 담고 있는 WeakSet이다.

---

Tombola의 모든 서브클래스를 테스트하기 위해 필자는 Tombola.__subclass__()와 Tombola._abc_registry로 만든 리스트를 반복하고 doctest에 사용한 ConcreteTombola라는 이름에 각 클래스를 바인딩하는 스크립트를 작성했다. (책 예제 11-15, 16참고)

이것으로 Tombola ABC 사례 연구를 마친다. 다음 절에서는 실제로 코딩할 때 register() ABC 함수를 사용하는 방법에 대해 알아본다.

# register()의 실제 용법
[tombolist.py Tombola의 가상 서브클래스 TomboList](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/tombolist.py)에서는 @Tombola.register를 클래스 데커레이터로 사용했다. 예제 마지막 부분의 주석에서 설명한 것처럼, 파이썬 3.3 이전에는 이런 형태로 register()를 사용할 수 없었고, 클래스를 정의한 후에는 평범한 함수처럼 호출해야 했다.

그렇지만 이제는 register()를 데커레이터로 사용할 수 있음에도 불구하고, 다른 곳에서 정의된 클래스를 등록하기 위해 함수 형태로 사용하는 경우가 더 많다. 예를 들어 collections.abc에 대한 소스 코드 (http://bit.ly/1QOA3Lt) 에서는 tuple, str, range, memoryview 내장 자료형이 다음과 같이 Sequence의 가상 서브클래스로 등록되었다.

---

Sequence.register(tuple)
Sequence.register(str)
Sequence.register(range)
Sequence.register(memoryview)

---
그 외 여러 내장 자료형이 _collections_abc.py (http://bit.ly/1/QOA3Lt) 에있는 ABC에 등록되었다. 모듈이 임포트될 때만 등록되는데, ABC에 접근하려면 어잿든 임포트해야 하므로 아무런 문제가 되지 않는다. MutableMapping에 접근해야 isinstacne(my_dict, MutableMapping) 코드를 실행할 수 있다.

이 장은 알렉스 마르텔리가 '물새와 ABC'에세이 (399쪽)에서 보여준 약간의 ABC 마술을 설명하면서 마친다.

# 오리처럼 행동할 수 있는 거위
'물새와 ABC' 에세이에서 알렉스 마르텔리는 클래스를 등록하지 않고도 ABC의 가상서브클래스로 인식시킬 수 있음을 보여줬다. issubclass()를 사용한 테스트를 추가해서 그의 예제를 다시 보자.

```
class Struggle:
    def __len__(self): return 23

from collections import abc
isinstance(Struggle(), abc.Sized)
# Trrue
issubclass(Struggle, abc.Sized)
# True
```
issubclass() 함수는 Struggle을 abc.Sized의 서브클래스라고 간주한다 (그리고 isinstance()도 마찬가지다). abc.Sized가 __subclasshook__()이라는 특별 클래스 메서드를 구현하기 때문이다. 아래 예제를 보자.

```
# Lib/_collections_abc.py 소스 코드에서 Sized()의 정의
class Sized(metaclass=ABCMeta):
    __slots__ = ()
    @abstractmethod
    def __len__(self):
        return 0
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__): #1
                return True #2
        return NotImplemented #3
```
1. C.__mro__에 나열된 클래스(C와 C의 슈퍼클래스) 중 __dict__ 속성에 __len__이라는 속성을 가진 클래스가 하나라도 있으면,
2. True를 반환해서 C가 Sized의 가상 서브클래스임을 알려준다.
3. 그렇지 않으면 NotImplemented를 반환해서 서브클래스 검사를 진행할 수 있게 한다.

서브클래스 검사에 관심이 있다면 Libabc.py 파일 (https:///hg.python.org/cpython/file/3.4/Libabc.py#l194) 에서 ABCMeta.__subclasscheck__() 메서드에 대한 소스 코드를 살펴보기 바란다. 이 코드 안에 if가 아주 많이 있고 두 번이나 재귀적 호출을 하고 있으므로 간단하지는 않을 것이다.

__subclasshook__()은 구스 타이핑에 약간의 덕 타이핑 유전자를 추가한다. ABC를 이용해서 공식적으로 인터페이스를 정의할 수 있고, 어디에서든 isinstacne() 검사를 할 수 있고, 단지 어떤 메서드를 구현하기만 하면(혹은 __subclasshook__()이 보증하게 만드는 어떤 일이든 수행하면) 전혀 상관없는 클래스들이 함께 어울리게 만들 수 있다. 물론 이것은 __subclasshook__()을 제공하는 ABC에만 적용된다.

우리가 만든 ABC에서 __subclasshook__()을 구현하는 게 좋을까? 아마도 아닐 것이다. 파이썬 소스코드에서 필자가 본 __subclasshook__()을 구현하는 클래스들은 모두 특별 메서드 하나만 선언한 Sized 같은 ABC며, 그 클래스들은 그러한 특별 메서드명만 검사할 뿐이다. '특별한' 상태에 있으니 __len__이라는 이름을 가진 메서드는 여러분이 기대하는 일을 할 것이라고 확신할 수 있다. 그렇지만 특별 메서드와 핵심 ABC 영역에서도 그런 가정을 하는 것은 위험하다. 예를 들어 매핑은 __len__(), __getitem__(), __iter__() 메서드를 구현하지만, 정수 오프셋으로 항목을 검색할 수 없고 항목 순서를 보장하지 않으므로 Sequence의 서브타입이라고 간주하지 않는다. 물론 삽입순서는 유지하지만, 오프셋으로 항목을 검색할 수 없는 OrderDict는 예외다.

여러분이나 필자가 작성할 수 있는 ABC의 경우에는 __subclasshook__()을 훨씬 더 믿을 수 없을 것이다. 필자는 load(), pick(), inspect(), loaded()를 구현하거나 상속하는 Spam이라는 이름의 클래스가 Tombola로 작동할 거라고 믿지 않는다. Spam을 Tombola에서 상속하거나, 적어도 Tombola.register(Spam)으로 등록함으로써 프로그래머가 그 사실을 약속할 수 있게 해준다면 더 나을 것이다. 물론 여러분이 작성한 __subclasshook__() 메서드가 메서드 시그너처 및 다른 기능을 검사할 수도 있겠지만, 그럴 가치가 있을 거라고 생각하지는 않는다.