<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-2/UML_class_diagram.png)
 -->
# 오버라이딩 디스크립터와 논오버라이딩 디스크립터

파이썬이 속성을 처리하는 방식에는 커다란 비대칭성이 있음을 주의하라. 일반적으로 객체를 통해 속성을 읽으면 객체에 정의된 속성을 반환하지만, 객체에 그 속성이 없으면 클래스 속성을 읽는다. 한편 일반적으로 객체의 속성에 값을 할당하면 객체 안에 그 속성을 만들고 클래스에는 전혀 영향을 미치지 않는다.

이런 비대칭성은 디스크립터에도 영향을 미쳐, __set__() 메서드의 정의 여부에 따라 두 가지 범주의 디스크립터를 생성한다. 서로 다른 작동 방식을 관찰하려면 몇 가지 클래스가 필요하므로, 이제부터는 아래 descriptorkinds.py을 테스트베드로 사용해서 디스크립터의 작동을 살펴본다.

> descriptorkinds.py의 모든 __get__()과 __set__() 메서드는 print_args()를 호출하므로, 호출될떄 받은 인수를 보기 좋게 출력한다. print_args()와 보조 함수 cls_name()및 display()를 이해하는 것은 중요하지 않으므로, 이 함수들에 주의를 빼앗기지 않도록 하자.

- [descriptorkinds.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-2/descriptorkinds.py)
1. __get__()과 __set__() 메서드를 가진 전형적인 오버라이딩 디스크립터 클래스
2. 이 예제에서는 모든 디스크립트 메서드에서 print_args()함수를 호출한다.
3. __get__() 메서드가 없는 오버라이딩 디스크립터 클래스
4. 이 클래스에는 __set__() 메서드가 없으므로, 논오버라이딩 디스크립터다.
5. 각 디스크립터 클래스의 객체를 하나씩 사용하는 관리 대상 클래스
6. 메서드가 디스크립터이기도 하므로, 비교하기 위해 spam() 메서드를 추가한다.

다음 절에서는 Managed 클래스와 관련된 속성을 읽고 쓰는 과정을 살펴보면서, 각기 다른 디스크립터에 대해 자세히 알아본다.

## 오버라이딩 디스크립터

__set__() 메서드를 구현하는 디스크립터를 **오버라이딩 디스크립터**라고 한다. 비록 클래스 속성이기는 하지만, __set__() 메서드를 구현하는 디스크립터는 객체 속성에 할당하려는 시도를 가로채기 때문이다. 이 방법은 [bulkfood_v4.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v4.py)의 코드에 사용되었다. 프로퍼티도 오버라이딩 디스크립터라고 할 수 있다. 세터 함수를 제공하지 않더라도, property 클래스에서 기본적으로 제공하는 __set__() 메서드가 읽기 전용 속성임을 알려주기 위해 AtributeError를 발생시킨다. 위 descriptorkinds.py의 코드를 이용해서 오버라이딩 디스크립터를 실험한 결과는 아래와 같다.

```
    >>> obj = Managed()  # <1>
    >>> obj.over  # <2>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over  # <3>
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7  # <4>
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over  # <5>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> obj.__dict__['over'] = 8  # <6>
    >>> vars(obj)  # <7>
    {'over': 8}
    >>> obj.over  # <8>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
```
1. 테스트하기 위해 Managed 객체를 생성한다.
2. obj.over는 관리 대상 객체인 obj를 두 번째 인수로 전달해서 디스크립터의 __get__() 메서드를 호출한다.
3. Managed.over는 두 번째 인수(instance)로 None을 전달해서 디스크립터의 __get__() 메서드를 호출한다.
4. obj.over에 값을 할당하면 값(7)을 마지막 인수로 전달해서 __set__() 메서드를 호출한다.
5. obj.over를 읽으면 여전히 디스크립터의 __get__() 메서드를 호출한다.
6. 디스크립터를 우회해서 obj.__dict__에 직접 값을 설정한다.
7. obj.__dict__의 over 키에 값이 들어 있는지 확인한다.
8. 그러나 obj.over라는 객체 속성을 읽을 때는 여전히 Managed.over 디스크립터가 개입해서 처리한다.

## __get__()이 없는 오버라이딩 디스크립터

일반적으로 오버라이딩 디스크립터는 __set__()과 __get__() 메서드를 모두 구현하지만, [bulkfood_v3.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v3.py)에서 본 것처럼 __set__() 메서드만 오버라이드할 수도 있다. 이때는 저장 연산만 디스크립터가 처리한다. 객체를 통해 디스크립터를 확인해보면 읽기 접근을 처리하는 __get__()메서드가 없으므로 디스크립터 객체 자체가 반환된다. 객체의 __dict__에 직접 접근해서 새로운 값을 가진 동일한 이름의 객체 속성을 생성하더라도, 이후의 쓰기 접근은 __set__() 메서드가 가로채지만, 그 속성을 읽을 때는 디스크립터 객체가 아니라 새로운 값을 그대로 반환한다. 즉, 읽기 연산의 경우에만 객체 속성이 디스크립터를 가린다. 아래예제를 보자.

