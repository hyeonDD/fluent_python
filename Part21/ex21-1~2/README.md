<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-1~2/ㅁ)
 -->
# 클래스 팩토리

이 책에서 이미 여러 번 봤지만, 표준 라이브러리에는 collections.namedtuple()이라는 클래스 팩토리가 있다. 이것은 일종의 함수로서, 클래스명과 속성명을 전달하면 이름으로 항목을 가져올 수 있게 해주고 디버깅하기 좋은 __repr__() 메서드를 제공하는 tuple의 서브클래스를 생성한다.

이따금 가변 객체에 이와 비슷한 팩토리가 있었으면 하는 때가 있었다. 예를 들어 지금 애완동물 가게용 애플리케이션을 만들고 있는데, 개에 대한 데이터를 간단한 레코드로 처리하고 싶다고 하자. 다음과 같은 식상한 코드는 좋지 않다.
```
class Dog:
    def __init__(self, name, weight, owner):
        self.name = name
        self.weight = weight
        self.owner = owner
```

따분하다. 똑같은 필드명이 세 번씩 나온다. 이렇게 따분한 코드는 repr()로 출력한 내용도 마으에 들지 않는다.
```
rex = Dog('Rex', 30, 'Bob')
rex
# <__main__.Dog object at 0x2865bac>
```

collections.namedtuple()에서 힌트를 얻어 Dog 같은 간단한 클래스를 즉석으로 생성하는 record_factory()를 만들어보자. 아래예제는 이 팩토리를 사용하는 예를 보여준다.
```
# 간단한 클래스 팩토리인 record_factory()의 테스트
    >>> Dog = record_factory('Dog', 'name weight owner')  # <1>
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex  # <2>
    Dog(name='Rex', weight=30, owner='Bob')
    >>> name, weight, _ = rex  # <3>
    >>> name, weight
    ('Rex', 30)
    >>> "{2}'s dog weighs {1}kg".format(*rex)  # <4>
    "Bob's dog weighs 30kg"
    >>> rex.weight = 32  # <5>
    >>> rex
    Dog(name='Rex', weight=32, owner='Bob')
    >>> Dog.__mro__  # <6>
    (<class 'factories.Dog'>, <class 'object'>)
```
1. 이 팩토리 함수의 시그너처는 namedtuple()의 시그너처와 비슷하게, 클래스명과 속성명을 공백이나 콤마로 구분해서 만든 문자열 하나를 받는다.
2. repr()도 멋지게 출력한다.
3. 객체를 반복할 수 있으므로 할당문에서도 간편하게 언패킹할 수 있다.
4. 그리고 format()과 같은 함수에도 쉽게 사용할 수 있다.
5. record 객체는 가변형이다.
6. 새로 생성된 클래스는 object를 상속하며, 팩토리와는 아무 관련이 없다.

아래 예제는 record_factory() 함수의 코드다.
- [factories.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-1~2/factories.py)
1. 실전 덕 타이핑. field_names를 콤마나 공백으로 분할하려고 시도한다. 실패하면, 이미 한 항목에 이름 하나씩 들어 잇는 반복형이다.
2. 속성명들의 튜플을 생성한다. 이 튜플은 새로운 클래스의 __slots__ 속성으로 사용하며, 언패킹과 __repr__()에 사용할 필드 순서도 설정한다.
3. 이 함수는 새로운 클래스의 __init__() 메서드가 된다. 위치 인수나 키워드 인수를 받는다.
4. __iter__() 메서드를 구현해서 클래스 객체를 반복형으로 만든다. __slots__에 들어 있는 순서대로 필드값을 생성한다.
5. __slots__와 self를 반복해서 멋지게 출력하는 __repr__() 메서드를 정의한다.
6. 클래스 속성의 딕셔너리를 조합한다.
7. type() 생성자를 호출해서 새로운 클래스를 생성하고 반환한다.

