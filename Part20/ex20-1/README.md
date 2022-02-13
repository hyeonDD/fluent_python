<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/UML_class_diagram.png)
 -->
# 디스크립터 예: 속성 검증

19.4절 '프로퍼티 팩토리 구현하기'에서 설명한 것처럼, 프로퍼티 팩토리를 사용하면 함수형 프로그래밍 스타일을 적용함으로써 똑같은 게터와 세터를 반복해서 구현할 필요가 없다. 프로퍼티 함수는 고위 함수로서 일련의 접근자 함수를 매개변수화하고 storage_name과 같은 환경변수를 클로저에 담아서 사용자 정의 프로퍼티 객체를 생성한다. 이와 동일한 문제를 객체지향 방식으로 해결한 것이 디스크립터 클래스다.

여기서는 19.4절 '프로퍼티 팩토리 구현하기'의 LineItem 에제를 이용해서 quantity()프로퍼티 팩토를 Quantity 디스크립터 클래스로 리팩토링한다.

## LineItem 버전 #3: 간단한 디스크립터
__get__(), __set__(), __delet__() 메서드를 구현하는 클래스가 디스크립터다. 디스크립터는 클래스의 객체를 다른 클래스의 속성으로 정의해서 사용한다.

우리는 Quantity 디스크립터 클래스를 생성하고, LineItem 클래스는 두 개의 Quantity 객체를 사용할 것이다. 하나는 weight 속성을, 다른 하나는 price 속성을 관리하기 위해 사용한다.
그림으로 보면 이해하기 쉬우니 아래 그림을 보자.

![quantity_descriptor.png](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/quantity_descriptor.png)

위 그림에 weight라는 둔어가 두 번 나옴에 주의하라. 실제로 weight라는 이름의 두 개의 속성이 따로 존재한다. 하나는 LineItem의 클래스 속성이며, 다른 하나는 LineItem 객체에 존재하는 객체 속성이다. 이것은 price에더 적용된다.

먼저 다음과 같이 용어를 정의하고 나서, 설명을 진행한다.

---

**디스크립터 클래스**
디스크립터 프로토콜을 구현하는 클래스, 아래 예제의 Quantity 클래스가 디스크립터 클래스다.

**관리 대상 클래스**
디스크립터 객체를 클래스 속성으로 선언하는 클래스, 아래예제의 LineItem 클래스가 관리대상 클래스다.

**디스크립터 객체**
관리 대상 클래스의 클래스 속성으로 선언된, 디스크르립터 클래스의 객체. 위 그림에서의 각각의 디스크립터 객체는 밑줄 친 이름을 가진 구성 화살표로 표현된다(UML에서 밑줄 친 속성은 클래스 속성을 나타낸다). 디스크립터 객체를 가진 LineItem 클래스 쪽에 검은 마름모가 온다.

**관리 대상 객체**
관리 대상 클래스의 객체. 이 예제에서는 LineItem 클래스의 객체들이 관리 대상 객체가 된다(클래스 다이어그램에는 나타나 있지 않다).

**저장소 속성**
관리 대상 객체 안의 관리 대상 속성값을 담을 속성. 위 그림에서 LineItem 객체의 weight와 price 속성이 저장소 속성이다. 이들은 디스크립터 객체와는 별개의 속성으로, 항상 클래스 속성이다.

**관리 대상 속성**
디스크립터 객체에 의해 관리되는 관리 대상 클래스 안의 공개 속성으로, 이 속성의 값은 저장소 속성에 저장된다. 즉, 디스크립터 객체와 저장소 속성이 관리 대상 속성에 대한 기반을 제공한다.

---

Quantity 객체는 LineItem의 클래스 속성이라는 점을 명심해야 한다. 아래그림에 공장과 장치 표기법(MGN)을 이용해서 이 점을 강조했다.

![MGN.png](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/MGN.png)

---

**_ 공장과 장치 표기법 소개 _**

디스크립터에 대한 설명을 자주 하다 보니 UML은 관리 대상 클래스와 디스크립터 객체 간의 관계처럼 클래스와 객체 간의 관계를 표현하기에 별로 좋지 않다는 것을 깨달았다. 그래서 필자는 UML 다이어그램에 설명을 붙이기 위해 사용할 수 있는 MGN(공장과 장치 표기법)이라는 나만의 '언어'를 만들어냈다.

