<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-1/UML_class_diagram.png)
 -->
# 연산자 오버로딩: 제대로 하기
연산자 오버로딩은 사용자 정의 객체 +와 |같은 중위 연산자, -와 ~같은 단항 연산자를 사용할 수 있게 해준다. 파이썬에서는 여기에서 더 나아가 함수호출(()), 속성 접근(.), 항목 접근/ 슬라이싱([])도 연산자로 구현되어 있지만, 이 장에서는 단항 연산자와 중위 연산자만 다룬다.

1.2.1절 '수치형 흉내 내기'에서는 기본 Vector 클래스가 간단히 연산자를 구현하는 예를 보았다. [예제1-2](https://github.com/hyeonDD/fluent_python/blob/master/Part1/ex1-2/vector.py)의 __add__()와 __mul__() 메서드는 특별 메서드가 연산자 오버로딩을 지원하는 방법을 보여주기 위해 작성되었지만, 여기에는 우리가 간과한 미묘한 문제가 있다. 그리고 아래예제에서는 Vector2d.__eq__() 메서드가 Vector(3, 4) == [3, 4]를 참이라고 판단한다(이 방법이 옳을 수도 있고 아닐 수도 있다). 이런 문제를 이 장에서 다룬다.

이 장에서는 다음과 같은 내용을 설명한다.
* 파이썬이 다른 자료형의 피연산자로 중위 연산자를 지원하는 방법
* 다양한 자료형의 피연산자를 다루기 위한 덕 타이핑이나 명시적인 자료형 검사의 사용
* ==, >, <=등 향상된 비교 연산자의 별난 행동
* 피연산자를 처리할 수 없다고 중위 연산자 메서드가 알려주는 방법
* +=과 같은 계산 할당 연산자의 기본 처리 방식 및 오버로딩 방법

# 요약
이 장에서는 먼저 파이썬 연산자 오버로딩에서의 제한을 살펴보았다. 내장 자료형의 연산자는 오버로딩하지 말아야 하며, is, and, or, not을 제외한 기존 연산자만 오버로딩할 수 있다.

먼저 __neg__()과 __pos__() 메서드를 구현하면서 단항 연산자를 살펴보았으며, __add__() 메서드가 지원하는 + 중위 연산자를 살펴보았다. 이때 단항 연산자와 중위 연산자는 결코 피연산자를 변경하면 안 되며, 새로운 객체를 생성해서 결과를 반환해야 함을 보았다. 다른 자료형과의 연산을 지원할 때는 에외를 발생시키지 않고 NotImplemented 특별값을 반환함으로써 파이썬 인터프리터가 그 연산자의 역순 메서드 (즉, __radd__())를 호출해볼 수 있게 해줘야 한다. 파이썬이 중위 연산자를 처리하는 알고리즘은 [13-3]의 플로차트로 정리했다.

서로 다른 자료형의 피연산자를 혼합해서 사용하도록 허용하려면, 처리할 수 없는 자료형을 탐지해야 한다. 이 장에서는 덕 타이핑과 명시적인 자료형 검사 방법을 사용했다. 덕 타이핑은 일단 연산을 수행한 후 TypeError 예외가 발생하면 이 예외를 잡아서 처리한다. 명시적인 자료형 검사 방법은 isinstance() 함수를 사용하며, 나중에 __mul__() 메서드를 구현할 때 사용했다. 이 두 방법에는 장단점이 있다. 덕 타이핑은 융통성이 높지만, 명시적인 자료형 검사는 코드의 의도를 명확히 알 수 있다.

isinstance() 함수를 사용할 때는 구상 클래스가 아닌 추상 클래스를 이용해서 isinstance(scalar, numbers.Real)과 같이 검사했다. 추상 클래스를 사용하면 융통성과 안전을 적절히 보장할 수 있다. 11장에서 설명한 것처럼 기존 또는 향후 사용자가 정의한 자료형이 ABC의 실제 또는 가상 서브클래스로 선언될 수 있기 때문이다.

또한 향상된 비교 연산자의 오버로딩에 대해 살펴보았다. == 연산자는 __eq__() 메서드로 지원하며, 파이썬은 object 기저 클래스에서 상속한 __ne__() 메서드를 이용해서 != 연산자를 적절히 지원한다는 사실을 알게 되었따. 파이썬이 >, <, >=, <= 연산자를 평가할 때는 역순 메서드를 선택하는 논리가 약간 다르며, ==와 != 연산자의 경우에는 특별히 최종적인 수단으로 객체의 ID를 비교하므로 결코 에러가 발생하지 않는다.

마지막 부분에서는 복합 할당 연산자를 집중적으로 살펴보았다. 파이썬에서는 기본적으로 이들을 일반적인 연산자로 처리하고 나서 할당한다. 즉, a += b를 a = a + b로 평가한다. 이 방식은 새로운 객체를 생성하므로 가변이나 불변 자료형 모두에 사용할 수 있다. 가변 객체의 경우 += 연산자에 대한 __iadd__() 특별 메서드를 직접 구현함으로써(인플레이스) 왼쪽에 나오는 피 연산자의 값을 직접 변경할 수 있다. 예제로 구현해보기 위해 불변 객체인 Vector 클래스 대신 BingoCage 서브클래스를 구현했고, list 내장 자료형이 list.extend() 메서드를 이용해서 += 연산자를 지원하는 방식과 동일하게 += 연산자를 지원했다. 이 메서드를 구현하면서 + 연산자가 일반적으로 += 연산자에 비해 사용할 수 있는 피연산자의 종류에 더 엄격하다는 것을 설명했다. 일반적으로 + 연산자는 동일한 자료형의 객체 두 개를 요구하지만, += 연산자는 모든 반복형을 피연산자로 사용할 수 있다.