type(my_obejct)를 이용해서 객체의 클래스와 동일한 my_object.__class__를 가져오므로, type()을 일종의 함수로 생각하기 쉽다. 그러나 type()은 클래스다. 다음과 같이 인수 세 개를 받아서 호출하면 새로운 클래스를 생성하는 일종의 클래스처럼 작동한다.
```
MyClass = type('MyClass', (MySuperClass, MyMixin),
                {'x': 42, 'x2': lambda self: self.x *2})
```
type()에 전달하는 세 인수의 이름은 name, bases, dict며, 이때 dict는 새로운 클래스의 속성명과 속성의 매핑이다. 위 코드는 기능상으로 다음 코드와 동일하다.
```
class MyClass(MySuperClass, MyMixin):
    x = 42

    def x2(self):
        return self.x * 2
```

특이한 점은 여기에 나온 MyClass나 위 부분의 record_factory() 테스트 에서의 Dog처럼 type의 객체가 클래스라는 것이다.

정리하면, [factories.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-1~2/factories.py) record_factory의 마지막 행은 cls_name 값을 이름으로 사용하고, object를 단 하나의 직속 슈퍼클래스로 사용하며, __slots__, __init__(), __iter__(), __repr__() 클래스 속성을 가진 하나의 클래스를 생성한다. 이때 __init__(), __iter__(), __repr__()은 객체 메서드다.

__slots__ 클래스 속성의 이름은 다른 이름으로 할 수도 있었지만, 그러면 할당할 속성명을 검증하기 위해 __setattr__() 메서드를 구현해야 한다. record 같은 클래스의 경우 속성들의 이름이 언제나 동일하고 같은 순서로 되어 있어야 하기 때문이다. __slots__를 사용하면 수백만 객체를 사용할 때 메모리를 절약하는 특징이 있지만, 9.8절 '__slots__ 클래스 속성으로 공간 절약하기'에서 설명한 단점도 있다.