MGN은 클래스와 객체를 아주 분명히 구분하기 위해 만들어졌다. MGN에서 클래스는 장치를 생상하는 복잡한 기계인 '공장'으로 나타난다. 클래스/공장은 다양한 조작 장치를 가진 기계다. 장치는 객체로서, 훨씬 더 간단하다. 장치는 자신을 생상한 공장과 동일한 색상이다.

이 예제에서 LineItem 객체는 세 개의 속성 (설명, 무게, 가격)을 표현하기 위해 세 개의 셀을 가진 한 줄의 표로 그렸다. 디스크립터인 Quantity 객체는 값을 가져와서 살펴보는 __get__()이라는 돋보기와 값을 설정하는 __set__()이라는 집게가 있다. 메타클래스에 대해 설명할 때, 이런 그림을 고안해내 필자에게 감사할 것이다.

---

그림은 충분히 본 것 같다. 이제 코드를 살펴보자. 위그림은 Quantity 클래스 및 두 개의 Quantity 객체를 사용하는 새로운 LineItem 클래스를 보여준다.
- [bulkfood_v3.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v3.py)
1. 디스크립터는  프로토콜에 기반한 기능이다. 구현하기 위해 상속할 필요가 없다.
2. 각각의 Quantity 객체는 storage_name 속성을 가진다. 이것이 바로 관리 대상 객체에서 값을 보관할 속성의 이름이다.
3. 관리 대상 속성에 값을 할당할 때 __set__()이 호출된다. 여기서 self는 디스크립터 객체(즉, lineItem.weight나 LineItem.price), instance는 관리 대상 객체(LineItem 객체), value는 할당할 값이다.
4. 이겨시너는 관리 대상 객체의 __dict__를 직접 처리해야 한다. setattr() 내장 함수를 사용하면 또 다시 __set__() 메서드가 호출되어, 무한 재귀가 된다.
5. 첫 번째 디스크립터 객체는 weight 속성에 바인딩된다.
6. 두 번째 디스크립터 객체는 price 속성에 바인딩된다.
7. 나머지 코드는 [bulkfood_v1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-2/bulkfood_v1.py)의 원래 bulkfood_v1.py 코드만큼 간단하고 깔끔하다.

bulkfood_v3.py에서 각각의 관리 대상 속성은 저장소 속성과 이름이 똑같으며, 별도의 게터 논리를 구현할 필요가 없으므로 Quantity 클래스에 __get__() 메서드가 필요 없다.

bulkfood_v3.py에서 구현한 클래스는 다음과 같이 의도한 대로 작동하며, 화이트 트러플(흰색 송로 버섯)을 0달러에 파는 것을 방지한다.
```
truffle = LineItem('White truffle', 100, 0)
"""
Traceback (most call last):
 ...
ValueError: value must be > 0
"""
```
> __set__() 메서드를 구현할 때 self와 instance 인수가 의미하는 것에 주의해야 한다. self는 디스크립터 객체, instance는 관리 대상 객체다. 객체 속성을 관리하는 디스크립터는 값을 관리 대상 객체에 저장해야 한다. 그렇기 때문에 파이썬이 instance 인수를 디스크립터 메서드에 제공하는 것이다.

각각의 관리 대상 속성을 디스크립터 객체 자체에 저장하고 싶은 생각이 들 수 있지만, 이것은 잘못된 방법이다. 예를 들어 다음과 같은 코드가 있다고 하자.

```
instacne.__dict__[self.storage_name] = value
```

이 코드를 다음과 같이 바꾸고 싶은 생각이 들 수도 있다.

```
self.__dict__[self.storage_name] = value
```

그러나 이 코드는 잘못되었다. 잘못된 이유를 이해하려면 __set__()에 전달되는 앞의 두 인수 self와 instance의 의미에 대해 생각해보라. 여기서 self는 디스크립터 객체로서, 관리 대상 클래스의 클래스 속성이다. 메모리에 수천 개의 LineItem 객체가 있더라도 디스크립터 객체는 LineItem.weight와 LineItem.price, 단 두 개밖에 없다. 따라서 디스크립터 객체에 저장하는 모든 것은 LineItem 클래스 속성이 되어, 모든 LineItem 객체가 공유한다.

