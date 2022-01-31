<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/UML_class_diagram.png)
 -->
# 표준 라이브러리의 ABC
파이썬 2.6 이후 표준 라이브러리에 ABC가 포함되었다. numbers와 io 패키지에서도 볼 수 있지만, 대부분의 aBC는 collections.abc 모듈에 정의되어 있으며, 이 모듈에 정의된 ABC들이 가장 많이 사용된다. 이제 어떤 ABC들이 있는지 살펴보자.

## collections.abc의 ABC
> 표준 라이브러리에 abc라는 이름을 포함하고 있는 모듈이 두 개 있다. 여기서는 collections.abc.에 대해 설명한다. 로딩 시간을 줄이기 위해 파이썬 3.4에서는 collections.abc 모듈을 collections 모듈에서 떼어내 Lib/_collections_abc.py (http://bit.ly/1QOA3Lt) 에서구현 하므로 collections와는 별도로 임포트된다. 그리고 이름이 단지 abc인 모듈, 즉 Lib/abc.py (https://hg.python.org/cpython/file/3.4/Lib/abc.py) 가 있는데, abc.ABC 클래스가 여기에 정의되어 있다. 모든 ABC가 이 모듈에 의존하지만, 직접 ABC를 만드는 경우가 아니라면 이 모듈을 임포트할 필요 없다.

아래그림은 파이썬 3.4 버전의 collections.abc에 정의된 16개의 ABC를 속성명을 생략하고 간략히 UML 클래스 다이어그램으로 보여준다. collections.abc 공식 문서는 ABC 클래스들 간의 관계, 추상 및 구상 메서드를 표 (http://bit.ly/1QOA9T8) 형태로 요약해서 잘 설명하고 있다(클래스를 상속하지 않고 사용할 수 있는 메서드를 '믹스인 메서드'라고 한다). 아래그림 에서는 다중 상속을 아주 많이 볼 수 있다. 다중 상속에 대해서는 12장에서 자세히 설명한다. 지금은 ABC에서는 일반적으로 다중 상속이 문제되지 않는다고만 알아두자.

![collections_abc_UML그림](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/collections_abc_UML.png)

위의 그림의 주요 부분을 요약하면 다음과 같다.

---

**Iterable, Container, Sized**
모든 컬렉션은 이 ABC를 상속하거나, 적어도 호환되는 프로토콜을 구현해야 한다. Iterable은 __iter__()를 통해 반복을, Container는 __contains__()를 통해 in 연산자를, Sized는 __len__()을 통해 len() 메서드를 지원한다.

**Sequence, Mapping, Set**
주요 불변 컬렉션형으로서, 각기 가변형 서브클래스가 있다. MutableSequence에 대한 자세한 다이어그램은 전장의 collections_abc_mutablesequence.jpg를, MutableMapping과 MutableSet에 대한 다이어그램은 그림3-1과 그림3-2를 참조하라.

**MappingView**
파이썬 3에서 items(), keys(), values() 메서드에서 반환된 객체는 각기 ItemsView, KeysView, ValuesView를 상속한다. ITemsView와 ValuesView는 풍부한 인터페이스를 제공하는 Set을 상속하므로 3.8.3절 '집합 연산'에서 설명한 연산자들이 포함된다.

**Callable, Hashable**
이 두 ABC는 컬렉션과 밀접한 연관이 있는 것은 아니지만, collections.abc가 파이썬 표준 라이브러리 안에서 ABC를 정의한 최초의 패키지며, 이 두 모듈은 여기에 포함시킬 가치가 있다고 생각했다. Callable이나 Hashable의 서브클래스는 본 적이 없다. 이 두 클래스는 주로 어떤 객체를 호출하거나 해시할 수 있는지 안전하게 판단하기 위해 isinstance() 함수와 함께 사용된다.

**Iterator**
Iterator는 Iterable을 상속한다. 이에 대해서는 14장에서 자세히 설명한다.

---

collections.abc 다음으로 파이썬 표준 라이브러리에서 가장 유용한 ABC 패키지는 numbers다. 다음 절에서 읽어보자.

## ABC의 숫자탑
numbers 패키지 (https://docs.python.org/3/libraray/numbers.html) 는 소위 '숫자탑'이라고 하는 것을 정의한다(말 그대로 ABC들이 선형 계츠구조로 되어 있다). 다음과 같이 Number가 최상위 슈퍼클래스며, 그 밑에 Complex, 그리고 계속해서 Integral까지 내려간다.

* Number
* Complex
* Real
* Rational
* Integral

따라서 정수형인지 검사해야 하는 경우 isinstance(x, numbers.Integral)을 이용해서 int형, bool형(int형의 서브클래스), 또는 자신을 numbers ABC에 등록한 정수형을 받을 수 있다. 그리고 언제든 클래스를 numbers.Integral의 가상 서브클래스로 등록하면, 해당 클래스의 객체가 isinstance(x, numbers.Integral) 검사를 통과할 수 있다.
그러나 값이 실수형이 될 수 있고  isinstance(x, numbers.Real)로 검사하는 경우 bool, int, float, fractions.Fraction, 또는 Numpy 등 외부 라이브러리에서 제공하는 복소수 외의 숫자형을 받을 수 있다. Numpy는 자신의 자료형을 적절히 등록한다.
> 다소 놀라운 사실이지만, decimal.Decimal은 numbers.Real의 가상 서브클래스로 등록되어 있지 않다. 프로그램 안에서 정밀도 높은 Decimal을 필요로 하는 경우 실수로 float처럼 정밀도 떨어지는 숫자형과 Decimal이 섞이는 문제를 예방하기 위한 것이다.

기존 ABC를 어느 정도 살펴봤으니, 이제 처음부터 ABC를 만들고 사용해보면서 구스 타이핑을 활용해보자. 여기에서의 목적은 누구나 ABC를 구현해보라고 장려하기 위한 것이 아니라, 표준 라이브러리 및 기타 패키지에서 볼 수 있는 ABC 소스 코드를 읽는 방법을 배우기 위한것이다.

# ABC의 정의와 사용
ABC를 생성하는 일을 정당화하기 위해, 프레임워크를 확장해야 하는 상황을 만들어보자, 여기서는 다음과 같은 상황을 가정한다.
    **웹사이트나 모바일 앱에서 광고를 무작위 순으로 보여주어야 하지만, 광고 목록에 들어 있는 광고를 모두 보여주기 전까지는 같은 광고를 반복하면 안된다.**
이제 ADAM이라는 광고 관리 프레임워크를 만든다고 가정해보자. 이 프레임워크는 사용자가 제공한 무반복 무작위 선발 클래스를 지원해야 한다. ADAM 사용자에게 '무반복 무작위 선택'요소가 갖추어야 할 성질을 명확히 알려주기 위해 우리는 ABC를 정의한다.

'스택'과'큐'에서 힌트를 얻어(이 둘 모두 사물의 물리적인 배치에 비유해서 추상 인터페이스를 설명한다), 실세계에 존재하는 것을 비유해서 ABC의 이름을 정해보자. 여기서는 집합이 소진될 때까지 반복하지 않고 유한 집합에서 무작위로 항목을 선택하도록 설계된 기계를 빙고 케이지와 로터리 블로어라고 부르겠다.

빙고의 이탈리아식 이름과 숫자를 혼합하는 통의 이름을 본떠 ABC의 이름을 Tombola로 한다.

Tombola ABC는 메서드를 네 개 가지고 있다. 그중 두 개의 추상 메서드는 다음과  같다.
* load(): 항목을 컨테이너 안에 놓는다.
* pick(): 컨테이너 안에서 무작위로 항목 하나를 꺼내서 반환한다.

나머지 두 개의 구상 메서드는 다음과 같다.
* loaded(): 컨테이너 안에 항목이 하나 이상 들어 있으면 True를 반환한다.
* inspect(): 내용물을 변경하지 않고 현재 컨테이너 안에 들어 있는 항목으로부터 만든 정렬된 튜플을 반환한다(원래의 내부 순서는 유지되지 않는다).

Tombola ABC와 세 개의 구상 클래스의 구조는 아래그림과 같다.

![collections_abc_UML그림](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/tombola_abc.png)

ABC와 세 개의 서브클래스의 UML 다이어그램. UML 관례에 따라 Tombola ABC와 이 클래스 안의 추상 메서드는 이탤릭체로 표현했다. 점선 화살표는 인터페이스 구현을 나타내며, 여기서는 TomboList가 Tombola의 가상 서브클래스임을 보여준다. 이 장 뒤에 나온 코드에서 알 수 있듯이 TomboList가 Tombola에 등록되기 때문이다.

- [tombola.py 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/tombola.py)
1. ABC를 정의하려면 abc.ABC를 상속해야 한다.
2. 추상 메서드를 @abstractmethod 데커레이터로 표시한다. 이 데커레이터에는 무서화 문자열만 들어 있는 경우가 종종 있다.
3. 골라낼 항목이 없는 경우 LookupError를 발생시키라고 문서화 문자열을 통해 코드 구현자에게 알려준다.
4. ABC에도 구상 메서드가 들어갈 수 있다.
5. ABC의 구상 메서드는 반드시 ABC에 정의된 인터페이스(즉, ABC의 다른 구상 메서드나 추상 메서드, 혹은 프로퍼티)만 사용해야 한다.
6. 구상 서브클래스가 항목을 저장하는 방법은 알 수 없지만, pick()을 계속 호출해서 Tombola 객체를 비움으로써 inspect()가 제공해야 하는 결과를 만들 수 있다.
7. 그러고 나서 load()를 호출해서 모두 다시 넣는다.
> 추상 메서드도 실제 구현 코드를 가질 수 있다. 추상 메서드가 실제 구현 코드를 담고 있더라도 서브클래스는 이 메서드 오버라이드해야 한다. 하지만 서브클래스에서는 처음부터 모든 기능을 구현하는 대신 super()를 이용해서 추상 메서드가 구현한 기능을 재사용할 수 있다. @abstractmethod 사용법에 대한 자세한 설명은 abc 모듈 문서 (https://docs.python.org/3/library/abc.html) 을 참조하라.

아래 예제의 insepct() 메서드는 아마도 어리석은 코드처럼 보일 것이다. 그러나 이 코드는 pick()과 load() 메서드를 이용해서 항목들을 모두 꺼낸 후 다시 넣어서 Tombola 내부를 조사할 수 있음을 보여준다. 이 코드의 핵심은 ABC 안에서 인터페이스에 정의된 다른 메서드만 이용하는 한 ABC에 구상 메서드를 제공하는 것도 가능하다는 점을 보여주는 것이다. 내부 데이터 구조를 알고 이쓴ㄴ Tombola의 구상 서브클래스는 언제든지 더 똑똑한 방식으로 inspect()를 오버라이드할 수 있지만, 꼭 오버라이드할 필요는 없다.

위 tombola.py 예제의 loaded() 메서드는 그리 어리석어 보이지는 않지만, 상당히 값비싼 연산을 수행한다. 단지 bool() 연산을 적용하기 위해 insepct()를 호출해서 정렬된 튜플을 생성하기 때문이다. 이 코드가 작동은 하지만, 뒤에서 보겠지만 구상 서브클래스에서 더 잘 구현할 수 있다.

우리가 비효율적으로 구현한 insepct() 메서드는 self.pick()이 발생시키는 LookupError를 잡아야 한다는 점에 주의하라. self.pick()이 LookupError를 발생시킨다는 것도 인터페이스의 일부분이지만, 파이썬에서는 문서 외에는 이 사실을 선언할 방법이 없다 (위 tombola.py의 예제의 pick() 추상 메서드에 대한 문서화 문자열을 참조하라.)

LookupError 예외를 선택한 이유는 파이썬 예외 계층구조에서 IndexError 및 KeyError와 관련된 이 예외의 위치 때문이다. IndexError와 KeyError는 Tombola 구상 서브클래스를 구현하기 위해 사용할 데이터 구조체에서 발생될 가능성이 높다. 따라서 Tombola 구상 서브클래스는 인터페이스에 따라 LookupError, IndexError, KeyError를 발생시킬 수 있다. 아래 에제를 참조하라 (전체 트리는 파이썬 표준 라이브러리의 5.4절 '예외 계층구조'를 참조하라.)


![exception계층구조](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/exception.png)

1. LookupError는 우리가 Tombola.inspect() 안에서 처리하는 예외다.
2. IndexError는 LookupError의 서브클래스로서 시퀀스에서 마지막 이후의 인덱스로 항목을 가져오려 할때 발생한다.
3. KeyError는 매핑에 존재하지 않는 키로 항목을 가져올 때 발생한다.

이제 우리만의 Tombola ABC를 구현했다. ABC가 인터페이스 검사를 제대로 수행하는지 확인 해보기 위해 아래 예제에 있는 잘못된 구현을 이용해서 Tombola를 속여보자.

```
from tombola import Tombola
class Fake(Tombola): #1
    def pick(self):
        return 13


Fake #2
# <class '__main__.Fake'>
f = Fake() #3
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
# TypeError: Can't instantiate abstract class Fake with abstract methods load
```
1. Fake를 Tombola의 서브클래스로 선언한다.
2. 클래스가 생성되었고, 아직까지 아무런 에러가 없다.
3. Fake의 객체를 생성할 때 TypeError가 발생한다. 메시지는 알아보기 쉽다. Tombola ABC에 선언된 추상 메서드 중 하나인 load()를 구현하지 않았기 때문에 Fake를 추상 메서드로 간주한다는 메시지다.

이제 우리가 처음으로 정의한 ABC가 완성되었으니, 사용하면서 클래스 검증을해보자. Tombola ABC를 상속하기 전에, ABC 코딩 규칙을 살펴봐야 할 것 같다.

## ABC 상세 구문
ABC를 선언할 때는 abc.ABC나 다른 ABC를 상속하는 방법이 가장 좋다.


그러나 abc.ABC는 파이썬 3.4에 새로 추가된 클래스다 따라서 이전 버전의 파이썬을 사용하고 있다면, (다른 기존 ABC를 상속한다는 것이 말이 안 되므로) metaclass 키워드를 사용해서 abc.AbCMeta(abc.ABC가 아니다)를 가리켜야 한다. 따라서 [tombola.py예제](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/tombola.py)는 다음과 같이 작성해야 한다.
```
class Tombola(metaclass=abc.ABCmeta):
    # ...
```

metaclass 키워드는 파이썬 3에서 소개되었으므로, 파이썬2에서는 __metaclass__ 클래스 속성을 사용해야 한다.
```
class Tombola(object): # 파이썬 2 코드다 !!!
    __metaclass__ = abc.ABCMeta
    # ...
```
메타클래스는 21장에서 설명한다. 일단 메타클래스와 ABC를 특별한 종류의 클래스라고 생각해두자. 예를 들어 '일반적인'클래스는 서브클래스를 검사하지 않으므로, 이것은 ABC의 특별한 동작 방식이다.

@abstractmethod 외에도 abc 모듈은 @abstractclassmethod, @abstractstaticmethod, @abstractproperty 데커레이터를 정의한다. 그러나 이 데커레이터 세 개는 파이썬 3.3 이후 사용 중단 안내되었다. 파이썬 3.3에서는 @abstractmethod 위에 데커레이터를 쌓아 올릴 수 있게 되어 이 세 개의 메서드가 중복되기 때문이다. 예를 들어 추상 클래스 메서드는 다음과 같이 선언한다.
```
class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def an_abstract_classmethod(cls, ...):
        pass
```
> 일반적으로 누적된 함수 데커레이터의 순서는 중요하다. @abstractmethod의 경우는 문서에서 다음과 같이 명확히 설명하고 있다.
**abstractmethod()를 다른 메서드 디스크립터와 함께 적용할 때는 이 데커레이터를 제일 안쪽에 위치시켜야 한다.**
즉, @abstractmethod와 def 문 사이에는 어떤 것도 올 수 없다.

ABC 구문에 대해 알아보았으니, 이제 모든 기능을 갖춘 Tombola 구상 서브클래스를 구현하면서 Tombola를 활용해보자.

## Tombola ABC 상속하기
Tombola ABC를 구현했으니, 이제 이 인터페이스를 만족시키는 구상 서브클래스를 두 개 만들어보자. 이 클래스들의 구성은 tombola_abc.png그림을 따른다. 가상 서브클래스는 다음 절에서 설명한다.

아래에제의 BingoCage 클래스는 더 좋은 난수생성기를 사용하도록 [뒤섞인 리스트에서 항목 골라내기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-4~8/bingocall.py)을 개선한 클래스다. BingoCage는 필요한 추상 메서드 load()와 pick()을 구현하고, Tombola에서 loaded()를 상속하고, inspect()를 오버라이드하고, __call__()메서드를 추가한다.

- [bingocall 더나은 난수생성기](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/bingocall_better.py)
1. BingoCage 클래스는 Tombola를 명시적으로 상속한다.
2. 이 클래스를 온라인 게임에 사용한다고 가정해보자. random.SystemRandom 클래스느 os.urandom()함수를 기반으로 random API를 구현한다. os 모듈 문서 (http://docs.python.org/3/library/os.html#os.urandom) 에 따르면 os.urandom() 함수는 '암호화에 적합한' 무작위 bytes를 생성할 수 있다.
3. 초기화 작업을 load() 메서드에 위임한다.
4. 평범한 random.shuffle() 함수 대신, SystemRandom 객체의 shuffle() 메서드를 사용한다.
5. pick()은 이전 구현된 구현과 동일하다.
6. __call__() 메서드도 동일한 구현이다. Tombola 인터페이스를 만족시키기 위해 필요한 것은 아니지만 메서드를 추가해도 해로운 것은 없다.

BingoCage는 Tombola의 실행 부담이 큰 loaded()와 바보 같은 inspect() 메서드를 상속한다. 이 두 메서드는 아래예제와 같이 훨씬 더 빠른 코드로 오버라이드 할 수 있다. 이 코드에서는 ABC에 구현된 메서드가 최적은 아니더라도 느긋하게 상속할 수 있음을 알 수 있다. Tombola에서 상속한 메서드들은 BingoCage에 최고의 성능을 발휘하지는 않지만, pick()과 load() 메서드를 제대로 구현하는 모든 Tombola 서브클래스에서 제대로 작동한다.

아래 예제는 Tombola 인터페이스를 제대로 구현하지만 아주 다른 클래스를 보여준다. '공'을 섞고 마지막 공을 꺼내는 대신 LotteryBlower는 임의의 위치에 있는 공을 꺼낸다.

- [Tombola의 inspect()와 loaded() 메서드를 오버라이드하는 LotteryBlower 구상 서브클래스 lotto.py](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/lotto.py)
1. 초기화 메서드는 어떠한 반복형도 받을 수 있따. 인수를 이용해서 리트를 생성한다.
2. random.randrange() 함수는 범위가 비어 있을 때 ValueError를 발생시키므로, Tombola 인터페이스를 따르기 위해 ValueError를 잡고 대신 LookupError를 발생시킨다.
3. 그렇지 않으면 self._balls에서 무작위로 선택된 항목을 꺼낸다.
4. inspect()를 호출하지 않도록 loaded() 메서드를 오버라이드한다(아래 예제에서 Tombola.loaded가 그랬듯이). self._balls를 직접 이용하면 속도를 향상시킬 수 있다. 정렬된 튜플을 통째로 만들 필요 없다.
5. 한 줄짜리 코르도 insepct()를 오버라이드한다.

위 예제에는 설명할 필요가 있는 관용구가 있다. __init__() 메서드 안에서 self._balls는 iterable이 아니라 list(iterable)을 저장한다 (즉, self._balls에 단순히 iterable을 할당하지 않는다). 앞에서 설명한 것처럼, 이렇게 하면 어떠한 반복형이라도 LotteryBlower 클래스를 초기화할 수 있으므로 융통성이 향상된다. 이와 동시에 항목들을 리스트에 저장하므로 항목을 꺼낼 수 있도록 보장한다. 그리고 늘 iterable 인수로 리스트를 받지만 list(iteralbe)을 실행하면 인수의 사본이 생성된다. 우리 클래스가 인수로 받은 반복형에서 항목을 제거하며 이 클래스의 사용자는 전달한 리스트가 변경된다는 사실을 모를 수 있다는 점을 고려하면, 훌륭한 방법이다.

이제 구스 타이핑에서 가장 중요한 동적 기능인 register() 메서드를 이용해서 가상 서브클래스를 선언하는 방법에 대해 알아보자.

## Tombola의 가상 서브클래스
구스 타이핑의 본질적인 기능(그리고 물새 이름을 가질 수 있는 이유)은 어떤 클래스가 ABC를 상속하지 않더라도 그 클래스의 **가상 서브클래스**로 등록할 수 있다는 것이다. 이렇게 함으로써 이 클래스가 ABC에 정의된 인터페이스를 충실히 구현한다고 약속하는 것이다. 그리고 파이썬은 검사하지 않고 우리를 믿어준다. 그러나 우리가 거짓말을 하면 런타임 예외가 발생한다.

ABC의 register() 메서드를 호출하면 클래스가 등록된다. 등록된 클래스는 ABC의 가상 서브클래스가 되어 issubclass()와 isinstance()함수에 의해 인식되지만, ABC에서 상속한 메서드나 속성은 전혀 없다.
> 가상 서브클래스는 자신의 ABC에서 상속한 것이 아니며, 심지어 객체를 생성할 때도 ABC 인터페이스에 따르는지 검사받지 않는다. 런타임 오류를 피하기 위해 필요한 메서드를 실제로 모두 구현하는 것은 전적으로 서브클래스에 달려 있다.

일반적으로 register() 메서드는 평범한 함수처럼 호출되지만 (11.9절 'register()의 실제 용법' 참조), 데커레이터로 사용할 수도 있다. 아래 예제에서는 데커레이터 구문을 이용해서 아래 그림에 나온 Tombola 의 가상 서브클래스인 TomboList를 구현한다.

TomboList는 자신이 밝힌 대로 작동하며, 이것을 입증하는 doctset는 11.8절 'Tombola 서브클래스 테스트 방법'에서 설명한다.

![Tombola의 가상 서브클래스인 TomboList에 대한 UML 클래스 다이어그램](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/abstract_register.png)

- [tombolist.py Tombola의 가상 서브클래스 TomboList](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-6~7/tombolist.py)
1. TomboList를 Tombola의 가상 서브클래스로 등록한다.
2. TomboList는 list를 상속한다.
3. TomboList는 list에서 __bool__을 상속한다. 리스트가 비어 있지 않으면 True를 반환한다.
4. pick() 메서드는 무작위 인덱스를 전달해서 list에서 상속한 self.pop()을 호추랗ㄴ다.
5. lsit.extend() 메서드를 TomboList.load에 할당한다.
6. loaded() 메서드를 bool() 함수에 위임한다.
7. 파이썬 3.3 및 이전 버전에서는 register()를 클래스 데커레이터로 사용할 수 없다. 표준적인 호출 구문을 사용해야 한다.

TomboList를 Tombola 클래스의 가상 서브클래스로 등록했기 때문에 이제 issubclass()와 isinstacne()함수는 TomboList가 Tombola의 서브클래스인 것처럼 판단한다.

```
from tombola import Tombola
from tombolist import TomboList
issubclass(TomboList, Tombola)
# True
t = TomboList(range(100))
isinstance(t, Tombola)
# True
```
그러나 상속은 메서드 결정순서(MRO)를 담은 __mro__라는 특별 클래스 속성에 의해 운영된다. 이 속성은 기본적으로 파이썬이 메서드를 검색할 순서대로 자신과 자신의 슈퍼클래스들을 나열한다. TomboList의 __mro__를 조사해보면 이 클래스의 '진짜'슈퍼클래스인 list와 object만 들어있다.
```
TomboList.__mro__
# (<class 'tombolist.TomboList'>, <class 'list'>, <class 'object'>)
```
Tombola가 TomboList.__mro__에 들어 있지 않으므로 TomboList는 Tombola에서 아무런 메서드도 상속하지 않는다.

동일한 인터페이스를 구현하는 여러 클래스를 작성하면서, 모두 동일한 doctest로 테스트할 방법이 필요했다. 다음 절에서는 일반 클래스와 ABC의 API를 활용해서 클래스를 테스트하는 방법을 살펴본다.