```
    >>> obj.over_no_get  # doctest: +ELLIPSIS #1
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Managed.over_no_get  # doctest: +ELLIPSIS #2
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7 #3
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # doctest: +ELLIPSIS #4
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.__dict__['over_no_get'] = 9 #5
    >>> obj.over_no_get #6
    9
    >>> obj.over_no_get = 7 #7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get #8
    9
```
1. 이 오버라이딩 디스크립터에는 __get__() 메서드가 정의되어 있지 않으므로, obj.over_no_get을 읽으면 클래스의 디스크립터 객체 자체가 반환된다.
2. 관리 대상 클래스를 통해 디스크립터 객체를 읽을 때도 마찬가지다.
3. obj.over_no_get에 설정하면 __set__() 디스크립터 메서드가 호출된다.
4. 여기에서 구현한 __set__() 메서드는 값을 변경하지 않으므로, obj.over_no_get을 다시 읽을 때 여전히 관리 대상 클래스의 디스크립터 객체가 반환된다.
5. 객체의 __dict__를 통해 over_no_get이라는 객체 속성을 설정한다.
6. 이제 over_no_get 객체 속성이 디스크립터를 가리지만, 읽기 연산만 가린다.
7. obj.over_no_get에 값을 할당하려고 하면 여전히 디스크립터의 __set__() 메서드를 거친다.
8. 그러나 읽기 연산의 경우 동일한 이름의 객체 속성이 있으므로 디스크립터가 가려진다.

## 논오버라이딩 디스크립터

디스크립터가 __set__() 메서드를 구현하지 않으면 논오버라이딩 디스크립터가 된다. 동일한 이름의 객체 속성을 설정하면 디스크립터를 가리므로, 그 객체에는 디스크립터가 작동하지 않는다. 메서드는 논오버라이딩 디스크립터로 구현된다. 아래예제는 논오버라이딩 디스크립터의 작동을 보여준다.

```
    >>> obj = Managed()
    >>> obj.non_over  # <1>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7  # <2>
    >>> obj.non_over  # <3>
    7
    >>> Managed.non_over  # <4>
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    >>> del obj.non_over  # <5>
    >>> obj.non_over  # <6>
```
1. obj.non_over를 읽을 때 obj를 두 번째 인수로 전달해서 디스크립터의 __get__() 메서드를 호출한다.
2. Managed.non_over는 논오버라이딩 디스크립터이므로, 할당에 개입하는 __set__() 메서드가 없다.
3. 이제 obj 에는 non_over라는 객체 속성이 생겼으므로, 이 속성이 managed 클래스에 있는 동일한 이름의 디스크립터 속성을 가린다.
4. Managed.non_over 디스크립터가 여전히 존재하므로, 읽기 연산을 가로챈다.
5. non_over 객체 속성을 제거한다.
6. 그러면 obj.non_over를 읽을 때 클래스 안에 있는 디스크립터의 __get__() 메서드가 호출된다. 여기서는 객체를 통해 접근하므로 두 번째 인수가 관리 대상 객체임에 주의하라.

> 이 개념을 설명할 때 파이썬 개발 참여자와 프로그래머는 서로 다른 용어를 사용한다. 오버라이딩 디스크립터는 데이터 디스크립터 혹은 강제 디스크립터라고도 한다. 논오버라이딩 디스크립터는 비데이터 디스크립터 혹은 가릴 수 있는 디스크립터라고도 한다.

앞에 나온 여러 예제에서, 디스크립터와 동일한 이름을 가진 객체 속성에 값을 할당하는 여러 연산이 디스크립터의 __set__() 메서드 존재 여부에 따라 결과가 달라짐을 알 수 있다.

클래스 안의 속성을 설정하는 것은 이 클래스에 연결된 디스크립터가 통제할 수 없다. 특히 다음 절에서 설명하는 것처럼 클래스 속성에 값을 할당함으로써 디스크립터 객체 자신이 무용지물이 될 수도 있따.

## 클래스 안에서 디스크립터 덮어쓰기

오버라이딩 디스크립터든 논오버라이딩 디스크립터든 클래스의 속성에 값을 핟ㄹ당하면 덮어써진다. 이런 기법을 멍키 패칭이라고 부르지만, 아래예제에서는 디스크립터가 정수로 바뀌므로, 제대로 작동하기 위해 디스크립터에 의존하는 모든 클래스를 사실살 무용지물로 만든다.
```
# 어떠한 디스크립터도 클래스 자체를 이용하면 덮어쓸 수 있다.
obj = Managed() #1
Managed.over = 1 #2
Managed.over_no_get = 2
Managed.non_over = 3
obj.over, obj.over_no_get, obj.non_over #3
# (1,2,3)
```
1. 나중에 테스트하기 위해 객체를 새로 생성한다.
2. 클래스에서 디스크립터 객체를 담은 속성을 덮어쓴다.
3. 실제로 디스크립터가 사라져버렸다.

위 예제는 속성의 읽기와 쓰기에 관련된 또 다른 비대칭성을 보여준다. 클래스 속성을 읽는 것은 관리 대상 클래스에 연결된 디스크립터의 __get__() 메서드에 의해 통제되지만, 클래스 속성에 쓰는 연산은 관리 대상 클래스에 연결된 디스크립터의 __set__() 메서드가 통제할 수 없다.
> 클래스 속성에 저장하는 연산을 통제하려면 클래스의 클래스(즉, 메타클래스)에 디스크립터를 연결해야 한다. 기본적으로 사용자 정의 클래스의 메타클래스는 type이며, type에는 속성을 추가할 수 없다. 21장에서는 메타클래스를 직접 만들어본다.

이제 파이썬에서 메서드를 구현하기 위해 디스크립터를 사용하는 방법을 알아보자.