bulkfood_v3.py의 단점은 관리 대상 클래스 본체에 디스크립터 객체를 생성할 때 속성명을 반복해야 한다는 것이다. LineItem 클래스를 다음과 같이 선언할 수 있다면 훨씬 더 좋을 것이다.

```
class LineItem:
    weight = Quantity()
    price = Qunatity()

    # 나머지 메서드는 이전과 동일하다.
```
8장에서 설명한 것처럼, 문제는 변수가 존재하기도 전에 할당문의 오른쪽이 실행된다는 것이다. 디스크립터 객체를 생성하기 위해 Quantity() 표현식이 평가되는데, 이때 Quantity 클래스 안에 있는 코드에서는 디스크립터 객체를 어떤 이름의 변수(예를 들면 weight 또는 price)에 바인딩해야 할지 알 수 없다는 것이다.

bulkfood_v3.py 코드 상태로는 각각의 Quantity 객체에 속성명을 명시적으로 지정할 수 밖에 없다. 이는 불편할 뿐만 아니라 위험하기도 하다. 프로그래머가 코드를 복사해서 붙여 넣고 변수명을 바꾸지 않아서, price = Quantity('weight')와 같이 되어 있다고 해보자. 이 프로그램은 엉뚱하게도 price의 값을 설정할 때마다 weight의 값을 변경한다.

이름 반복 문제에 대한 그리 멋지지는 않지만 쓸 만한 해결책을 다음 절에서 소개한다. 더 좋은 해결책은 클래스 데커레이터나 메타클래스가 필요하므로 21장에서 설명한다.

## LineItem 버전 #4: 자동 저장소 속성명
디스크립터를 선언할 때 속성명을 반복 입력하지 않기 위해 각 Quantity 객체의 storage_name에 대한 고유한 문자열을 생성할 것이다. 아래 그림은 Quantity와 LineItem 클래스에 대한 새로운 UML 다이어그램을 보여준다.

![quantity_descriptor2.png](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/quantity_descriptor2.png)

