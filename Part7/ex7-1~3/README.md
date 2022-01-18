# 데커레이터 기본 지식
<!-- 
![UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-1~3/UML_class_diagram.png)
 -->
데커레이터는 다른 함수를 인수로 받는 콜러블(데커레이트된 함수)이다. 데커레이터는 데커레트된 함수에 어떤 처리를 수행하고, 함수를 반환하거나 함수를 다른 함수나 콜러블 객체로 대체한다.

예를 들어 다음 코드에서처럼 decorate라는 이름의 데커레이터가 있다고 가정하자.

```
@decorate
def target():
    print('running target()')
```
위 코드는 다음과 동일하게 작동한다.

```
def target():
    print('running target()')
target = decorate(target)
```
결과는 동일하다. 두 코드를 실행한 후 target은 꼭 원래의 target()함수를 가리키는 것이 아니며, decorate(target)이 반환함 함수를 가르키게 된다.

데커레이트된 함수가 대체되었는지 확인하기 위해 아래의 예제를 보자.
- [데커레이터 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-1~3/decorate.py)
    1. deco()가 inner()함수 객체를 반환한다.
    2. target()을 deco로 데커레이트했다.
    3. 데커레이트된 target()을 호출하면 실제로는 inner()를 실행한다.
    4. 조사해보면 target이 inner()를 가리키고 있음을 알 수 있다.

엄밀히 말해 데커레이터는 편리구문일뿐이다. 방금 전에 본 것처럼 데커레이터는 다른 함수를 인수로 전달해서 호출하는 일반적인 콜러블과 동일하다. 그렇지만 런타임에 프로그램 행위를 변경하는 **메타프로그래밍**을 할 때 데커레이터가 상당히 편리하다.

지금까지의 설명을 요약해보자. 첫째, 데커레이터는 데커레이트된 함수를 다른 함수로 대체하는 능력이 있다. 둘째, 데커레이터는 모듈이 로딩될 때 바로 실행된다. 다음 절에서는 두 번째 성질에 대해 알아보자.

# 파이썬이 데커레이터를 실행하는 시점
데커레이터의 핵심 특징은 데커레이트된 함수가 정으된 직후에 실행된다는 것이다. 이는 일반적으로 파이썬이 모듈을 로딩하는 시점, 즉 **임포트 타임**에 실행된다.
아래 예제를 보자.
- [registration.py모듈](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-1~3/registration.py)
    1. registry 배열은 @register로 데커레이트된 함수들에 대한 참조를 담는다.
    2. register()는 함수를 인수로 받는다.
    3. 데커레이트된 함수를 출력한다(시험용)
    4. func를 registry에 추가한다.
    5. func를 반환한다. 반드시 함수를 반환해야 하며, 여기서는 인수로 받은 함수를 그대로 반환한다.
    6. f1과 f2는 @register로 장식되었다.
    7. f3는 데커레이트되지 않았다.
    8. main()은 registry를 출력하고 f1(),f2(),f3()를 차례로 호출한다.
    9. main()은 registration.py를 스크립트로 실행할 때만 호출된다.

register()는 모듈 내의 다른 어떠한 함수보다 먼저 실행(두번)된다. register()가 호출될 때 데커레이트된 함수(예를 들면 <function f1 at 0x100631bf8>)를 인수로 받는다.

모듈이 로딩된 후 registry는 데커레이트된 두 개의 함수 f1()과 f2()에 대한 참조를 가진다. 이 두 함수(물론f3()도 포함하여)는 main()에 의해 명시적으로 호출될 때만 실행된다.

registration.py를 스크립트로 실행하지 않고 임포트하면 다음과 같이 출력된다.

```
>>> import registration
running register(<function f1 at 0x000001B3CF2D69D0>)
running register(<function f2 at 0x000001B3CF2D6940>)
```

이때 registry를 살펴보면 다음과 같은 내용이 들어 있다.
```
>>> registration.registry
[<function f1 at 0x000001B3CF2D69D0>, <function f2 at 0x000001B3CF2D6940>]
```