클래스를 동적으로 생성하기 위해 일반적으로 인수 세 개를 전달해서 type()을 호출한다. collections.namedtuple() 소스 코드 (http://bit.ly/1HGwxRl) 에서는 다른 방법을 사용한다. 하나의 문자열로 되어 있는 소스 코드 템플릿 _class_template과 namedtuple() 함수가 _class_template.format()을 호출해서 빈 칸을 채운다. 그러고 나서 exec() 내장 함수를 이용해서 생성된 소스 코드 문자열을 평가한다.

record_factory()로 생성한 클래스의 객체들은 직렬화할 할 수 없다는 제한이 있다. 즉, pickle 모듈의 dump(), load() 함수와 함께 사용할 수 없다. 이 절의 목표는 간단한 사례에서 type 클래스의 사용법을 보여주는 것이므로, 이 문제를 해결하는 것은 이 예제의 범위를 벗어난다. 직렬화 문제를 해결하려면 collections.namedtuple 소스 코드 (http://bit.ly/1HGwxRl) 에서 'pickle'을 검색해서 연구하기 바란다.
> 파이썬에서 메타프로그래밍을 할 때는 exec()나 eval()을 피하는 것이 좋다. 이 함수들이 신뢰할 수 없는 곳에서 가져온 문자열을 전달하면 심각한 보안 위험이 발생할 수 있다. 파이썬은 내부 조사를 할 수 있는 도구를 충분히 제공하므로, 대부분의 경우 exec()와 eval()을 사용할 필요가 없다. 그러나 파이썬 핵심 개발자는 nametuple()을 구현할 때 exec()를 사용하기로 결정했다. 이 방법은 클래스를 생성하기 위해 만들어진 코드를 _source 속성 (http://bit.ly/1HGwAfW) 을 통해 확인할 수 있게 해준다.

# 디스크립터를 커스터마이즈하기 위한 클래스 데커레이터

20.1.3절 'LineItem 버전 #5: 새로운 디스크립터형'에서는 알아보기 쉬운 저장소명을 사용하는 문제를 남겨둔 채 LineItem 예제를 마쳤다. weight 값이 _Quantity#0이라는 이름의 객체 속성에 저장되어 있어서 디바깅하기 힘든 상태다. 다음 명령을 이용하면 [bulkfood_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v5.py)의 디스크립터에서 저장소명을 가져올 수 있다.
```
LineItem.weight.storage_name
# '_Quantity#0'
```
그러나 저장소명이 다음과 같이 실제 관리 대상 속성의 이름을 포함하고 있으면 더 좋을 것이다.
```
LineItem.weight.storage_name
# '_quantity#weight'
```
20.1.2절 'LineItem 버전 #4: 자동 저장소 속성명'에서 설명한 것처럼 디스크립터 객체가 생성될 때는 관리 대상 속성(디스크립터 객체가 바인딩될 클래스 속성으로서, LineItem 예제에서 weight 등의 속성)의 이름을 알 수 없기 때문에 알아보기 쉬운 저장소명을 사용할 수 없었다. 그러나 일단 전체 클래스가 만들어지고 디스크립터 객체가 클래스 속성에 바인딩된 후에는, 클래스를 조사하고 디스크립터에 적절한 저장ㅅ오명을 설정할 수 있다. LineItem 클래스의 __new__() 메서드에서 이 작업을 수행할 수 있으므로, __init__() 메서드 안에서 디스크립터를 사용할 때가 되면, 이미 올바른 저장소명이 설정되어 있다. 그러나 이런 용도로 __new__()를 사용하면 컴퓨터 자원을 낭비하는 문제가 있다. LineItem 클래스 자체가 만들어진 후에는 디스크립터 객체와 관리 대상 속성 간의 바인딩은 변하지 않지만, __new__()의 논리는 LineItem객체가 생성될 때마다 실행되기 때문이다. 그러므로 클래스를 생성할 때 저장소명을 설정해야한다. 바로 이 작업을 클래스 데커레이터나 메타클래스를 이용해서 처리할 수 있다. 먼저 간단한 것부터 만들어보자.

클래스 데커레이터는 함수 데커레이터와 아주 비슷하다. 클래스를 받아서 동일하거나 수정된 클래스를 반환한다.

아래 bulkfood_v6.py에서 LineItem 클래스는 인터프리터에 의해 평가되어 생성된 클래스 객체가 model.entity() 함수에 전달된다. 파이썬은 model.entity()가 반환하는 것을 전역 명칭인 LineItem에 할당한다. 이 예제에서 model.entity()는 LineItem 클래스 안에 있는 각 디스크립터 객체의 storage_name 속성을 변경해서 반환한다.

- [bulkfood_v6.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-1~2/bulkfood_v6.py)
1. 이 클래스는 데커레이터가 추가되었다는 점 외에는 그대로다.

아래 예제는 데커레이터의 소스 코드다. model_v6.py의 끝부분에 추가된 코드만 여기에 나열한다. 나머지 코드는 model_v5.py와 동일하다.
```
def entity(cls):  # <1>
    for key, attr in cls.__dict__.items():  # <2>
        if isinstance(attr, Validated):  # <3>
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)  # <4>
    return cls  # <5>
```
1. 데커레이터는 클래스를 인수로 받는다.
2. 클래스의 속성을 담고 있는 딕셔너리를 반복한다.
3. 속성이 Validated 디스크립터 클래스인지 확인한다. 만일 그렇다면
4. 디스크립터 클래스명과 관리 대상 속성명을 사용하기 위해 storage_name을 설정한다 (예를 들면 _NonBlank#description).
5. 변경된 클래스를 반환한다.

blukfood_v6.py에 들어 있는 doctest는 수정한 코드가 제대로 작동함을 입증한다. 아래 예제는 LineItem 객체의 저장소 속성명을 보여준다.
```
    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)[:3]
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> LineItem.description.storage_name
    '_NonBlank#description'
    >>> raisins.description
    'Golden raisins'
    >>> getattr(raisins, '_NonBlank#description')
    'Golden raisins'
```
그리 복잡하지 않다. 클래스 데커레이터를 사용하면 이전에는 메타클래스를 사용해야 했던 작업(클래스가 생성되는 순간 클래스의 커스터마이즈)을 더 간단히 수행할 수 있다.

그러나 클래스 데커레이터는 자신에게 직접 인용된 클래스에서만 작동할 수 있다는 커다란 단점이 있다. 즉, 장식된 클래스의 변경된 내용에 따라 서브클래스가 변경된 내용을 상속할 수도 아닐 수도 있다. 다음 절에서는 이 문제를 알아보고, 이 문제의 해결책도 살펴본다.

