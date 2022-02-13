<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-4/UML_class_diagram.png)
 -->
# 프로퍼티 팩토리 구현하기

여기서는 quanity()라는 프로퍼티 팩토리를 만든다. 이 팩토리가 관리하는 속성은 0보다 큰값만 가져야 한다는 의미에서 quantity 라는 이름을 붙였다. bulkfood_v2prop.py은 두 개의 quantity 프로퍼티 객체를 이용해서 정의한 깔끔한 LineItem 클래스를 보여준다. 프로퍼티 객체 하나는 weight 속성을, 다른 하나는 price 속성을 관리한다.

```
class LineItem:
    weight = quantity('weight')  # <1>
    price = quantity('price')  # <2>

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # <3>
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # <4>
```
1. 팩토리를 이용해서 첫 번째 프로퍼티 weight를 클래스 속성으로 정의한다.
2. 두 번째 호출할 때는 또 다른 프로퍼티 price가 정의된다.
3. 이미 프로퍼티가 활성화되어 있으므로 weight가 0이나 음수가 되지 않게 보장한다.
4. 이미 프로퍼티가 사용되고 있으므로 객체에 저장된 값을 가져온다.

프로퍼티는 클래스 속성이라는 점을 주의하라. quantity() 르포러티를 생성할 때 해당 프로퍼티에 의해 관리된 LineItem 속성의 이름을 전달해야 한다. 다음 코드에서 weight라는 단어를 두 번이나 입력하는 것은 좋지 않아 보인다.
```
weight = quantity('weight')
```

그러나 프로퍼티가 어느 클래스 속성명에 바인딩해야 할지 알 수 있는 방법이 없으므로, 이렇게 반복하지 않으면 복잡해진다. 할당문의 오른쪽이 먼저 평가되므로 quantity()가 호출될 때 weight 클래스 속성은 존재하지 않음에 주의하라.

> 속성명을 두 번 입력하지 않도록 quantity()를 개선하려면 아주 복잡한 메타프로그래밍 기법을 사용해야 한다. 20장에서 임시방편을 설명하지만, 제대로 해결하려면 클래스 데커레이터나 메타클래스를 사용해야 하므로 21장을 공부할 때까지 기다린다.

아래의 코드는 quantity() 프로퍼티 팩토리의 소스 코드를 보여준다.

```
def quantity(storage_name):  # <1>

    def qty_getter(instance):  # <2>
        return instance.__dict__[storage_name]  # <3>

    def qty_setter(instance, value):  # <4>
        if value > 0:
            instance.__dict__[storage_name] = value  # <5>
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)  # <6>
```
1. storage_name 인수는 각 프로퍼티를 어디에 저장할지 결정한다. weight 속성의 경우 storage_name은 'weight'가 된다.
2. qty_getter()의 첫 번째 인수명을 self로 할 수도 있지만, 이 메서드가 클래스 본체에 있는 것이 아니므로 저장할 객체를 가리키게 된다. 즉, instacne는 속성을 저장할 LienItem 객체를 가리킨다.
3. qty_getter()가 storage_name을 참조하므로, storage_name은 이 함수의 클로저에 보관된다. 프로퍼티를 사용하면 무한히 재귀적으로 호출되므로, 프로퍼티를 우회하기 위해 instance.__dict__에서 직접 속성을 가져온다.
4. qty_setter()도 첫 번째 인수로 instance를 받도록 정의한다.
5. 여기에서도 프로퍼티를 우회해서 istance.__dict__에 직접 value를 저장한다.
6. 사용자 정의 프로퍼티 객체를 생성해서 반환한다.

bulkfood_v2prop.py에서 storage_name 변수 주변 코드를 주의 깊게 살펴보기 바란다. 프로퍼티를 전통적인 방식으로 구현하는 경우에는 값을 저장할 속석명이 게터와 세터 메서드 안에 하드코딩된다. 그러나 여기서 qty_getter()와 qty_setter()는 범용 함수로서, 객체의 __dict__안에 있는 어느 속성에서 값을 가져오고 어느 속성에 값을 저장할지 판단하기 위해 storage_name에 의존한다. quantity() 팩토리 함수가 호출될 때마다 프로퍼티를 생성하므로, storage_name은 고유한 값으로 설정되어야 한다.

qty_getter()와 qty_setter() 함수는 팩토리 함수 마지막 행에서 생성된 property 객체에 의해 래핑된다. 나중에 호출될 때 이 함수들은 자신의 클로저에서 storage_name을 가져와서 어느 속성을 읽고, 어느 속성에 저장할지 결정한다.

아래 bulkfood_v2prop.py에서는 LineItem 객체를 생성하고 조사해서 값을 저장하는 속성을 보여준다.

```
# bulkfood_v2prop.py: quantity() 프로퍼티 팩토리
nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
nutmeg.weight, nutmeg.price #1
# (8, 13.95)
sorted(vars(nutmeg).items()) #2
# [('description', 'Moluccan nutmeg'), ('price', 13.95), ('weight', 8)]
```
1. 프로퍼티를 통해 weight와 price를 읽으므로 동일한 이름의 객체 속성을 가린다.
2. vars()를 이용해서 nutmeg 객체를 조사한다. 여기서는 값을 저장하기 위해 사용되는 실제 객체 속성을 보여준다.

패ㅐㄱ토리가 만든 프로퍼티가 19.3.1절 '객체 속성을 가리는 프로퍼티'에서 설명한 대로 작동하고 있음을 명심하라. weight 프로퍼티는 weight 객체 속성을 가리므로 self.weight나 nutmeg.weight로 참조하는 것은 모두 프로퍼티 함수에 의해 처리되며, 객체의 __dict__에 접근하는 방법을 이용해야 프로퍼티 논리를 우회할 수 있다.

bulkfood_v2prop.py의 코드는 약간 어렵지만, 아주 간단하다. 길이로 보면 [bulkfood_v2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-2/bulkfood_v2.py)에서 정의한 weight 프로퍼티의 게터와 세터 메서드와 똑같다. [bulkfood_v2prop.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-4/bulkfood_v2prop.py)에서의 LineItem 정의는 게터와 세터로 어지렵혀져 있지 않으므로 훨씬 더 보기 좋다.

실제 시스템에서는 이런 형태의 검증을 여러 필드와 클래스에서 볼 수 있으며, quantity() 프로퍼티 팩토리는 유틸리티 모듈에 넣어 계속 사용할 수 있다. 결국 이 간단한 팩토리는 리팩토링을 통해 확장성이 향상된 디스크립터 클래스가 되며, 특화된 서브클래스는 여러 가지 다른 형태의 검증을 수행한다. 20장에서는 이와 같은 예제를 만들어본다.

이제 속성 제거 문제를 알아보면서 프로퍼티에 대한 설명을 마치고자한다.