storage_name을 생성하기 위해 '_Quantity#' 문자열 뒤에 정수를 연결한다. 새로운 Quality 디스크립터 객체가 클래스에 연결될 때마다 Quantity.__counter 클래스 속성의 값이 증가한다. 해시 기호 (#)를 사용하면 storage_name이 사용자가 점 표기법으로 생성한 속성과 충돌되지 않도록 보장할 수 있다. nutmeg._Quantity#0은 올바른 파이썬 문법이 아니기 때문이다. 그러나 우리는 getattr()과 setattr() 내장 함수를 사용하거나 직접 객체의 __dict__를 건드려서 '잘못된' 식별자 속성의 값을 가져오거나 저장할 수 있다. 아래 bulkfood_v4.py는 새로 구현한 코드를 보여준다.

- [bulkfood_v4.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v4.py)
1. __counter는 Quantity의 클래스 속성으로서, Quantity 객체의 수를 센다.
2. cls는 Quality 클래스에 대한 참조다.
3. 각 디스크립터 객체에 대한 storage_name은 디스크립터 클래스명과 현재 __counter 값으로 만들어지므로(예를 들면 _Quantity#0), 고유한 값을 가진다.
4. __counter를 증가시킨다.
5. 관리 대상 속성의 이름이 storage_name과 동일하지 않으므로, __get__() 메서드를 구현해야 한다. owner 인수는 잠시 후에 설명한다.
6. instance에서 value 값을 가져오기 위해 getattr() 내장 함수를 사용한다.
7. instance 안에 값을 저장하기 위해 setattr() 내장 함수를 사용한다.
8. 이제는 Quantity 생성자에 관리 대상 속성명을 전달하지 않아도 된다. 이것이 이 버전의 목표다.

여기서는 instance.__dict__ 대신 고수준 getattr()과 setattr() 내장 함수를 이용해서 값을 저장할 수 있었다. 관리 대상 속성과 저장소 속성의 이름이 다르기 때문에 저장소 속성에 getattr()을 호출하더라도 디스크립터를 실행하지 않으므로, bulkfood_v3.py에서 설명한 무한재귀가 발생하지 않는다.

bulkfood_v4.py를 테스트해보면 weight와 price 디스크립터가 예상한 대로 작동하며, 저장소 속성을 직접 읽을 수 있으므로 디버깅할 때 유용하게 사용할 수 있다.
```
from bulkfood_v4 import LineItem
coconuts = LineItem('Brazilian coconut', 20, 17.95)
coconuts.weight, coconuts.price
# (20, 17.95)
getattr(coconuts, '_Quantity#0'), getattr(coconuts, '_Quantity#1')
# (20, 17.95)
```
> _LineItem__quantity0처럼 이름을 장식하기 위해 파이썬이 사용하는 관례를 따르고 싶다면, 관리 대상 클래스(즉, LineItem)의 이름을 알아야 한다. 그러나 클래스를 정의하는 코드는 클래스 자체가 만들어지기 전에 실행되므로, 디스크립터 객체를 생성할 때는 클래스에 대한 정보를 가져올 수 없다. 그러나 Quantity 디스크립터의 경우에는 서브클래스를 실수로 덮어쓰는 문제를 피하기 위해 관리 대상 클래스명을 포함할 필요가 없다. 디스크립터 객체가 생성될 때마다 디스크립터 클래스의 __counter가 증가하므로, Quantity 디스크립터가 관리하는 모든 클래스에서 저장소명이 겹치지 않음을 보장할 수 있다.

__get__() 메서드는 self, instance, owner 등 3개의 인수를 받는다. onwer 인수는 관리 대상 클래스(즉, LineItem)에 대한 참조며, 디스크립터를 이용해서 클래스의 속성을 가져올 때 유용하게 사용할 수 있다. LineItem.weight처럼 클래스에서 관리 대상 속성(weight)을 가져올때는 디스크립터 __get__()메서드가 instance 인수값으로 None을 받는다. 이제 다음 콘솔세션에서 AttributeError가 발생하는 이유를 알 수 있을 것이다.

```
from bulkfood_v4 import LineItem
LineItem.weight
"""
Traceback (most recent call last):
 ...
 File ".../descriptors/blukfood_v4.py", Line 54, in __get__
    return getattr(instance, self.storage_name)
AttributeError: 'NoneType' object has no attribute '_Quantity#0'
"""
```

__get__()을 구현할 때 AttributeError를 발생시켜도 무방하지만, 이 예외를 발생시키는 경우에는 NoneType과 _Quantity#0 등 내부 구현에 관련된 혼란스러운 메시지는 삭제해야 한다. ''LineItem' calss has no such attribute'정도가 적절할 것이다. 찾을 수 없는 속성명을 알려주면 금상첨화지만, 이 예제에서는 디스크립터가 관리 대상 속성명을 모르므로, 이 이상은 할 수 없다.

한편 사용자가 내부 조사나 여타 메타프로그래밍 기법을 사용할 수 있도록 지원하려면, 클래스를 통해 관리 대상 속성에 접근할 때 __get__() 메서드가 디스크립터 객체를 반환하게 하는 것이 좋다. bulkfood_v4b.py은 bulkfood_v4.py의 Quantity.__get__()에 약간의 논리를 추가해서 조금 변형한 버전이다.

```
class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self  # <1>
        else:
            return getattr(instance, self.storage_name)  # <2>

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')
```
1. 객체를 통해 호출하지 않으면 디스크립터 자신을 반환한다.
2. 그렇지 않으면 하던 대로 관리 대상 속성을 반환한다.

bulkfood_v4b.py의 클래스를 테스트해보면 다음과 같다.
```
from bulkfood_v4b import LineItem
LineItem.price
# <bulkfood_v4b.Quantity object at 0x100721be0>
br_nuts = LineItem('Brazil nuts', 10, 34.95)
br_nuts.price
# 34.95
```
bulkfood_v4b.py를 보면서 단지 속성 두 개를 관리하기 위해 너무 많이 코딩하는 게 아닌가 하는 생각이 들 수도 있지만, 이제는 디스크립터 논리가 별도의 코드인 Quantity 클래스에 들어 있음을 알아야 한다. 일반적으로 프레임워크를 개발하는 경우에는, 사용할 곳에 디스크립터를 바로 정의하지 않고, 여러 애플리케이션에서 사용할 수 있도록 볃로의 모듈에 정의한다.

bulkfood_v4c.py는 디스크립터를 별도의 모듈에 정의해서 사용하는 전형적인 모습을 보여준다.
- [bulkfood_v4c.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v4c.py)
1. model_v3c 모듈을 임포트하고, 더 편안한 이름을 부여한다.
2. model.Quantity를 사용한다.

장고 사용자라면 bulkfood_v4c.py의 코드가 모델 정의와 비슷하다는 생각이 들었을 것이다. 당연하다. 장고의 모델 필드가 디스크립터기 때문이다.
> 지금까지 구현한 Quantity 디스터는 아주 잘 작동한다. 단점이 하나 있다면, _Quantity#0과 같은 자동 생성된 저장소명을 사용하므로 사용자가 디버깅하기 어렵다는 것이다. 관리 대상 속성과 비슷한 이름의 저장소명을 사용하려면 클래스 데커레이터나 메타클래스가 필요하다. 이에 대해서는 21장에서 다룬다.

디스크립터가 클래스로 정의되므로, 새로운 디스크립터를 생성할 때, 상속을 통해 기존 디스크립터를 재사용할 수 있다. 다음 절에서 자세히 알아보자.

---

**_ 프로퍼티 팩토리와 디스크립터 클래스_**

[bulkfood_v2prop.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-4/bulkfood_v2prop.py)에서 본 프로퍼티 팩토리에 몇 줄 추가함으로써 [bulkfood_v4.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v4.py)의 디스크립터 클래스를 향상시키는 것도 어렵지 않다. __counter 변수 때문에 어렵지만, 아래 예제에서 보는것처럼 이 변수 팩토리 함수 객체 자체의 속성으로 정의하면 팩토리의 실행이 끝나더라도 그 상태를 여구 보존할 수 있다.

- [bulkfood_v4prop.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v4prop.py)
1. storage_name 인수가 없다.
2. 카운터 상태를 보존하기 위한 클래스 속성에 의존할 수 없으므로, quantity() 함수 자체의 속성으로 정의한다.
3. quantity.counter가 정의되어 있지 않으면 0으로 설정한다.
4. 객체 속성이 없으므로, storage_name을 지역 변수로 설정하고, 클로저를 이용해서 나중에 qty_getter()와 qty_setter()가 사용할 수 있게 유지한다.
5. 나머지 코드는 bulkfood_v2prop.py 코드와 동일하지만, 여기서는 instance.__dict__에 직접 접근하는 대신 getattr()과 setattr() 내장 함수를 사용한다.

bulkfood_v4.py와 bulkfood_v4prop.py 중 어느 코드가 더 마음에 드는가?

필자는 다음과 같은 두 가지 이유 때문에 bulkfood_v4.py의 디스크립터 클래스를 선호한다.

* 디스크립터 클래스는 상속을 이용해서 확장할 수 있다. 팩토리 함수의 경우, 복사해서 붙여 넣지 않고서는 재사용하기 힘들다.
* 함수 속성과 클로저에 상태를 저장하는 bulkfood_v4prop.py보다 클래스와 객체 속성에 저장하는 것이 더 간단하다.

한편 bulkfood_v4prop.py를 설명할 때는 공장과 장치 표기법을 사용하고 싶은 마음이 들지 않았다. 프로퍼티 팩토리 코드에는 self와 instance라는 인수를 가진 디스크립터 메서드가 보여주는 이상한 객체 관계가 존재하지 않는다.

어떤 면에서 보면 프로퍼티 팩토리 패턴이 더 간단하지만, 디스크립터 클래스 방법은 확장성이 뛰어나다. 그리고 디스크립터 클래스가 널리 사용된다.

---

## LineItem 버전 #5: 새로운 디스크립터형

가상의 유기농 식품 가게가 궁지에 빠졌다. 어쩌다가 LineItem 객체 하나가 빈 description 속성으로 생성되어 주문을 완료할 수 없게 되었다. 이 문제를 방지하기 위해 새로운 디스크립터 NonBlank를 생성할 것이다. NonBlank를 설계하다보니 검증 논리를 제외하고는 Quantity 디스크립터와 아주 비슷하다는 것을 알게 되었다.

Quantity의 기능을 곰곰이 생각해보면, 두 가지 일을 한다. 관리 대상 객체의 저장소 속성을 관리하고, 이 속성을 설정하기 위해 사용되는 값을 검증한다. 따라서 이 두 작업으로 리팩토링해서 다음과 같이 두 개의 베이스 클래스를 생성하면 확장을 용이하게 할 수 있다.

---

**AutoStorage**
저장소 속성을 자동으로 관리하는 디스크립터 클래스

**Validated**
__set__() 메서드를 오버라이드해서 서브클래스에서 반드시 구현해야 하는 validate() 메서드를 호출하는 AutoStorage의 추상 서브클래스 

---

그러고 나서 Validated를 상속하고 validate() 메서드를 구현함으로써 Quantity 클래스를 작성하고 NonBlank를 구현한다. 아래 그림은 이 클래스들의 관계를 보여준다.

![validate_descriptor.png](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/validate_descriptor.png)

validated, Quantity, NonBlank 클래스 간의 관계는 템플릿 메서드 디자인 패턴을 응용한 것이다. 특히 Validated.__set__() 메서드는 에릭 감마, 리처드 헬름, 랄프 존슨, 존 블리시디스의 "Design Patterns: Elements of Reusable Object-Oriented Software."에서 다음과 같이 설명한 템플릿 메서드의 사례를 명확히 보여준다.

**템플릿 메서드는 서브클래스가 구체적인 동작을 구현하기 위해 오버라이드하는 추상적인 연산의 관점에서 알고리즘을 정의한다.**

이때 추상적인 연산은 검증이다. 아래 예제는 위 그림에 나온 클래스들을 구현한다.

- [model_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/model_v5.py)
1. AutoStorage는 이전 Quantity 디스크립터가 제공하던 기능 대부분을 제공한다.
2. 그러나 검증 기능은 제공하지 않는다.
3. Validated는 AutoStorage를 상속하지만, 추상 클래스다.
4. __set__()은 validate() 메서드에 검증을 위임한다.
5. 그러고 나서 반환된 값을 이용해서 실제로 값을 저장하는 슈퍼클래스의 __set__() 메서드를 호출한다.
6. 이 클래스의 validate()는 추상 메서드다.
7. Quantity와 NonBlank는 Validated 클래스를 상속한다.
8. 구상 validate() 메서드가 검증된 값을 반환하도록 요구함으로써, 전달받은 데이터를 정리, 변환, 혹은 정규화할 수 있는 기회를 제공한다. 여기서는 value 인수의 앞뒤에 있는 공백 문자를 제거하고 반환한다.

model_v5.py의 사용자는 이러한 내부 처리 과정을 알 필요 없다. 중요한 것은 Quantity와 NonBlank 디스크립터 클래스를 사용해서 객체 속성을 자동으로 검증할 수 있다는 것이다. 이 디스크립터들을 사용한 최신 LineItem 클래스는 bulkfood_v5.py와 같다.

- [bulkfood_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-1/bulkfood_v5.py)
1. model_v5 모듈을 임포트하고, 사용하기 편리한 이름을 부여한다.
2. model.NonBlank()를 사용한다. 나머지 코드는 그대로다.

지금까지 이 장에서 살펴본 LineItem 예제는 데이터 속성을 관리하는 디스크립터의 전형적인 사용법을 보여준다. 이러한 디스크립터는 오버라이딩 디스크립터라고도 한다. 디스크립터의 __set__() 메서드가 관리 대상 객체 안에 있는 동일한 이름의 속성 설정을 오버라이드(즉, 가로채서 변경하기)하기 때문이다. 그러나 오버라이드하지 않는 논오버라이딩 디스크립터도 있다. 이 둘의 차이점에 대해서는 다음 절에서 자세히 설명한다.