위를 통해 함수 데커레이터는 모듈이 임포트되자마자 실행되지만, 데커레이트된 함수는 명시적으로 호출될 때만 실행됨을 알 수 있다. 이 예제는 파이썬 개발자가 **임포트 타임**이라고 부르는 것과 **런타임**이라고 부르는 것의 차이를 명확히 보여준다.

데커레이터가 실제 코드에 흔히 사용되는 방식과 비교해서 위 예제는 다음 두 가지 차이점이 있다.
* 데커레이터 함수가 데커레이트되는 함수와 같은 모듈에 정의되어 있다. 일반적으로 실제 코드에서는 데커레이터를 정의하는 모듈과 데커레이터를 적용하는 모듈을 분리해서 구현한다.
* register() 데커레이터가 인수로 전달된 함수와 동일한 함수를 반환한다. 실제 코드에서 대부분의 데커레이터는 내부 함수를 정의해서 반환한다.

위의 register() 데커레이터가 데커레이트된 함수를 그대로 반환하기는 하지만, 이 기법이 쓸모없는 것은 아니다. URL 패턴을 HTTP 응답 생성 함수에 매핑하는 레지스트리 등 함수를 어떤 중앙의 레지스트리에 추가하기 위해 여러 파이썬 웹 프레임워크에서 이와 비슷한 데커레이터가 사용된다. 이러한 등록 데커레이터들은 데커레이트된 함수를 변경할 수도 있고 아닐 수도 있다. 다음절에서는 데커레이터를 실제로 적용해보자.

# 데커레이터로 개선한 전략 패턴
등록 데커레이터는 Part6에서 구현한 전자상거래 프로모션 할인 코드를 개선하는 데 유용하게 사용할 수 있다.
```
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """최대로 할인받을 금액을 반환한다."""
    return max(promo(order) for promo in promos)
```
위 소스에서 가장 큰 문제는 함수를 정의할 때, 그리고 가장 큰 할인 방식을 결정하는 best_promo()함수에 의해 사용되는 promos리스트에 함수명을 반복해서 사용한다는 점이다. 코드를 반복하는 것은 문제가 있다. 예를 들어 새로운 프로모션 전략 함수를 추가했는데 promos 리스트에 이 함수를 추가하는 것을 깜빡 잊었다면, best_promo()는 새로운 전략 함수를 무시하므로 시스템에 포착하기 힘든 버그가 발생할 수 있다. 아래 예제는 등록 데커레이터를 이용해서 이 문제를 해결한다.

- [promotion 데커레이터로 채운 promos리스트](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-1~3/deco_promotion.py)
    1. 빈 promos 리스트로 시작한다.
    2. promotion()데커레이터는 promo_func를 promos 리스트에 추가한 후 그대로 반환한다.
    3. @promotion으로 데커레이트한 함수는 모두 promos 리스트에 추가된다.
    4. best_promos()는 promos 리스트에 의존하므로 변경할 필요 없다.

이 방법은 [기존 promotion](https://github.com/hyeonDD/fluent_python/blob/master/Part6/ex6-1/order_class_refactoring_usage.py)에서 구현한 예제 코드에 비해 다음과 같은 장점이 있다.
* 프로모션 전략 함수명이 특별한 형태로 되어 있을 필요 없다(이제는 함수명이 _promo로 끝나지 않아도 된다.)
* @promotion 데커레이터는 데커레이트된 함수의 목적을 명확히 알려주며, 임시로 어떤 프로모션을 배제할 수 있다. 단지 데커레이터만 주석처리하면 된다.
* 프로모션 할인 전략을 구현한 함수는 @promotion 데커레이터가 적용되는 한 어느 모듈에서든 정의할 수 있다.

대부분의 데커레이터는 데커레이트된 함수를 변경한다. 즉, 내부 함수를 정의하고 그것을 반환하여 데커레이트된 함수를 대체한다. 내부 함수를 사용하는 코드는 제대로 작동하기 위해 거의 항상 클로저에 의존한다. 클로저를 이해하기 위해 먼저 파이썬에서 변수 범위의 작동 방식에 대해 자세히 살펴보자.